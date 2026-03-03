import requests
import json

# text YEAR should be replaced with a year from 2020 thru 20XX
# Example: https://www-static.warframe.com/repos/WarframeUsageData2025.json
SOURCE_URL = r"https://www-static.warframe.com/repos/WarframeUsageDataYEAR.json"
#LOCAL_DATAFILE = r"data/WarframeUsageData2025.json"

# Format of timestamp: Mon, 24 Nov 2025 01:00:03 GMT
# See: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
TIMESTAMP_FORMAT = '%a, %d %b %Y %X %Z' 


def get_and_parse_data(year):
	"""
	Pulls usage data from the URL and coverts the json into a list of dicts.
	Returns the list.
	"""
	# replace placeholder in URL with our actual year
	yearURL = SOURCE_URL.replace("YEAR", str(year))

	# download json as a string	
	payload = requests.get(yearURL)
	
	# convert string into objects
	arrayOfDictionaries = json.loads(payload.text)

	return arrayOfDictionaries


### Testing ###
def _main():
	data = get_and_parse_data(2025)
	print(data)

if __name__ == '__main__':
	_main()