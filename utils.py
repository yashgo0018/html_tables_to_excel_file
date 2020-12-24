import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_html_file(url):
    r = requests.get(url)
    return r.content


def get_tables(page):
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find_all("table")


def convert_html_table_to_dict(table):
    table_dict = {}
    headings = table.find_all("th")
    headings = list(map(lambda x: x.text, headings))
    for heading in headings:
        table_dict[heading] = []
    for row in table.find_all("tr")[1:]:
        values = row.find_all("td")
        for i in range(len(headings)):
            table_dict[headings[i]].append(values[i].text.replace("\xa0", ""))
    return table_dict


def saves_dicts_to_excel(dicts, filename):
    with pd.ExcelWriter(filename) as writer:
        for i in range(len(dicts)):
            df = pd.DataFrame(dicts[i])
            df.to_excel(writer, index=False,
                        sheet_name=f"Sheet_number_{i + 1}")
