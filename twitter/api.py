import requests
from .config import TOKEN


class Response:
    def __init__(self, request: requests.Response) -> None:
        self.request = request
        self.success = self.request.status_code == 200
        self.data = request.json()


class API:
    def __init__(self, token: str) -> None:
        self.headers = {"Authorization": f"Bearer {token}",
                        "content-type": "application/json"}

    def get(self, url: str) -> Response:
        request = requests.get(url, headers=self.headers)
        return Response(request)


api = API(TOKEN)
