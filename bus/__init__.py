import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import warnings

warnings.simplefilter('ignore', InsecureRequestWarning)

URL = "https://www.stcp.pt/pt/itinerarium/soapclient.php"

SCHEDULE_CHECKS = [
    { 
        "stop": "AML3",
        "lines": [205],
        "hash": "73rrHNI-jqSXT5EVlLcCCCZXt4ThmOLcZqpJD_6qIFE"
    },
    {
        "stop": "TLHR1",
        "lines": [600, 704],
        "hash": "XBvI-jkLEsHXkOfd1lfhbfnOPd9mF31yQVddUIgEbH8"
    }
]

def fetch_next_buses():
    next_buses = []
    for schedule in SCHEDULE_CHECKS:
        for line in schedule['lines']:
            querystring = {"codigo": schedule['stop'], "linha": line, "hash123": schedule['hash'] }
            response = requests.request("GET", URL, params=querystring, verify=False)
            sched_results = [ { **entry, 'stop': schedule['stop']} for entry in parse_content(response.text)]
            next_buses.extend(sched_results)
    sorted_next_buses = sorted(next_buses, key=lambda bus: -1 if bus['wait_time'] == '' else int(bus['wait_time'].replace('min', '')))
    return sorted_next_buses[:5]

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

def format(bus):
    return f'🚌 Line {bus["line"]} 🚏 {bus["stop"]} ⏳ {bus["wait_time"]}  ({bus["predicted"]})'

def display():
    next_buses = fetch_next_buses()
    print("\n".join([format(bus) for bus in next_buses]))
 
