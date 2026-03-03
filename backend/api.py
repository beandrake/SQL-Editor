import time
from flask import Flask, request

from usageStats import UsageStats
from getData import get_and_parse_data


MIN_YEAR = 2020
MAX_YEAR = 2025
MASTERY_RANK_MAX = 36
TABLE_NAMES=["warframe", "primary_weapon", "secondary_weapon", "melee_weapon"]
JSON_NAMES=["Warframe", "Primary", "Secondary", "Melee"]


# initialize database as global variable
statData = UsageStats(MASTERY_RANK_MAX, TABLE_NAMES)

def initialize_records():
	"""
	Load database tables with yearly statistical data pulled from web endpoint.
	"""
	for year in range(MIN_YEAR, MAX_YEAR + 1):
		# get data from web endpoint
		dataForThisYear = get_and_parse_data(year)

		# load each database table with that year's data
		for i in range(0, len(TABLE_NAMES)):
			currentTableName = TABLE_NAMES[i]
			currentDataCategory = JSON_NAMES[i]
			statData.loadStats(
				currentTableName, 
				year, 
				dataForThisYear["ALL"][currentDataCategory]
			)


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


# Runs a pre-determined sample query.
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
	results = statData.runQuery(query, values)
	print(results)

	return results


# Runs any query the user submits.
@app.route('/api/query', methods=['GET', 'POST'] )
def get_api_query():
	dictionary = request.args
	print(dictionary)
	query = dictionary['query']
	print(query)
	results = statData.runQuery(query)
	print(results)

	return results