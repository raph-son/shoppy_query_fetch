"""
Fetch customer email from query
"""
import json

import requests

class EmailFromQuery:
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
        req = requests.get(url, headers=headers)

        result = json.loads(req.text)

        for queries in result:
            if queries['id'] == id:
                result = {
                    "status": True,
                    "id": queries['id'],
                    "email": queries['email'],
                    "message": queries["message"]
                }
                return result
        # If id isn't found
        result = {
            "status": False,
            "id": id
        }
        return result

def main():
    email_from_query = EmailFromQuery()
    email_from_query.connect("vdYfTkp")

if __name__ == "__main__":
    main()