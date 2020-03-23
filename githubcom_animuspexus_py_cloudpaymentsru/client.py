import json
import urllib.request


class Client:

    def __init__(self, public_id: str = "", api_secret: str = "", anonymous_login: bool = False):
        self.base_uri = 'https://api.cloudpayments.ru/'

        self.public_id = public_id
        self.api_secret = api_secret

    def SendAsJSON(self, obj: dict, to: str) -> (dict, Exception):

        json_string = ""

        try:
            json_string = json.dumps(obj)
        except Exception as err:
            return None, err

        request_res = None

        try:
            request_res = urllib.request.urlopen(self.base_uri + to, data=json_string)
        except Exception as err:
            return None, err

        if request_res != 200:
            return None, Exception

        resp_data = ""
        try:
            resp_data = request_res.read()
        except Exception as err:
            return None, err

        resp_obj = None
        try:
            resp_obj = json.loads(resp_data)
        except Exception as err:
            return None, err

        if not type(resp_obj) == dict:
            return None, Exception("ersponse is not JSON")

        return None

    def Test(self):
        self.SendAsJSON(dict(), "test")

    def PerformSingleIterationPayment(self, payment: dict):
        self.SendAsJSON(payment, "payments/cards/charge")
