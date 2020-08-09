from requests import Response


class CelsiusNetworkHTTPError(Exception):
    def __init__(self, response: Response):
        self.url = response.url
        self.status_code = response.status_code
        self.response = response
        self.message = response.json()["message"]

        super().__init__(f'The request failed with '
                         f'HTTP status code {self.status_code}: {self.message}')
