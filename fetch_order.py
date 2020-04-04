"""
Fetch order by email or ID
"""
import json

import requests

from requests.exceptions import ConnectionError

class OrderByEmailOrID:
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
        Searching by email require an extra search of individual order(by ID) that belongs to the emails

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
                # Make extra request for each ID to retrieve order details
                req = requests.get(f"{self._URL}{value['id']}", headers=self._HEADERS)
                result = json.loads(req.text)
                try:
                    order_details = result["accounts"][0]["account"]
                except IndexError:
                    order_details = ""

                coupon_raw = value["coupon"]
                coupon = ""
                if len(coupon_raw) == 0:
                    coupon += "No coupon"
                else:
                    for value in coupon_raw:
                        coupon += f"{value} "
                result_extracted = {
                    "id": value["id"],
                    "price": f"{value['currency']} {value['price']}",
                    "country": value["agent"]["geo"]["country"],
                    "ip": value["agent"]["geo"]["ip"],
                    "coupon": coupon,
                    "quantity": value["quantity"],
                    "product": value["product"]["title"],
                    "details": order_details,
                    "gateway": value["gateway"],
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
        Searching by ID is a constant time (no looping of result by client)

        id: str - id of the order
        """
        try:
            req = requests.get(f"{self._URL}{id}", headers=self._HEADERS)
        except ConnectionError:
            result = self._connection_error_result
            return result
            
        result = json.loads(req.text)
        try:
            order_details = result["accounts"][0]["account"]
        except IndexError:
            order_details = ""
        coupon_raw = result["coupon"]
        coupon = ""
        if len(coupon_raw) == 0:
            coupon += "No coupon"
        else:
            for result in coupon_raw:
                coupon += f"{result} "
        result_extracted = {
            "status": True,
            "type": "ORDER ID",
            "result": {
                "email": result["email"],
                "price": f"{result['currency']} {result['price']}",
                "country": result["agent"]["geo"]["country"],
                "ip": result["agent"]["geo"]["ip"],
                "coupon": coupon,
                "quantity": result["quantity"],
                "product": result["product"]["title"],
                "details": order_details,
                "gateway": result["gateway"],
                "created_at": result["created_at"]
            }
        }
        return result_extracted

        result = {
            "status": False,
            "message": f"order ID <span style='color: red;'>{id}</span> not found"
        }
        return result
        


def main():
    order_by_email_id = OrderByEmailOrID()
    result = order_by_email_id.id("e52c824b-604a-4c6d-b566-0246d6acb843")
    #result = order_by_email_id.email("thecoolabbas@gmail.com")
    print(result)
    

if __name__ == "__main__":
    main()