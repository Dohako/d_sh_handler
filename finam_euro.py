import requests
import bs4


def main(currency_name):
    if 'eur' in currency_name.lower():
        URL = 'https://www.finam.ru/quote/mosbirzha-valyutnyj-rynok/eur-rub-fix-1-sec/'
        # URL = 'https://www.moex.com/ru/issue.aspx?board=TQBR&code=MOEX'
        page = requests.get(URL)
        soup = bs4.BeautifulSoup(page.content)
        clear_data = soup.prettify()
        eur_to_rub = clear_data[clear_data.find('&quot;price&quot;:')+18:clear_data.find('&quot;price&quot;:')+25]
        answer = eur_to_rub
    else:
        answer = 'not implemented'
    return answer

if __name__ == '__main__':
    a = main('eur')
    print(a)