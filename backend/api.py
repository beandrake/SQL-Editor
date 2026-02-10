import time
from flask import Flask, request

from usageStats import UsageStats
from getData import get_and_parse_data


MIN_YEAR = 2020
MAX_YEAR = 2025
MASTERY_RANK_MAX = 36
TABLE_NAMES = ["warframe", "primary_weapon", "secondary_weapon", "melee_weapon"]
JSON_NAMES = ["Warframe", "Primary", "Secondary", "Melee"]


# initialize database table as global variable
stats = UsageStats(MASTERY_RANK_MAX, TABLE_NAMES)

def initialize_records():
	# load data
	for year in range(MIN_YEAR, MAX_YEAR + 1):
		# get data from web endpoint
		yearData = get_and_parse_data(year)

		# load database tables with data
		for i in range(0, len(TABLE_NAMES)):
			# send data 
			currentTableName = TABLE_NAMES[i]
			currentDataCategory = JSON_NAMES[i]
			stats.loadStats(currentTableName, year, yearData["ALL"][currentDataCategory])

apiReady = False
print("Initializing records...")
initialize_records()
print("Records initialized.")
apiReady = True

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
	return {'time': time.time()}

@app.route('/api/ready')
def get_api_ready():
	return {'ready': apiReady}

@app.route('/api/data')
def get_api_data():
	query="""
		SELECT
			name as "Name",			
			-- format overall to XX.XX (2 digits before decimal, 2 after)
			substr(
				'00' || printf("%.2f", round(overall*100, 2) ),
				-5,
				5
			) as "Use %",
			overall	as "Use as Decimal"
		FROM warframe
		WHERE year=?
		ORDER BY overall DESC;
	"""
	values=[2025]
	results = stats.runQuery(query, values)
	print(results)

	return results

@app.route('/api/query', methods=['GET', 'POST'] )
def get_api_query():
	dictionary = request.args
	print(dictionary)
	query = dictionary['query']
	print(query)
	results = stats.runQuery(query)
	print(results)

	return results