from urllib.request import urlopen
from bs4 import BeautifulSoup

def url_scrape():
    url = "https://www.inherentresolve.mil/Releases/Strike-Releases/"
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # gets full list of urls
    link_list = []
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            link_list.append(link.attrs['href'])

    # gets only report urls
    reports = [s for s in link_list if "/Portals/14" in s]

    # cleans up urls
    reports_updated = []
    for x in reports:
        if 'https' not in x:
            n = 'https://www.inherentresolve.mil' + x
            n.replace(" ", "%20")
            reports_updated.append(n)
        elif 'https' in x:
            n = x.replace(" ", "%20")
            reports_updated.append(n)

    return reports_updated
