import requests
import bs4
import json

BASE_URL = 'http://www.washington.edu/students/crscat/'


def get_urls():
    urls = []
    r = requests.get(BASE_URL)
    soup = bs4.BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        a = str(link.get('href'))
        if not (a.startswith('http') or a.startswith('/')) and a.endswith('html'):
            urls.append(a)
    return urls


def get_courses(urls):
    for url in urls:
        r = requests.get(BASE_URL+url)
        soup = bs4.BeautifulSoup(r.text)
        for text in soup.find_all('b'):
            format_text(text.text)


def format_text(text):
    parts = text.split()
    dept = parts[0]
    num = parts[1]
    fullname = dept.tolower()+num
    title = text[len(dept)+len(num)+1:text.index('(')]
    record(fullname, dept, num, title)


def record(fullname, dept, num, title):
    payload = {'fullname': fullname, 'dept': dept, 'num': num, 'title': title}
    r = requests.post('52.27.91.71/update', json=json.dumps(payload))
