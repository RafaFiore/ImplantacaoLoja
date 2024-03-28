import EmailInfo
from nested_lookup import nested_lookup


class Implantacao:
    def __init__(self):
        self.email_obj = EmailInfo.EmailInfo()

    def get_form_content(self):
        form_response = self.email_obj.search_forms()
        values = nested_lookup('_values', form_response)[0]
        return values


if __name__ == "__main__":
    implant = Implantacao()
    implant.get_form_content()