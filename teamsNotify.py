import pymsteams
import logger

class TeamsNotifications:
    def __init__(self):
        #Prod
        # self.msteams_webhook = pymsteams.connectorcard("https://newfolddigital.webhook.office.com/webhookb2/b9f649c2-6d9b-4614-ac98-563fab025cb8@d3008fd4-0d20-418b-bf30-4e70d910c727/IncomingWebhook/ebbe2a90ccbd41d19cc37d28f84858b2/05e16ef1-14de-48ff-a511-492d21158794")

        #Teste
        self.msteams_webhook = pymsteams.connectorcard("https://newfolddigital.webhook.office.com/webhookb2/5603c95b-a727-4822-8fc2-622c29a29cf7@d3008fd4-0d20-418b-bf30-4e70d910c727/IncomingWebhook/1c382c78303e4e19bb90247099c77401/05e16ef1-14de-48ff-a511-492d21158794")
        self.log = logger.Logger()

    def send_notification(self, dominio, email, forms_url):
        try:
            self.msteams_webhook.title(f'Notificações Implantação')
            texto = (f"Não foi possível encontrar um ticket para o cliente abaixo.    \nDomínio: {dominio}    \nEmail: {email}    \nLink para respsota: {forms_url}")
            self.msteams_webhook.text(texto)
            self.msteams_webhook.send()
        except pymsteams.TeamsWebhookException as err:
            self.log.error('error.log', err)
