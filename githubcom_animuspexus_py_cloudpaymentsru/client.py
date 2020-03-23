import json
import base64

import urllib.request


class Client:
    def __init__(
            self,
            basic_auth_user: str = "",
            basic_auth_password: str = ""
    ):
        self.base_uri = 'https://api.cloudpayments.ru/'

        self.authorization_header = base64.b64encode(
            "{}:{}".format(basic_auth_user, basic_auth_password).encode(encoding="utf-8")
        ).decode(encoding="utf-8")

    def SendAsJSON(self, obj: dict, to: str) -> (dict, [Exception]):

        exceptions = list()

        try:
            json_string = json.dumps(obj)
        except Exception as err:
            exceptions.append(err)
            return None, exceptions

        req = None
        try:
            req = urllib.request.Request(
                self.base_uri + to,
                data=json_string.encode(encoding='utf-8'),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as err:
            exceptions.append(err)
            return None, exceptions

        req.add_header("Authorization", "Basic {}".format(self.authorization_header))

        for i in req.headers:
            print("header", i, req.headers[i])

        request_res = None
        try:
            request_res = urllib.request.urlopen(req)
        except Exception as err:
            exceptions.append(err)
            return None, exceptions

        if request_res != 200:
            exceptions.append(Exception("Response is not 200"))

        resp_data = ""
        try:
            resp_data = request_res.read()
        except Exception as err:
            exceptions.append(err)
            return None, exceptions

        resp_obj = None
        try:
            resp_obj = json.loads(resp_data)
        except Exception as err:
            exceptions.append(err)
            return None, exceptions

        if not type(resp_obj) == dict:
            exceptions.append(Exception("response is not JSON"))
            return None, exceptions

        return resp_obj, exceptions

    def Test(self) -> (dict, [Exception]):
        return self.SendAsJSON(dict(), "test")

    def PerformSingleIterationPayment(self, payment: dict) -> (dict, [Exception]):
        return self.SendAsJSON(payment, "payments/cards/charge")
