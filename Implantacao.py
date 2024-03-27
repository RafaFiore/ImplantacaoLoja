import EmailInfo


class Implantacao:
    def __init__(self):
        self.email_obj = EmailInfo.EmailInfo()

    def get_form_content(self):
        self.email_obj.search_forms()


if __name__ == "__main__":
    implant = Implantacao()
    implant.get_form_content()