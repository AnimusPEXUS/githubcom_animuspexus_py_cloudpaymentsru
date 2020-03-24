import requests
import base64


class Client:
    def __init__(
            self,
            basic_auth_user: str = "",
            basic_auth_password: str = ""
    ):
        self.base_uri = 'https://api.cloudpayments.ru/'

        self.basic_auth_user = basic_auth_user
        self.basic_auth_password = basic_auth_password

        self.authorization_header = base64.b64encode(
            "{}:{}".format(basic_auth_user, basic_auth_password).encode(encoding="utf-8")
        ).decode(encoding="utf-8")

    def SendAsJSON(self, obj: dict, to: str) -> (dict, [Exception]):

        exceptions = list()

        try:
            request_res = requests.request(
                method="POST",
                url=self.base_uri + to,
                auth=(self.basic_auth_user, self.basic_auth_password,),
                json=obj,
            )
        except Exception as err:
            exceptions.append(err)

        if request_res.status_code != 200:
            exceptions.append(Exception("response is not 200"))

        try:
            resp_obj = request_res.json()
        except Exception as err:
            exceptions.append(err)
            return None, exceptions

        if not type(resp_obj) == dict:
            exceptions.append(Exception("response JSON is invalid"))

        return resp_obj, exceptions

    def Test(self) -> (dict, [Exception]):
        return self.SendAsJSON(dict(), "test")

    def PerformSingleIterationPayment(self, payment: dict) -> (dict, [Exception]):
        return self.SendAsJSON(payment, "payments/cards/charge")
