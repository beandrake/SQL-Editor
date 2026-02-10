import sqlite3
import datetime

# NOTE: refactor this to be 2 classes:
#	- a base database class
#	- an inherited class that does the Warframe stuff



class UsageStats:
	"""
	Contains yearly Warframe usage data saved locally to an sqlite3 database.
	"""

	# Without PARSE_DECLTYPES, a datetime.date that is inserted into the sqlite
	# database will be retrieved as a different datatype.
	DETECT_TYPES=sqlite3.PARSE_DECLTYPES
	

	def __init__(self, maxMasteryRank, tableNames):
		self.maxMasteryRank = maxMasteryRank
		self.tableNames = tableNames

		# Makes our database in memory, as opposed to in a file.
		databaseLocation = ":memory:"		
		self.database = sqlite3.connect(
			databaseLocation,
			detect_types=UsageStats.DETECT_TYPES,
			check_same_thread=False #only one thread writes at a time = safe
		)
		self.cursor = self.database.cursor()
		self._createTables()
		self._prepareQueries()


	def _createTables(self):
		# table definition, contains two placeholders (PH) to replace later
		makeTableQuery = r"""	
			CREATE TABLE --PH_Name--(
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL,
				year INTEGER NOT NULL,
				overall REAL NOT NULL,
				--PH_MR--
			) STRICT;
		"""

		# Automate rather than hard-coding the many nearly identical MR columns
		masteryRankColumns = "mr0 REAL"
		for rank in range(1, self.maxMasteryRank+1):
			masteryRankColumns += "," + "\n" + "mr" + str(rank) + " REAL"
		
		makeTableQuery = makeTableQuery.replace(r"--PH_MR--", masteryRankColumns)
		
		# make all tables
		previousName = r"--PH_Name--"
		for name in self.tableNames:
			makeTableQuery = makeTableQuery.replace(previousName, name)
			print(makeTableQuery)
			self.cursor.execute(makeTableQuery)
			previousName = name
		
		# verify existence (can be removed later)
		#self.cursor.execute(r"SELECT name FROM sqlite_schema WHERE type='table'")
		#for result in self.cursor:
		#	print(result)


	def _prepareQueries(self):
		masteryRankColumns = "mr0"
		masteryRankValues = "?"
		for rank in range(1, self.maxMasteryRank+1):
			masteryRankColumns += ", " + "mr" + str(rank)
			masteryRankValues += ", " + "?"

		self.insertQuery = f"""
			INSERT INTO --PH_Name--
				(name, year, overall, {masteryRankColumns})
			VALUES
				(?, ?, ?, {masteryRankValues});
		"""


	def loadStats(self, table, year, data):
		
		query = self.insertQuery.replace("--PH_Name--", table)
		
		for itemName in data:
			#print(data[itemName])			
			all = data[itemName]["ALL"]
			values = [ itemName, year, all]
			
			
			for rank in range(0, self.maxMasteryRank+1):
				# not all items/years have access to all Mastery Ranks
				try:
					currentRankValue = data[itemName][str(rank)]
				except:
					currentRankValue = None
				values.append(currentRankValue)

			#print(query)
			#print(values)

			self.cursor.execute(query, values)


	
	def runQuery(self, query, values=[]):
		"""
		Run the query and return the results into a dictionary containing
		two items: headers and records.
		"""
		self.cursor.execute(query, values)
		headerList = [desc[0] for desc in self.cursor.description]
		recordList = []
		for record in self.cursor:
			recordList.append(record)
		
		return {
			"headers": headerList,
			"records": recordList
		}





	def endSession(self):
		"""
		Closes the connection to the database, allowing memory to be freed and making this object unusable.
		"""
		#self.cursor.close()
		self.database.close()


	def clearNotes(self):
		"""
		Removes all records from the database.
		"""
		# sqlite doesn't have truncate; this is the advised alternative
		self.cursor.execute(r"DROP TABLE notes")
		self._createTables()



	def save(self, filename):		
		"""
		Saves database as a file.
		"""
		savedDatabase = sqlite3.connect(filename, detect_types=UsageStats.DETECT_TYPES)
		
		# this copies our database from memory into the newly-created database file
		with savedDatabase: 
			self.database.backup(savedDatabase, pages=1)
		savedDatabase.close()


	def load(self, filename):
		"""
		Loads database from a file.
		"""
		loadedDatabase = sqlite3.connect(filename, detect_types=UsageStats.DETECT_TYPES)
		
		# this copies our database from a file into our in-memory database
		loadedDatabase.backup(self.database, pages=1)
		loadedDatabase.close()

		#self.cursor = self.database.cursor()
		





if __name__ == '__main__':
	myTodo = UsageStats()