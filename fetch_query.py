"""
Fetch customer query
"""
import json

import requests

from requests.exceptions import ConnectionError

class FetchQuery:
    def __init__(self):
        self._API_KEY = "rjJs9xF6YjDDmaGrGIQWGCHKcVDaV7GejhCjIqPuuDv2MS0fAW"    # Shoppy API key

    def connect(self, id):
        """
        Make http request for query

        id: str - ID of the query
        """
        headers = {
            "User-Agent": "QueryFetch",
            "Authorization": self._API_KEY
        }
        url = "https://shoppy.gg/api/v1/queries/"
        try:
            req = requests.get(f"{url}{id}", headers=headers)
        except ConnectionError:
            result = {
                "status": False,
                "message": "<span style='color: red;'>Connection Error</span>"
            }
            return result
        print(req.text)
        queries = json.loads(req.text)

        result = {
            "status": True,
            "type": "QUERY ID",
            "id": queries['id'],
            "email": queries['email'],
            "message": queries["message"]
        }
        return result
        # If id isn't found
        result = {
            "status": False,
            "message": f"query ID <span style='color: red;'>{id}</span> not found"
        }
        return result

def main():
    fetch_query = FetchQuery()
    fetch_query.connect("vdYfTkp")

if __name__ == "__main__":
    main()