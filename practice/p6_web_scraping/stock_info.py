"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

from operator import itemgetter
import requests as requests

from tabulate import tabulate
from bs4 import BeautifulSoup

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.84 Safari/537.36"}

table1 = []
table2 = []
table3 = []


def get_companies():
    response = requests.get("https://finance.yahoo.com/most-active")
    assert response.status_code == 200

    most_active_soup = BeautifulSoup(response.text, 'lxml')
    body = most_active_soup.find("tbody")
    companies = body.contents
    return companies


def _fill_table1(company_name, company_code):
    company_profile_url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(company_code, company_code)
    response = requests.get(company_profile_url, headers=HEADERS)
    assert response.status_code == 200

    company_profile_soup = BeautifulSoup(response.text, 'lxml')
    ceos = company_profile_soup.findAll('tr')
    summary = company_profile_soup.find("div", {"class": "asset-profile-container"})
    summary_col1 = summary.div.p
    summary_col2 = summary.div.p.nextSibling
    company_country = summary_col1.contents[4]
    company_n_emp = summary_col2.contents[10].text
    ceos_dict = {}
    for ceo in ceos:
        name = ceo.contents[0].text
        age = ceo.contents[4].text
        if age.isdigit():
            ceos_dict.update({age: name})
    min_age = min(ceos_dict, key=ceos_dict.get)
    yongest_ceo_in_company = ceos_dict.get(min_age)
    table1.append([company_name, company_code, company_country, company_n_emp, yongest_ceo_in_company, min_age])
    return table1

def _fill_table2(company_name, company_code):
    company_stastic_url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(company_code, company_code)
    response = requests.get(company_stastic_url, headers=HEADERS)
    assert response.status_code == 200

    company_stastic_soup = BeautifulSoup(response.text, 'lxml')
    summary = company_stastic_soup.findAll("td")
    week_change = total_cash = None
    for i in summary:
        if i.text == "52-Week Change 3":
            week_change = i.nextSibling.text
        if i.text == "Total Cash (mrq)":
            total_cash = i.nextSibling.text

    return table2.append([company_name, company_code, week_change, total_cash])


def fill_table3():
    response = requests.get("https://finance.yahoo.com/quote/BLK/holders?p=BLK", headers=HEADERS)
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.findAll("tbody")
    for tr in tbody[1:]:
        for td in tr:
            shares = td.contents[1].text
            date_reported = td.contents[2].text
            perc_out = td.contents[3].text
            value = td.contents[4].text

            table3.append(["Blackrock Inc", "BLK", shares, date_reported, perc_out, value])

    return table3


def main():
    TABLE1_HEADERS = [['Name', 'Code', 'Country', 'Employees', 'CEO Name', 'CEO Year Born']]
    TABLE2_HEADERS = [['Name', 'Code', '52-Week Change', 'Total Cash']]
    TABLE3_HEADERS = [['Name', 'Code', 'Shares', 'Date Reported', '% Out', 'Value']]

    companies = get_companies()

    for company in companies:
        company_code = company.contents[0].text
        company_name = company.contents[1].text
        print(company_name)

        _fill_table1(company_name, company_code)
        _fill_table2(company_name, company_code)

    table3 = fill_table3()

    table1_sorted = (sorted(table1, key=itemgetter(-1), reverse=True))[:5]  # sort by yangest ceo
    full_table1 = TABLE1_HEADERS + table1_sorted
    print(tabulate(full_table1, headers='firstrow', tablefmt='fancy_grid',
                   colalign=("center", "center", "center", "center", "center", "center",)))

    table2_sorted = (sorted(table2, key=itemgetter(-1), reverse=True))[:10]
    full_table2 = TABLE2_HEADERS + table2_sorted
    print(tabulate(full_table2, headers='firstrow', tablefmt='fancy_grid',
                   colalign=("center", "center", "center", "center",)))

    table3_sorted = (sorted(table3, key=itemgetter(-1), reverse=True))[:10]
    full_table3 = TABLE3_HEADERS + table3_sorted
    print(tabulate(full_table3, headers='firstrow', tablefmt='fancy_grid',
                   colalign=("center", "center", "center", "center", "center", "center",)))


if __name__ == "__main__":
    main()
