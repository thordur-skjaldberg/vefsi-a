from flask import Flask, render_template, request
import usda_api

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def search():
    result = None
    if request.method == "POST":
        query = request.form["query"]
        result = usda_api.search_and_report(query)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)