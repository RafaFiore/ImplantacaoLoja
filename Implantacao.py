import time
import EmailInfo
from nested_lookup import nested_lookup
import DB
import re
import logger
import zenRequests
from datetime import datetime
from dateutil import parser
import teamsNotify


class Implantacao:
    def __init__(self, brand):
        self.brand = brand
        self.email_obj = EmailInfo.EmailInfo()
        self.zenAPI = zenRequests.ZenAPI('dloja')
        self.db_conn = DB.Database()
        self.zenAPI = zenRequests.ZenAPI(self.brand)
        self.db_values = []
        self.teams_notify = teamsNotify.TeamsNotifications()

    # Obter conteúdo da resposta do forms
    def get_form_content(self):
        form_response, num_msgs = self.email_obj.search_forms()
        values = nested_lookup('_values', form_response)[0]
        return values, num_msgs

    # Procurar no Zendesk os tickets em aberto da RD
    def search_rd_tickets(self):
        query = 'type%3Aticket%20requester%3Arafael.fiorentini%40newfold.com%20status%3Aopen%20status%3Anew%20Implanta%C3%A7%C3%A3o%20Ecommerce'
        url = self.zenAPI.new_urls[self.brand] + self.zenAPI.search + query
        response = self.zenAPI.get_request(url, new_instance=True)
        result = response['results']
        return result

    # Verificar se já existe um ticket de implatanção em aberto
    def check_tickets(self, rd_ticket_id):
        ticket_created = self.db_conn.select_rd_tickets(rd_ticket_id)
        return ticket_created

    # Verificar se o cliente já tem cadastro no Zendesk
    def check_zd_user(self, cst_email):
        url = self.zenAPI.new_urls[self.brand] + self.zenAPI.search_users + cst_email
        response = self.zenAPI.get_request(url, new_instance=True)
        user = response['users']
        return user

    # Criar usuário no Zendesk
    def create_zd_user(self, cst_email, nome):
        endpoint = 'users'
        payload = {
            "user": {
                "email": f"{cst_email}",
                "name": f"{nome}",
                "role": "end-user",
                "verified": "true"
            }
        }
        response = self.zenAPI.post_request(payload, endpoint)
        return response

    # Definir o assunto e comentários do ticket
    def zd_template(self):
        ticket_subject = 'Parabéns por escolher a Loja HostGator - Solicitação de Informações'
        with open('templates\\ticket_template', mode='r', encoding='utf8') as ticket_template:
            zd_comment = ticket_template.read()
        return ticket_subject, zd_comment

    # Criar ticket na Zendesk
    def create_ticket(self, cst_email):
        subject, comment = self.zd_template()
        submitter_id = 24966456979859 # TROCAR PARA PROD
        group_id = 24966089236755 # TROCAR PARA PROD
        brand_id = 26558151214099 # TROCAR PARA PROD
        payload = {
            "ticket": {
                "subject": f"{subject}",
                "comment": {
                    "body": f"{comment}"
                },
                "submitter_id": submitter_id,
                "requester": {
                    "email": f"{cst_email}"
                },
                "group_id": group_id,
                "is_public": "true",
                "status": "pending",
                "brand_id": brand_id
            }
        }
        response = self.zenAPI.post_request(payload, self.zenAPI.create_tickets)
        return response

    # Atualizar tickets na Zendesk
    def update_tickets(self, ticket_id, comment, status):
        url = self.zenAPI.new_urls[self.brand] + self.zenAPI.ticekts + ticket_id
        submitter_id = 24966456979859  # TROCAR PARA PROD
        payload = {
            "ticket": {
                "comment": {
                    "body": f"{comment}",
                    "public": "false"
                },
                "submitter_id": submitter_id,
                "status": f"{status}"
            }
        }
        response = self.zenAPI.put_request(payload, url)
        return response

    # Ajustar a data do ticket para BR
    def ticket_date_parser(self, ticket_date):
        new_ticket_date = parser.parse(ticket_date)
        new_ticket_date = new_ticket_date.astimezone(tz=None).replace(tzinfo=None)
        return new_ticket_date

    # Criar lista de tupla com os valores para inserir no banco de dados
    def add_db_values(self, ticket_id, rd_ticket_id, cst_email, cst_name, rd_ticket_date, ticket_date, status):
        rd_ticket_date_br = self.ticket_date_parser(rd_ticket_date)
        values_tuple = (ticket_id, rd_ticket_id, cst_email, cst_name, rd_ticket_date_br, ticket_date, status)
        self.db_values.append(values_tuple)

    # Adicionar os dados no banco de dados
    def add_to_db(self, values):
        if values:
            self.db_conn.insert_ticket(values)

    # Função principal de processamento que envolvem tickets
    def process_implantacao(self):
        log = logger.Logger()
        rd_tickets = self.search_rd_tickets()
        rd_lead_pattern = 'https://app.rdstation.com.br/leads/public/.*\\/s'
        if rd_tickets:
            for i in rd_tickets:
                rd_ticket_id = str(i['id'])
                rd_ticket_date = i['created_at']
                subject = i['subject']
                cst_email = subject.split('-')[1].strip()
                cst_name = subject.split('-')[2].strip()
                rd_lead_url = re.findall(rd_lead_pattern, i['description'])[0]
                print(rd_lead_url)
                print(cst_email)
                ticket_created = self.check_tickets(rd_ticket_id)
                if ticket_created:
                    print(f'Implantação já encaminhada: {rd_ticket_id}')
                    continue
                else:
                    user_exists = self.check_zd_user(cst_email)
                    if user_exists:
                        print(f'Usuário {cst_email} já existe, não é necessário criar')
                    else:
                        new_user = self.create_zd_user(cst_email, cst_name)
                        log.info('debug.log', f'New Zendesk user created - {new_user["user"]["url"]}')
                ticket = self.create_ticket(cst_email)
                ticket_id = str(ticket['ticket']['id'])
                job_status_url = ticket['job_status']['url']
                job_status_response = self.zenAPI.get_request(job_status_url, new_instance=True)
                job_status = job_status_response['job_status']['status']
                rd_comment = f'Ticket aberto com o cliente: {ticket_id}'
                rd_ticket_response = self.update_tickets(rd_ticket_id, rd_comment, status='solved')
                print(rd_ticket_response)
                cst_comment = f"""
                Ticket da RD: {rd_ticket_id}
                Link para dados do cliente: {rd_lead_url}
                """
                if job_status == 'completed':
                    cst_ticket_response = self.update_tickets(ticket_id, cst_comment, status='pending')
                    ticket_date = datetime.now().replace(microsecond=0)
                    print(cst_ticket_response)
                else:
                    print('Aguardando criação do ticket')
                    time.sleep(15)
                    cst_ticket_response = self.update_tickets(ticket_id, cst_comment, status='pending')
                    ticket_date = datetime.now().replace(microsecond=0)
                    print(cst_ticket_response)
                self.add_db_values(ticket_id, rd_ticket_id, cst_email, cst_name, rd_ticket_date, ticket_date, 'pending')
        else:
            print('Sem ticket')
            exit()
        self.add_to_db(self.db_values)

    # Função principal de processamento de email s forms
    def process_form_answers(self):
        num_msgs = 1
        while num_msgs > 0:
            form_answer, num_msgs = self.get_form_content()
            dominio = form_answer[0]
            cst_email = form_answer[1]
            form_link = form_answer[2]
            ticket_exists = self.db_conn.select_customers(cst_email)
            if ticket_exists:
                ticket_id = str(ticket_exists[0])
                comment = f"""
                Prosseguir com implatanção.
                Link para respostas do forms do cliente: {form_link} 
                """
                response = self.update_tickets(ticket_id, comment, status='open')
                self.db_conn.update_ticket(ticket_id)
            else:
                print('Ticket não encontrado com o email do cliente')
                self.teams_notify.send_notification(dominio, cst_email, form_link)


if __name__ == "__main__":
    implant = Implantacao('dloja')
    implant.process_form_answers()
