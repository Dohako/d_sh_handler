from requests import get
from bs4 import BeautifulSoup
from pycbrf import ExchangeRates
from datetime import datetime

URL = 'https://www.finam.ru/quote/mosbirzha-valyutnyj-rynok/eur-rub-fix-1-sec/'
# URL = 'https://www.moex.com/ru/issue.aspx?board=TQBR&code=MOEX'


def get_pycbrf_course(currency_name):
    rates = ExchangeRates(datetime.now().strftime("%Y-%m-%d"))
    # currency_name = self.currency_list_correct[self.currency_list.index(currency)]
    pycbrf_todays_currency = rates[currency_name].value
    return pycbrf_todays_currency


def scrap_currency_from_page(currency_name, url=URL):
    if 'eur' in currency_name.lower():
        page = get(url)
        soup = BeautifulSoup(page.content)
        clear_data = soup.prettify()
        eur_to_rub = clear_data[clear_data.find('&quot;price&quot;:') + 18:clear_data.find('&quot;price&quot;:') + 25]
        answer = eur_to_rub
    else:
        answer = 'not implemented'
    return answer


if __name__ == '__main__':
    # a = scrap_currency_from_page('eur')
    a = get_pycbrf_course('EUR')
    print(a)
