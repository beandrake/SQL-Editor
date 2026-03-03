
const coreFrameQuery = `
-- This query isolates the name of each distinct Warframe,
-- without modifiers like Prime or Umbra.
select 
    substr(
        trim(name),
        1,
        instr(
            trim(name)||' ',
            ' '
        ) - 1
    ) as "Core Frame"
  ,*
from warframe
where year=2025
order by overall desc;
`;

export default coreFrameQuery;