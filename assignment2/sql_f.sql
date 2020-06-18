SELECT distinct f.docid
from Frequency as f
INNER join (
select * 
from Frequency 
where term='world'
)as c 
where f.docid = c.docid and
f.term='transactions'
