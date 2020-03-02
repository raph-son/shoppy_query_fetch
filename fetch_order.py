"""
Fetch order by email or ID
"""
import json

import requests

from requests.exceptions import ConnectionError

class ProductByEmailOrID:
    def __init__(self):
        self._URL = "https://shoppy.gg/api/v1/orders/"
        self._API_KEY = "rjJs9xF6YjDDmaGrGIQWGCHKcVDaV7GejhCjIqPuuDv2MS0fAW"    # Shoppy API key
        self._HEADERS = {
            "User-Agent": "QueryFetch",
            "Authorization": self._API_KEY
        }
        self._connection_error_result = {
            "status": False,
            "message": "<span style='color: red;'>Connection Error</span>"
        }

    def email(self, email):
        """
        search order by email

        email: str - email of the order
        """
        try:
            req = requests.get(self._URL, headers=self._HEADERS)
        except ConnectionError:
            result = self._connection_error_result
            return result

        return_list = []
        return_dict = {}
        result = json.loads(req.text)

        for value in result:
            if value["email"] == email:
                result_extracted = {
                    "id": value["id"],
                    "price": f"{value['currency']} {value['price']}",
                    "country": value["agent"]["geo"]["country"],
                    "ip": value["agent"]["geo"]["ip"],
                    "quantity": value["quantity"],
                    "product": value["product"]["title"],
                    "created_at": value["created_at"]
                }
                return_list.append(result_extracted)

        if len(return_list) > 0:
            result = {
                "status": True,
                "type": "ORDER EMAIL",
                "result": return_list
            }
            return result

        result = {
            "status": False,
            "message": f"order Email <span style='color: red;'>{email}</span> not found"
        }
        return result

    def id(self, id):
        """
        search order by ID

        id: str - id of the order
        """
        try:
            req = requests.get(self._URL, headers=self._HEADERS)
        except ConnectionError:
            result = self._connection_error_result
            return result
            
        result = json.loads(req.text)

        for value in result:
            if value["id"] == id:
                result_extracted = {
                    "status": True,
                    "type": "ORDER ID",
                    "result": {
                        "email": value["email"],
                        "price": f"{value['currency']} {value['price']}",
                        "country": value["agent"]["geo"]["country"],
                        "ip": value["agent"]["geo"]["ip"],
                        "quantity": value["quantity"],
                        "product": value["product"]["title"],
                        "created_at": value["created_at"]
                    }
                }
                return result_extracted

        result = {
            "status": False,
            "message": f"order ID <span style='color: red;'>{id}</span> not found"
        }
        return result
        


def main():
    product_by_email_id = ProductByEmailOrID()
    result = product_by_email_id.id("93c39394-6531-4349-8f44-50d832447e02")
    # result = product_by_email_id.email("jon.80110@gmail.com")
    print(result)
    

if __name__ == "__main__":
    main()