import requests
import bs4

BASE_URL = 'http://www.washington.edu/students/crscat/'


def get_urls():
    urls = set()
    r = requests.get(BASE_URL)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    for link in soup.find_all('a'):
        a = str(link.get('href'))
        if not (a.startswith('http') or a.startswith('/')) and a.endswith('html'):
            urls.add(a)
    return urls


def get_courses(urls):
    for url in urls:
        r = requests.get(BASE_URL+url)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        for text in soup.find_all('b'):
            format_text(text.text, url)


def format_text(text, url):
    parts = text.split()
    dept = parts[0]
    candidate = parts[1]
    try:
        num = int(candidate)
    except ValueError:
        dept = dept + ' ' + candidate
        num = int(parts[2])

    fullname = dept.lower().replace(' ', '')+str(num)
    title = text[len(dept)+len(str(num))+1:text.index('(')]
    description = BASE_URL+url+'#'+fullname
    payload = {'fullname': fullname, 'dept': dept, 'number': num, 'title': title.strip(),
               'description': description}
    record(payload)


def record(payload):
    r = requests.post('http://52.27.91.71/api/', data=payload)
    if r.status_code != 201:
        print(payload, r.status_code)


def main():
    get_courses(get_urls())

main()
