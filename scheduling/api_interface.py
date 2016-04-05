import requests


class APIException(Exception):
    """
    Handle exceptions thrown by the APIServer class
    """
    pass


class APIServer(object):
    """
    Provide a more straightforward way of handling API calls
    without changing the cron jobs significantly
    """
    def __init__(self, base_url):
        self.base = base_url

    def get(self, resource=None, data=None, status=None):
        """
        Make a call into the API

        Args:
            status: Expected http status
            resource: API resource to touch
            data: payload to send in

        Returns: response and status code

        """
        if resource and resource[0] == '/':
            url = '{}{}'.format(self.base, resource)
        elif resource:
            url = '{}/{}'.format(self.base, resource)
        else:
            url = self.base

        resp = requests.get(url, data=data)

        if status and resp.status_code != status:
            self._unexpected_status(resp.status_code, url)

        return resp.json(), resp.status_code

    def get_configuration(self, key):
        """
        Retrieve a configuration value

        Args:
            key: configuration key

        Returns: value if it exists, otherwise None

        """
        config_url = '/configuration/{}'.format(key)

        resp, status = self.get(config_url, 200)

        if key in resp.json():
            return resp.json()[key]

    def get_scenes_to_process(self, limit, user, priority, product_type):
        """
        Retrieve scenes/orders to begin processing in the system

        Args:
            limit: number of products to grab
            user: specify a user
            priority: depricated, legacy support
            product_type: landsat and/or modis

        Returns: list of dicts
        """
        params = ['record_limit={}'.format(limit) if limit else None,
                  'for_user={}'.format(user) if user else None,
                  'request_priority={}'.format(priority) if priority else None,
                  'product_types={}'.format(product_type) if product_type else None]

        query = '&'.join([q for q in params if q])

        url = '/production-api/v0/products?{}'.format(query)

        resp, status = self.get(url, 200)

        return resp

    def handle_orders(self):
        """
        Sends the handle_orders command to the API

        Returns: True if successful
        """
        url = '/production-api/v0/handle-orders'

        resp, status = self.get(url, 200)

        return resp

    @staticmethod
    def _unexpected_status(code, url):
        """
        Throw exception for an unhandled http status

        Args:
            code: http status that was received
            url: URL that was used
        """
        raise Exception('Received unexpected status code: {}\n'
                        'for URL: {}'.format(code, url))

    def test_connection(self):
        """
        Tests the base URL for the class
        Returns: True if 200 status received, else False
        """
        resp, status = self.get()

        if status == 200:
            return True

        return False


def api_connect(url):
    """
    Simple lead in method for using the API connection class

    Args:
        url: base URL to connect to

    Returns: initialized APIServer object if successful connection
             else None
    """
    api = APIServer(url)

    if not api.test_connection():
        return None

    return api
