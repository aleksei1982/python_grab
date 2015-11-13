__author__ = 'rav'
import re
import urllib.request
from bs4 import BeautifulSoup
import csv

BASE_URL = 'http://weblancer.net/projects/'


def get_html(url):
    #  proxies = {'http': 'http://127.0.0.1:3128'}
    # response = urllib.request.urlopen(url, proxies)

    proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:3128', 'https': '127.0.0.1:3128'})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url)
    return response.read()


def page_count(html):
    soup = BeautifulSoup(html, "lxml")
    pagination = soup.find('ul', 'pagination')
    stroka = str(pagination.find_all('a')[-1])

    # print(stroka)
    # [int(s) for s in stroka.split if s.isdigit()]
    # for s in stroka:
    #    if s.
    # print(s)

    # id=re.sub("\D", "", stroka)
    # print('id = ',id)
    return ''.join(filter(lambda x: x.isdigit(), stroka))


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', 'container-fluid cols_table show_visited')
    projects = []
    for row in table.find_all('div', 'row'):
        cols = row.find_all('div', 'col-sm-7')
        category = row.find_all('div', 'text-muted')
        price = row.find_all('div', 'col-sm-2 amount title')
        zayavki = row.find_all('div', 'col-sm-3 text-right text-nowrap hidden-xs')
        # 'price':price.a.text
        projects.append({
            'title': cols[0].a.text, 'categories': category[0].a.text, 'price': price[0].text.strip(),
            'kol-vo zayavok': zayavki[0].text.strip()
        })
    return projects


    # for project in projects:
    #    print(project)
    # print(table.prettify())
    # print(rows)
    # for rows in table

#
def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('проект', 'категории', 'цена', 'заявки'))
        for project in projects:
            writer.writerow(
                (project['title'], ''.join(project['categories']), project['price'], project['kol-vo zayavok']))


def main():
    page_c = page_count(get_html(BASE_URL))
    print('всего найдено страниц %s' % page_c)
    projects1 = []
    for page in range(1, int(page_c)):
        print('Парсинг %d%%' % (page / int(page_c) * 100))
        parse(get_html(BASE_URL + '?page=%d' % page))
        projects1.extend(parse(get_html(BASE_URL + '?page=%d' % page)))
    # parse(get_html(BASE_URL+'?page=%d' % 150))


    for project in projects1:
        print(project)
        # print(page_count(get_html(BASE_URL)))
        # parse(get_html('http://weblancer.net/projects/ '))
    save(projects1,r'c:\temp\project.csv')

if __name__ == '__main__':
    main()



# def main():
#   print(get_html(r'http://ya.ru/'))
