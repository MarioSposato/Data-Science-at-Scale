SELECT f.docid,
   f1.term,
   SUM(f.count * f1.count) AS similarity
FROM Frequency f
INNER JOIN Frequency f1
ON f.term = f1.term
where f.docid < f1.docid
and f.docid = '10080_txt_crude'
and f1.docid = '17035_txt_earn'
GROUP BY f1.docid;