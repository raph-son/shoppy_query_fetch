import re

from flask import Flask, render_template, request, jsonify
from fetch_query import FetchQuery
from fetch_order import OrderByEmailOrID

app = Flask(__name__)

def decide_search_method(search):
        """
        Determine if search will be by ID (order ID or query ID) or email

        search: str - ID or email string
        """
        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        id_pattern = re.compile(r"[\w+-]*")
        query_id_pattern = re.compile(r"(^[a-zA-Z0-9]+$)")

        email_match = re.match(email_pattern, search)
        id_match = re.match(id_pattern, search)
        query_id_match = re.match(query_id_pattern, search)

        try:
            by_order_email = email_match.group(0)
            return "BY ORDER EMAIL"
        except AttributeError:
            try:
                by_query_id = query_id_match.group(0)
                return "BY QUERY ID"
            except AttributeError:
                by_order_id = id_match.group(0)
                return "BY ORDER ID"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    search_string = str(request.form.get("search"))
    search_string_type = decide_search_method(search_string)

    if search_string_type == "BY QUERY ID":
        fetch_query = FetchQuery()
        result = fetch_query.connect(search_string)
        return jsonify(result)
    if search_string_type == "BY ORDER EMAIL":
        order_by_email_id = OrderByEmailOrID()
        result = order_by_email_id.email(search_string)
        return jsonify(result)
    if search_string_type == "BY ORDER ID":
        order_by_email_id = OrderByEmailOrID()
        result = order_by_email_id.id(search_string)
        return jsonify(result)

if __name__ == "__main__":
    app.run()