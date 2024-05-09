SELECT 
    wf.sortbad,
    COUNT(DISTINCT CASE WHEN id1_min_sortbad.sortbad = wf.sortbad THEN id1_min_sortbad.identifier1 END) AS identifier1_dropped,
    COUNT(DISTINCT CASE WHEN id1_min_sortbad.sortbad > wf.sortbad THEN id1_min_sortbad.identifier1 END) AS identifier1_remaining,
    COUNT(DISTINCT CASE WHEN id1_id2_min_sortbad.sortbad = wf.sortbad THEN id1_id2_min_sortbad.identifier1 || ':' || id1_id2_min_sortbad.identifier2 END) AS identifier1_identifier2_dropped,
    COUNT(DISTINCT CASE WHEN id1_id2_min_sortbad.sortbad > wf.sortbad THEN id1_id2_min_sortbad.identifier1 || ':' || id1_id2_min_sortbad.identifier2 END) AS identifier1_identifier2_remaining
FROM 
    user_work.waterfall wf
    LEFT JOIN (
        SELECT identifier1, MIN(sortbad) AS sortbad
        FROM user_work.waterfall
        GROUP BY identifier1
    ) id1_min_sortbad
    ON wf.sortbad >= id1_min_sortbad.sortbad
    LEFT JOIN (
        SELECT identifier1, identifier2, MIN(sortbad) AS sortbad
        FROM user_work.waterfall
        GROUP BY identifier1, identifier2
    ) id1_id2_min_sortbad
    ON wf.sortbad >= id1_id2_min_sortbad.sortbad
GROUP BY 
    wf.sortbad
ORDER BY 
    wf.sortbad;
