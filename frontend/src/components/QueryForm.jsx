import React from 'react';

function QueryForm(props){

	const [query, setQuery] = React.useState("");

	function handleChange(event) {
		let userInput = event.target.value;
		setQuery(userInput);
	}

	function handleSubmit(event) {
		console.log(query)
		props.runQuery(query)

		// prevents default form submission behavior of refreshing page
		event.preventDefault();
	}

	return (
		<form onSubmit={handleSubmit}>
			<textarea 
				onChange={handleChange}
				type='text'
				placeholder=""
				value={query}
				disabled={false}
				autoComplete="off"
				autoFocus={true}
			/>
			<br/>
			<button 
				type="submit"
				disabled = {false}
			>Execute Query</button>
		</form>
	);

}

export default QueryForm;