select count(*)
from(
select docid, count(*) as s
from Frequency
GROUP by docid
having s>300)
