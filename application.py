from flask import Flask, render_template, request, jsonify
from fetch_query import EmailFromQuery

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    id = str(request.form.get("id"))

    email_from_query = EmailFromQuery()
    result = email_from_query.connect(id)
    return jsonify(result)

if __name__ == "__main__":
    app.run()