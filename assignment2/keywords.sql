SELECT f.docid, f.term,
   SUM(f.count * f1.count) AS similarity
FROM query_view f
INNER JOIN query_view f1
ON f.term = f1.term
where f.docid='q' or f1.docid='q'
GROUP BY f.docid
order by similarity desc