import requests
import bs4

BASE_URL = 'http://www.washington.edu/students/crscat/'
ERRORS = []


def get_urls():
    urls = []
    r = requests.get(BASE_URL)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    for link in soup.find_all('a'):
        a = str(link.get('href'))
        if not (a.startswith('http') or a.startswith('/')) and a.endswith('html'):
            urls.append(a)
    return urls


def get_courses(urls):
    for url in urls:
        r = requests.get(BASE_URL+url)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        for text in soup.find_all('b'):
            format_text(text.text)


def format_text(text):
    parts = text.split()
    dept = parts[0]
    candidate = parts[1]
    try:
        num = int(candidate)
    except:
        dept = dept + ' ' + candidate
        num = int(parts[2])

    fullname = dept.lower()+str(num)
    title = text[len(dept)+len(str(num))+1:text.index('(')]
    payload = {'fullname': fullname, 'dept': dept.replace(' ', ''), 'number': num, 'title': title.strip()}
    record(payload)


def record(payload):
    r = requests.post('http://52.27.91.71/post/', data=payload)
    if r.status_code != 201:
        print(payload, r.status_code)
        ERRORS.append(payload)


def main():
    get_courses(get_urls())
    file_ = open('error.txt', 'w')
    for payload in ERRORS:
        file_.write("%s\n" % payload)

main()
