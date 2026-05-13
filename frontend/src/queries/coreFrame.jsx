
const coreFrameQuery = `
-- This query combines the overall usage rates of all variants of a frame type.
-- For example, Excalibur Umbra, Excalibur Prime, and Excalibur are all Excalibur variants.

select
	FrameType, SUM(overall) as "Overall"
FROM
(
	-- Sub-query returns the Warframe table with a new column, FrameType
	select 
		-- isolates the name of a frame, without modifiers like Prime or Umbra
		subSTR(name, 1, inSTR(name||' ', ' ') - 1) as "FrameType",
		*
	from warframe
	order by overall desc
)
WHERE year=2025
GROUP BY FrameType
ORDER BY "Overall" DESC;
`;

export default coreFrameQuery;