import React from 'react';

function ResultsGrid(props){

	function displayHeader(header, index) {
		return (
			<th key={index}>
				{header}
			</th>
		);
	}
	
	function displayItem(item, index) {
		return (
			<td key={index}>
				{item}
			</td>
		);
	}
	
	function displayRow(row, index) {
		return (
			<tr key={index}>
				{row.map(displayItem)}
			</tr>
		);
	}

	return (
		<div className="results">
			{props.itemGrid &&
				<table>
					<thead>
						<tr>
							{props.itemGrid.headers.map(displayHeader)}	
						</tr>
					</thead>
					<tbody>
						{props.itemGrid.records.map(displayRow)}
					</tbody>
				</table>
			}
		</div>
	);

}

export default ResultsGrid;