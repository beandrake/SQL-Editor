import { useState, useEffect } from 'react';
import QueryForm from './components/QueryForm';
import ResultsGrid from './components/ResultsGrid';
import coreFrameQuery from './queries/coreFrame';
import './App.css';

// Edit this file and save to experience Hot Module Replacement.


/*
	Todo List:

		- This App.jsx file is overdue for refactoring.
				Some of the content can probably be removed entirely,
				but first at least put some of the functionality in
				other files.

		- Frontend CMD gets errors when trying to connect to backend.
				This removes the URL from the CMD, and it's less than clean.

		- Interface is a bit all over the place; how to make it coherent?
				Maybe have some buttons for pre-generated example queries?
				Or perhaps something else.

		- Error-handling for bad queries.

		- Eventually will probably want to extract data returned from queries.
				Can currently copy and paste into in full to Excel/Sheets.
					Is that enough for now?
					Maybe hold off until use cases validate a need for more.
*/



const MAX_API_TRIES = 10;

function App() {
	
	const [statusMessage, setStatusMessage] =  useState("Awaiting query...");
	const [statusError, setStatusError] =  useState(false);
	const [itemGrid, setItemGrid] = useState(null);
	const [count, setCount] = useState(0);
	const [currentTime, setCurrentTime] = useState(0);

	// NOTE: React knows where to send fetch requests, see vite.config.js
	
	
	// reaches out to the Python API up to 10 times with 1 second delays
	function getTime(tries=1){
		console.log("Asking API for current time, attempt #" + tries + "...");
		setTimeout(
			() => {
				fetch('/api/time')
					.then(
						response => {
							if (response.ok) {
								return response.json();
							}
							throw response; // will be handled by catch
						}
					).then(
						data => {
							console.log("Time received!");
							setCurrentTime(data.time);
						}
					).catch(
						exception => {
							if(tries < MAX_API_TRIES){
								getTime(tries+1);
							}else{
								console.log("Couldn't connect!");
								throw exception;
							}
						}
					);
			},
			1000	//1 seconds
		);
	}

	useEffect(
		() => {						
			getTime();
		},
		[] // run once when component is initially rendered and never again
	);





	function performSampleQuery() {
		console.log("Asking API for data...");
		let query = `
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
		WHERE year=2025
		ORDER BY overall DESC;
		`		
		runQuery(query);
	}
	


	function runQuery(query) {
		console.log("Sending query...");	
		fetch('/api/query?' + new URLSearchParams(
				{
					query: query,
				}
			)
		).then(
			response => {
				console.log("Response received, status code: " + response.status);
				console.log(response);
				setStatusError(!response.ok);
				if (response.status === 400){
					console.log("Here dat boi");
					console.log(response.json());
				}
				if (response.ok) {
					setStatusMessage("Query executed successfully.");
					if (response.status === 204){
						return Promise.resolve(null);
					}else{
						let data = response.json();
						console.log(data);
						return data;
					}
				}
				setStatusMessage("Something bad happened. (add better error-handling later)");
				throw response; // will be handled by catch
			}
		).then(
			data => {
				console.log("Query results received!");
				if (data != null){
					setItemGrid(data);
				}
				console.log(data);
			}
		).catch(
			exception => {
				// put any specific error-handling here
				console.log("...and then an error occurred.");
				//throw exception; // enable anytime you want to see the details in the log
			}
		);
	}




	return (
		<>
			<div className="upper">
				<QueryForm
					runQuery={runQuery}
					defaultQueryText={coreFrameQuery}
					statusMessage={statusMessage}
					statusError={statusError}
				/>
			</div>
			<div className="lower">
				<ResultsGrid
					itemGrid={itemGrid}
				/>
			</div>
		</>
	)
}

export default App;
