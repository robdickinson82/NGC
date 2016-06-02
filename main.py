# -*- coding: utf-8 -*-
import requests
import datetime
from requests.auth import HTTPBasicAuth
from config import NGC_USERNAME, NGC_PWORD, NGC_URL, NGC_CA_BUNDLE

risk_levels = {
    'HIGH': ["sanction", "pep-class-1", "pep-class-2"],
    'LOW': ["sanction"],
}


class NGC(object):

    def __init__(self,
                 uri='https://api-test.ngcprograms.com/v2/',
                 username=None,
                 password=None):
        self.uri = uri
        self.auth = (username, password)

    def __call__(self, path, type_=None, data=None, params=None):
        req = getattr(requests, type_, requests.get)
        kwargs = {'auth': self.auth, 'verify': NGC_CA_BUNDLE}
        if data is not None:
            kwargs['json'] = data
        res = req(self.uri + path, params=params, **kwargs)
        #print(res.text)
        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            print(res.json())
            res.raise_for_status()

    def _ping(self):
        return self('ping', type_='get')

    def ping(self, **kwargs):

        #risk_category = kwargs.pop('risk_category')
        #default_types = risk_levels.get('HIGH', [])
        #kwargs['types'] = risk_levels.get(risk_category, default_types)

        #entity = search_entity(**kwargs)

        return self._ping()

    def _vendor(self):
        return self('vendor', type_='get')

    def vendor(self, **kwargs):
        return self._vendor()

    def _inventory(self, **kwargs):
        if kwargs.get('vendor_code'):
            path = 'vendor/' + kwargs['vendor_code'] + '/inventory'
        else:
            path = 'inventory'
        return self(path, type_='get')

    def inventory(self, **kwargs):
        return self._inventory(**kwargs)

    def _account_balance(self):
        return self('account_balance', type_='get')

    def account_balance(self, **kwargs):
        return self._account_balance()

    def _order_card(self, **kwargs):
        delivery = {}
        if kwargs.get('email_address'):
            delivery['deliveryType'] = 'email'
            delivery['recipient'] = {}
            delivery['recipient']['email'] = kwargs.get('email_address')
            if kwargs.get('first_name'):
                delivery['recipient']['firstName'] = kwargs.get('first_name')
            if kwargs.get('last_name'):
                delivery['recipient']['lastName'] = kwargs.get('last_name')
            kwargs.pop('email_address')
        else:
            delivery['deliveryType'] = 'api'

        kwargs['delivery'] = delivery

        return self('giftcard', type_='post', data=kwargs)

    def order_card(self, **kwargs):
        return self._order_card(**kwargs)

    def _get_card_details(self, **kwargs):
        if kwargs.get('cardCode'):
            params = None
            path = 'giftcard/' + kwargs['cardCode'] + '/'
        else:
            params = kwargs
            path = 'giftcard'
        return self(path, type_='get', params=params)

    def get_card_details(self, **kwargs):
        return self._get_card_details(**kwargs)

api = NGC(uri=NGC_URL,
          username=NGC_USERNAME,
          password=NGC_PWORD)


def test_ping():
    response = api.ping()


def test_order_card_with_api():
    response = api.order_card(auditNumber='Rob-2WATEGBP-'
                              + datetime.datetime.now()
                              .strftime("%Y%m%d%H%M%S%f"),
                              purchaseOrderNumber='PO-Rob001',
                              vendorCode='2WATEGBP',
                              cardAmount='10.00',
                              currency='GBP')

    print (response)
    return


def test_order_card_with_email_address():
    response = api.order_card(auditNumber='Rob-2WATEGBP-'
                              + datetime.datetime.now()
                              .strftime("%Y%m%d%H%M%S%f"),
                              purchaseOrderNumber='PO-Rob001',
                              vendorCode='2WATEGBP',
                              cardAmount='10.00',
                              currency='GBP',
                              email_address='rob@osper.com')

    print(response)
    return


def test_get_card_details_using_audit_number():
    response = api.get_card_details(auditNumber=
                                    'Rob-2WATEGBP-20160602202652438000')
    print(response)
    return


def test_get_card_details_using_card_code():
    response = api.get_card_details(cardCode=
                                    'JbHkLpDBh36ipNiuimdqFB9MEMvaqWLcvh0v7fMSyu653TKW2LjrpM31hFrEtrz4')
    print(response)
    return


def test_get_card_details_using_both_card_code_and_audit_number():
    response = api.get_card_details(cardCode=
                                    'JbHkLpDBh36ipNiuimdqFB9MEMvaqWLcvh0v7fMSyu653TKW2LjrpM31hFrEtrz4',
                                    auditNumber='abc123')
    print(response)
    return

test_order_card_with_email_address()
#test_order_card_with_api()
#test_get_card_details_using_audit_number()
#test_get_card_details_using_card_code()
