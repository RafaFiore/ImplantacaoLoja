import requests
import os
from dotenv import load_dotenv
import time
import logger
from zenpy import Zenpy


# noinspection PyUnboundLocalVariable
class ZenAPI:
    def __init__(self, brand):
        self.brand = brand
        load_dotenv()
        self.__user = os.getenv("zd_user")
        self.__dloja_user = os.getenv("dloja_zd_user")
        self.__token = os.getenv(f"token_{brand.lower()}")
        self.__new_token = os.getenv('new_token')
        self.header = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        self._attach_header = {
            "Content-type": "image/gif",
            "Content-type": "application/json"
        }
        self.__url = f'https://hostgator{brand}.zendesk.com/api/v2/'
        self.__categories_endpoint = 'help_center/categories'
        self.log = logger.Logger()
        self.__permission_group_endpoint = 'guide/permission_groups.json'
        self.__user_segments_endpoint = 'help_center/user_segments'
        self.__sections_endpoint = 'help_center/sections.json?page[size]=100'
        self.__section_endpoint = 'help_center/sections/'
        self.__articles_endpoint = 'help_center/articles.json?page[size]=100'
        self.__show_article_endpoint = 'help_center/articles/'
        self.__users = 'users.json?page[size]=100'
        self.__search_users = 'users/search?query='
        self.__create_many_users = 'users/create_many'
        self.__search = 'search.json?query='
        self.__create_tickets = 'tickets.json?async=true'
        self.__tickets = 'tickets/'
        self.__instances = {
            "br": {
                "url": "https://hostgatorbr.zendesk.com/api/v2/",
                "token": f"{os.getenv('token_br')}"
            },
            "es": {
                "url": "https://hostgatormx.zendesk.com/api/v2/",
                "token": f"{os.getenv('token_mx')}"
            },
            "dloja": {
                "url": "https://dlojavirtual.zendesk.com/api/v2/",
                "token": f"{os.getenv('token_dloja')}"
            }
        }

        self.__new_urls = {
            "br": "https://hgsandboxoficial.zendesk.com/api/v2/",
            "dloja": "https://atendimentohgbrasil1704801360.zendesk.com/api/v2/"
        }

        self.__subdomains = {
            "br": "hgsandboxoficial",
            "es": "placeholderES",
            "dloja": "dlojasb"
        }

        self.creds = {
            "email": f"{self.__user}",
            "token": f"{self.__new_token}",
            "subdomain": f"{self.subdomains[self.brand]}"
        }

    @property
    def url(self):
        return self.__url

    @property
    def instances(self):
        return self.__instances

    @property
    def new_urls(self):
        return self.__new_urls

    @property
    def subdomains(self):
        return self.__subdomains

    @property
    def categories_endpoint(self):
        return self.__categories_endpoint

    @property
    def permission_group_endpoint(self):
        return self.__permission_group_endpoint

    @property
    def user_segments_endpoint(self):
        return self.__user_segments_endpoint

    @property
    def sections_endpoint(self):
        return self.__sections_endpoint

    @property
    def section_endpoint(self):
        return self.__section_endpoint

    @property
    def articles_endpoint(self):
        return self.__articles_endpoint

    @property
    def show_article_endpoint(self):
        return self.__show_article_endpoint

    @property
    def users(self):
        return self.__users

    @property
    def search_users(self):
        return self.__search_users

    @property
    def create_many_users(self):
        return self.__create_many_users

    @property
    def search(self):
        return self.__search

    @property
    def create_tickets(self):
        return self.__create_tickets

    @property
    def ticekts(self):
        return self.__tickets

    def get_request(self, url, new_instance):
        log = logger.Logger
        if new_instance:
            token = self.__new_token
            user = self.__user
        else:
            token = self.instances[self.brand]['token']
            if self.brand == 'dloja':
                user = self.__dloja_user
            else:
                user = self.__user

        try:
            log = logger.Logger()
            request = requests.get(url, auth=(user + '/token', token), headers=self.header)
            if request.status_code == 429:
                seconds_to_wait = int(request.headers['Retry-After'])
                log.info('debug.log', f'HTTP 429 - Waiting {seconds_to_wait} seconds to retry')
                time.sleep(seconds_to_wait)
                return self.get_request(url, new_instance)

            if 'X-Rate-Limit-Remaining' in request.headers.keys():
                rate_limit = int(request.headers['X-Rate-Limit-Remaining'])
                if 300 > rate_limit > 200:
                    time.sleep(10)
                elif 200 > rate_limit > 100:
                    time.sleep(20)
                elif rate_limit < 100:
                    time.sleep(40)
            if request.status_code == 200:
                return request.json()
            else:
                log.error('error.log', f'URL: {url} - Status: {request.status_code}')
                return False
        except requests.exceptions.RequestException as err:
            log.error('error.log', err)

    def post_request(self, payload, endpoint):
        url = self.new_urls[self.brand] + endpoint
        log = logger.Logger()
        try:
            request = requests.post(url, auth=(self.__user + '/token', self.__new_token), headers=self.header,
                                    json=payload)
            if request.status_code == 429:
                seconds_to_wait = int(request.headers['Retry-After'])
                log.info('debug.log', f'HTTP 429 - Waiting {seconds_to_wait} seconds to retry')
                time.sleep(seconds_to_wait)
                return self.post_request(payload, endpoint)
            elif request.status_code == 201 or request.status_code == 200 or request.status_code == 202:
                return request.json()
            elif request.status_code == 503:
                return self.post_request(payload, endpoint)
            else:
                log.error('error.log', f'URL: {url} - Status: {request.status_code}')
        except requests.exceptions.RequestException as err:
            log.error('error.log', err)

    def upload_attachment(self, attachment, file_name, content_type):
        zenpy_client = Zenpy(**self.creds)
        try:
            attach = zenpy_client.help_center.attachments.create_unassociated(attachment=attachment,
                                                                              file_name=file_name,
                                                                              inline='true',
                                                                              content_type=content_type)
            return attach.to_dict(serialize=True)
        except requests.exceptions.HTTPError:
            self.log.error('error.log', 'Post expection, waiting 30 seconds to retry')
            time.sleep(30)
            return self.upload_attachment(attachment, file_name, content_type)

    # Fazer download do anexo
    # noinspection PyUnboundLocalVariable
    def get_attachment(self, url):
        log = logger.Logger()
        try:
            request = requests.get(url, auth=(self.__dloja_user + '/token', self.__token), headers=self._attach_header)
            if request.status_code == 200:
                return request
        except requests.exceptions.RequestException as err:
            log.error('error.log', f'Error: {request.status_code} - {err}')

    def put_request(self, payload, url):
        log = logger.Logger()
        try:
            request = requests.put(url, auth=(self.__user + '/token', self.__new_token), headers=self.header,
                                   json=payload)
            if request.status_code == 429:
                seconds_to_wait = int(request.headers['Retry-After'])
                log.info('debug.log', f'HTTP 429 - Waiting {seconds_to_wait} seconds to retry')
                time.sleep(seconds_to_wait)
                return self.put_request(payload, url)
            if request.status_code == 200:
                return request.json()
        except requests.exceptions.RequestException as err:
            log.error('error.log', f'Error: {request.status_code} - {err}')

    def delete_request(self, url):
        log = logger.Logger()
        try:
            request = requests.delete(url, auth=(self.__user + '/token', self.__new_token), headers=self.header)
            if request.status_code == 429:
                seconds_to_wait = int(request.headers['Retry-After'])
                print(f'HTTP 429 - Waiting {seconds_to_wait} seconds to retry')
                time.sleep(seconds_to_wait)
                return self.delete_request(url)
            if request.status_code == 204:
                return request
        except requests.exceptions.RequestException as err:
            log.error('error.log', f'Error: {request.status_code} - {err}')
