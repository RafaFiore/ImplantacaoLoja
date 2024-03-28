import email
import imaplib
import json
import html_to_json
import os
from dotenv import load_dotenv
import logger
from email.mime.text import MIMEText
import html

class EmailInfo:
    def __init__(self):
        load_dotenv()
        self.__email_acc = os.getenv("email_acc")
        self.__email_pw = os.getenv("email_pw")
        self.__imap_host = os.getenv("imap_host")
        self.__imap_port = os.getenv("imap_port")
        self.__sender = os.getenv("sender")
        self.log = logger.Logger()
        self.report_dir = 'anexos'

    def imap_conn(self):
        try:
            conn = imaplib.IMAP4_SSL(self.__imap_host, self.__imap_port)
            conn.login(self.__email_acc, self.__email_pw)
            status, messages = conn.select('Inbox')
        except imaplib.IMAP4.abort as err:
            self.log.error('error.log', err)
        return conn, status, messages

    def delete_mail(self, num, conn):
        try:
            conn.store(num, "+FLAGS", "\\Deleted")
        except Exception as err:
            self.log.error('error.log', err)
            exit()

    def mail_check(self, num, conn):
        res, msg = conn.fetch(str(num), '(RFC822)')
        # self.delete_mail(str(num), conn)
        try:
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if part.get_content_maintype() == "multipart":
                                continue
                            try:
                                body = part.get_payload(decode=True).decode()
                            except RuntimeError as err:
                                print(err)
                                exit()
                            if content_type == 'text/html':
                                conteudo_html = MIMEText(body, 'html')
                            else:
                                conteudo = body
                            content_disposition = str(part.get('Content-Disposition'))
                            if 'attachment' in content_disposition:
                                report = part.get_filename()
                                if report:
                                    if not os.path.isdir(self.report_dir):
                                        os.mkdir(self.report_dir)
                                    filepath = os.path.join(self.report_dir, report)
                                    open(filepath, 'wb').write(part.get_payload(decode=True))
                    else:
                        # extrair tipo de conteúdo do email
                        content_type = msg.get_content_type()

        except RuntimeError as err:
            self.log.error('error.log', err)
        conteudo_json = html_to_json.convert(body)
        return conteudo_json

    def search_forms(self):
        conn, status, messages = self.imap_conn()
        try:
            status, messages = conn.search(None, f'(OR (FROM "{self.__sender}" ) (FROM "{self.__sender}"))')
            if messages[0]:
                print(f'num msgs: {int(messages[0].split()[-1])}')
                n = 1
                messages = int(messages[0].split()[-1])
                for num in range(messages, messages - n, -1):
                    form_response_json = self.mail_check(num, conn)
                # conn.expunge()
                conn.close()
                conn.logout()
                return form_response_json
            else:
                exit()
        except RuntimeError as err:
            self.log.error('error.log', err)