from flask import Flask, render_template, request, send_from_directory
from utils import get_html_file, get_tables, convert_html_table_to_dict, saves_dicts_to_excel
import io

app = Flask(__name__, static_folder="static")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/file.xlsx", methods=["POST"])
def makeExcel():
    url = request.form["text"]
    file = get_html_file(url)
    tables = get_tables(file)
    if len(tables) == 0:
        return "No Table Found on the page"
    table_dicts = []
    for table in tables:
        table_dicts.append(convert_html_table_to_dict(table))
    saves_dicts_to_excel(table_dicts, "static/table.xlsx")
    return send_from_directory("static", "table.xlsx")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
