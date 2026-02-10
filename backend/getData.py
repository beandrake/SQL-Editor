import requests
import json

# text YEAR should be replaced with a year from 2000 thru 2025
# Example: https://www-static.warframe.com/repos/WarframeUsageData2025.json
SOURCE_URL = r"https://www-static.warframe.com/repos/WarframeUsageDataYEAR.json"
#LOCAL_DATAFILE = r"data/WarframeUsageData2025.json"

# Format of timestamp: Mon, 24 Nov 2025 01:00:03 GMT
# See: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
TIMESTAMP_FORMAT = '%a, %d %b %Y %X %Z' 


def _get_url_for_year(year):
	return SOURCE_URL.replace("YEAR", str(year))


def get_and_parse_data(year):
	yearURL = _get_url_for_year(year)

	# download json as a string	
	payload = requests.get(yearURL)
	
	# convert string into objects
	arrayOfDictionaries = json.loads(payload.text)

	return arrayOfDictionaries


def _main():
	data = get_and_parse_data(2025)
	print(data)

if __name__ == '__main__':
	_main()