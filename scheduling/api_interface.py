import requests


class APIException(Exception):
    pass


class APIServer(object):
    def __init__(self, base_url):
        self.base = base_url

    def get(self, resource, data=None):
        with requests.Session() as s:
            resp = s.get('{}{}'.format(self.base, resource), data=data)

        return resp.json(), resp.status_code

    def get_configuration(self, key):
        config_url = '/configuration/{}'.format(key)

        resp, status = self.get(config_url)

        if status != 200:
            self._unexpected_status(status, config_url)

        if key in resp.json():
            return resp.json()[key]

    def get_scenes_to_process(self, limit, user, priority, product_type):
        params = ['record_limit={}'.format(limit) if limit else None,
                  'for_user={}'.format(user) if user else None,
                  'request_priority={}'.format(priority) if priority else None,
                  'product_types={}'.format(product_type) if product_type else None]

        query = '&'.join([q for q in params if q])

        url = '/production-api/v0/products?{}'.format(query)

        resp, status = self.get(url)

        if status != 200:
            self._unexpected_status(status, url)

        return resp.json()

    def handle_orders(self):
        url = '/production-api/v0/handle-orders'

        resp, status = self.get(url)

        if status != 200:
            self._unexpected_status(status, url)

        return resp.json()

    @staticmethod
    def _check_status(expected, received):
        if expected == received:
            return True
        else:
            return False

    @staticmethod
    def _unexpected_status(code, url):
        raise Exception('Received unexpected status code{}\n'
                        'for URL {}'.format(code, url))

    def test_connection(self):
        with requests.Session() as s:
            resp = s.get(self.base)

        if resp.status_code == 200:
            return True

        return False


def api_connect(url):
    api = APIServer(url)

    if not api.test_connection():
        return None

    return api
