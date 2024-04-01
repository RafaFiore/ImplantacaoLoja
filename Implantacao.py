import EmailInfo
from nested_lookup import nested_lookup
import DB
import re

import logger
import zenRequests


class Implantacao:
    def __init__(self, brand):
        self.brand = brand
        self.email_obj = EmailInfo.EmailInfo()
        self.zenAPI = zenRequests.ZenAPI('dloja')
        self.db_conn = DB.Database()
        self.zenAPI = zenRequests.ZenAPI(self.brand)

    def get_form_content(self):
        form_response = self.email_obj.search_forms()
        values = nested_lookup('_values', form_response)[0]
        return values

    def search_rd_tickets(self):
        query = 'type%3Aticket%20requester%3Arafael.fiorentini%40newfold.com%20status%3Aopen%20status%3Anew%20Implanta%C3%A7%C3%A3o%20Ecommerce'
        url = self.zenAPI.new_urls[self.brand] + self.zenAPI.search + query
        response = self.zenAPI.get_request(url, new_instance=True)
        result = response['results']
        return result

    def check_tickets(self, rd_ticket_id):
        ticket_created = self.db_conn.select_rd_tickets(rd_ticket_id)
        return ticket_created

    def check_zd_user(self, cst_email):
        url = self.zenAPI.new_urls[self.brand] + self.zenAPI.search_users + cst_email
        response = self.zenAPI.get_request(url, new_instance=True)
        user = response['users']
        return user

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

    def zd_template(self):
        ticket_subject = 'Parabéns por escolher a Loja HostGator - Solicitação de Informações'
        with open('templates\\ticket_template', mode='r', encoding='utf8') as ticket_template:
            zd_comment = ticket_template.read()
        return ticket_subject, zd_comment

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

    def process_implantacao(self):
        log = logger.Logger()
        rd_tickets = self.search_rd_tickets()
        rd_lead_pattern = 'https://app.rdstation.com.br/leads/public/.*\\/s'
        for i in rd_tickets:
            rd_ticket_id = i['id']
            ticket_date = i['created_at']
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
            print(ticket)


if __name__ == "__main__":
    implant = Implantacao('dloja')
    implant.process_implantacao()
