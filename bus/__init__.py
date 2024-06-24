import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import warnings

warnings.simplefilter('ignore', InsecureRequestWarning)

URL = "https://www.stcp.pt/pt/itinerarium/soapclient.php"

SCHEDULE_CHECKS = {
    "TLHR1": [600]
}

# No idea what this is, but request needs it, maybe for rate-limiting?
HASH = "XBvI-jkLEsHXkOfd1lfhbfnOPd9mF31yQVddUIgEbH8"
 
def fetch_next_buses():
    next_buses = []
    for stop, lines in SCHEDULE_CHECKS.items():
        for line in lines:
            querystring = {"codigo": stop, "linha": line, "hash123": HASH }
            response = requests.request("GET", URL, params=querystring, verify=False)
            next_buses.extend(parse_content(response.text))
    return next_buses

def parse_content(content):
    try:
        parsed = []
        bs = BeautifulSoup(content, 'html.parser')
        table = bs.find('table', {'id': 'smsBusResults'})
        rows = table.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            parsed.append({
                'line': cells[0].text.strip().split()[0],
                'predicted': cells[1].text.strip(),
                'wait_time': cells[2].text.strip()
            })
        return parsed
    except Exception as err:
        print('Error connecting to itinerarium API', err)
        return []

def format(forecasts):
    return '\n'.join([
        f'🚌 Line {bus["line"]}  ⏳ {bus["wait_time"]}  ({bus["predicted"]})'
        for bus in forecasts
    ])

def display():
    w = fetch_next_buses()
    print(format(w))
 
