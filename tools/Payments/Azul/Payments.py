import ssl
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class Azul:
    def __init__(self):
        self.msg_send = ""
        self.msg_received = ""
        self.url = ""

    def OpenConnection(self, inputs):
        url = "https://pruebas.azul.com.do/Webservices/JSON/default.aspx"

        data = {
            "Channel":"EC",
            "Store":"99999991",
            "CardNumber":"1234567890123456",
            "Expiration":"201412",
            "CVC":"1234",
            "PosInputMode":"E-Commerce",
            "TrxType":"Sale",
            "Amount":"550050",
            "CurrencyPosCode":"$",
            "Payments":"1",
            "itbis": 000,
            "Plan":"0",
            "OriginalDate":"",
            "OriginalTrxTicketNr":"",
            "AuthorizationCode":"",
            "ResponseCode":"",
            "AcquirerRefData":"1",
            "RRN":None,
            "CustomerServicePhone":"",
            "OrderNumber":"",
            "ECommerceURL":""
        }


        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.request = Request(url, data=urlencode(data).encode('utf-8'))
        self.request.add_header("CONTENT_TYPE", "multipart/form-data;charset=utf-8")
        self.request.add_header("Auth1", "eps")
        self.request.add_header("Auth2", "eps")
        #self.request.add_header('X-Mashape-Key', '39036630010')

        self.request.add_header('Accept', 'application/json')
        self.request.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0")
        # check error
        response = urlopen(self.request, context=gcontext)
        print(response.read().decode())


if __name__ == '__main__':
    Azul().OpenConnection({})