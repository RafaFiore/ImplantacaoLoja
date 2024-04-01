import EmailInfo
from nested_lookup import nested_lookup
import DB

import zenRequests


class Implantacao:
    def __init__(self):
        self.email_obj = EmailInfo.EmailInfo()
        self.zenAPI = zenRequests.ZenAPI('dloja')
        self.db_conn = DB.Database()

    def get_form_content(self):
        form_response = self.email_obj.search_forms()
        values = nested_lookup('_values', form_response)[0]
        return values

    def search_rd_tickets(self):
        pass

    def check_tickets(self, rd_ticket_id):
        ticket_created = self.db_conn.select_rd_tickets(rd_ticket_id)
        return ticket_created


if __name__ == "__main__":
    implant = Implantacao()
    implant.check_tickets()