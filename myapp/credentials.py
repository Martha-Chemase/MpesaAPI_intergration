# import requests
# import json
# from requests.auth import HTTPBasicAuth
# from datetime import datetime
# import base64


# class MpesaC2bCredential:
#     consumer_key = 'XbWBSTnQayeUX4ZLXqNFyTKlPBfXWTylwlv8Q8nfUoXfby4X'
#     consumer_secret = 'vQzrGadk63vMDWgNnAg4XSUrqxfrM9slq5pvbvGLLFsgVfTvUWtsidLkpAx6aJb4'
#     api_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'


# class MpesaAccessToken:
#     r = requests.get(MpesaC2bCredential.api_URL,
#                      auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token["access_token"]


# class LipanaMpesaPpassword:
#     lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
#     Business_short_code = "174379"
#     OffSetValue = '0'
#     passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

#     data_to_encode = Business_short_code + passkey + lipa_time

#     online_password = base64.b64encode(data_to_encode.encode())
#     decode_password = online_password.decode('utf-8')

import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'XbWBSTnQayeUX4ZLXqNFyTKlPBfXWTylwlv8Q8nfUoXfby4X'
    consumer_secret = 'vQzrGadk63vMDWgNnAg4XSUrqxfrM9slq5pvbvGLLFsgVfTvUWtsidLkpAx6aJb4'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    @staticmethod
    def get_access_token():
        response = requests.get(
            MpesaC2bCredential.api_URL,
            auth=HTTPBasicAuth(
                MpesaC2bCredential.consumer_key,
                MpesaC2bCredential.consumer_secret,
            ),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()['access_token']


class LipanaMpesaPpassword:
    Business_short_code = "174379"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    @staticmethod
    def generate_password():
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = f"{LipanaMpesaPpassword.Business_short_code}{LipanaMpesaPpassword.passkey}{timestamp}"
        password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
        return timestamp, password


class MpesaSTKPush:
    def __init__(self, phone_number, amount):
        self.phone_number = phone_number
        self.amount = amount
        self.timestamp, self.password = LipanaMpesaPpassword.generate_password()
        self.access_token = MpesaAccessToken.get_access_token()

    def initiate_stk_push(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }

        payload = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": self.amount,
            "PartyA": self.phone_number,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": self.phone_number,
            "CallBackURL": "https://example.com/callback",
            "AccountReference": "Test123",
            "TransactionDesc": "Payment for testing",
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
        )

        response.raise_for_status()
        return response.json()