import { useState, useEffect } from 'react'
import QueryForm from './components/QueryForm'
import ResultsGrid from './components/ResultsGrid'

import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const MAX_API_TRIES = 10;

function App() {
	const [itemGrid, setItemGrid] = useState(null);
	const [count, setCount] = useState(0);
	const [currentTime, setCurrentTime] = useState(0);

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



	function loadData2222() {
		console.log("Asking API for data...");
		fetch('/api/data')
			.then(
				response => {
					if (response.ok) {
						return response.json();
					}
					throw response; // will be handled by catch
				}
			).then(
				data => {
					console.log("Data received!");
					setItemGrid(data);
					console.log(data);
				}
			).catch(
				exception => {
					console.log("Couldn't connect!");
					throw exception;
				}
			);
		fetch(
			'https://api.sunrise-sunset.org/json?' + new URLSearchParams(
				{
					lat: 69,
					lng: 108,
				}
			)
		).then(
			response => {
				if (response.ok) {
					return response.json();
				}
				throw response; // will be handled by catch
			}
		).then(
			data => {
				console.log("Data received!");
				console.log(data);
			}
		).catch(
			exception => {
				console.log("Couldn't connect!");
				throw exception;
			}
		);
	}

	function loadData() {
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
		fetch('/api/query?' + new URLSearchParams(
				{
					query: query,
				}
			)
		).then(
			response => {
				if (response.ok) {
					return response.json();
				}
				throw response; // will be handled by catch
			}
		).then(
			data => {
				console.log("Data received!");
				setItemGrid(data);
				console.log(data);
			}
		).catch(
			exception => {
				console.log("Couldn't connect!");
				throw exception;
			}
		);
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
				if (response.ok) {
					return response.json();
				}
				throw response; // will be handled by catch
			}
		).then(
			data => {
				console.log("Query results received!");
				setItemGrid(data);
				console.log(data);
			}
		).catch(
			exception => {
				console.log("Couldn't connect!");
				throw exception;
			}
		);
	}




	return (
		<>
			<div>
				<a href="https://vite.dev" target="_blank">
					<img src={viteLogo} className="logo" alt="Vite logo" />
				</a>
				<a href="https://react.dev" target="_blank">
					<img src={reactLogo} className="logo react" alt="React logo" />
				</a>
			</div>
			<h1>Vite + React</h1>
			<div className="card">
				<button onClick={() => setCount((count) => count + 1)}>
					count is {count}
				</button>
				<button onClick={loadData}>
					Load Data
				</button>
				<p>
					Edit <code>src/App.jsx</code> and save to test HMR
				</p>
				<p>First rendered at {new Date(currentTime * 1000).toLocaleString()}.</p>
			</div>
			<p className="read-the-docs">
				Click on the Vite and React logos to learn more
			</p>
			<QueryForm
				runQuery={runQuery}
			/>
			<ResultsGrid
				itemGrid={itemGrid}
			/>
		</>
	)
}

export default App
