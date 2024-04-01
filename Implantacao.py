import EmailInfo
from nested_lookup import nested_lookup
import DB
import re

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
        rd_lead_pattern = 'https://app.rdstation.com.br/leads/public/.*\\/s'
        query = 'type%3Aticket%20requester%3Arafael.fiorentini%40newfold.com%20status%3Aopen%20status%3Anew%20Implanta%C3%A7%C3%A3o%20Ecommerce'
        url = self.zenAPI.new_urls[self.brand] + self.zenAPI.search + query
        response = self.zenAPI.get_request(url, new_instance=True)
        result = response['results']
        for i in result:
            print(result)
            ticket_id = i['id']
            ticket_date = i['created_at']
            subject = i['subject']
            cst_email = subject.split('-')[1].strip()
            cst_name = subject.split('-')[2].strip()
            rd_lead_url = re.findall(rd_lead_pattern, i['description'])[0]
            print(rd_lead_url)
            print(cst_email)

    def check_tickets(self, rd_ticket_id):
        ticket_created = self.db_conn.select_rd_tickets(rd_ticket_id)
        return ticket_created


if __name__ == "__main__":
    implant = Implantacao('dloja')
    implant.search_rd_tickets()
