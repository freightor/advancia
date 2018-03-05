import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def clean(table_data):
    table_data = table_data.string.strip().replace("First ", "")
    table_data = table_data.replace("NIL", "0")
    table_data = table_data.replace("Next ", "")
    table_data = table_data.replace("Exceeding ", "")
    table_data = table_data.replace(",", "")
    return Decimal(table_data).quantize(Decimal("0.01"))


def get_tax_data(url):
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    monthly_table = soup.find_all("table")[1]
    tax_dict = []
    for row in monthly_table.tbody.find_all("tr")[1:]:
        tds = row.findChildren("td")
        tax_dict.append([clean(tds[0]), clean(tds[1])/100])
    return tax_dict


def get_tax(amount, tax_rates):
    tax = 0
    for rate in tax_rates[:-1]:
        if amount <= rate[0]:
            tax += amount*rate[1]
            amount -= amount
            break
        else:
            tax += rate[0]*rate[1]
            amount -= rate[0]
    tax += amount*tax_rates[-1][1]
    return Decimal(tax).quantize(Decimal("0.01"))


if __name__ == "__main__":
    print(get_tax(3700, get_tax_data(
        "http://www.gra.gov.gh/index.php/tax-information/income-tax")))
