from dotenv import load_dotenv
import os
import base64
import logging
import requests

class SkinPort:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.authorization_string = None

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def authenticate(self) -> None:
        if self.client_id and self.client_secret:
            client_data = f"{self.client_id}:{self.client_secret}"
            encoded_data = str(base64.b64encode(client_data.encode("utf-8")), "utf-8")
            authorization_string = f"Basic {encoded_data}"

            self.authorization_string = authorization_string
        
        else:
            self.logger.error('CLIENT_ID or CLIENT_SECRET not found')

    def get_transactions(self, page):
        if self.authorization_string:
            r = requests.get("https://api.skinport.com/v1/account/transactions", 
                headers={
                "authorization": self.authorization_string
                }, 
                params={
                "page": page,
                "limit": 100,
                "order": "desc"
                }).json()
            return r
        else:
            self.logger.error("No Authorization string found!")