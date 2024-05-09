SELECT 
    wf.sortbad,
    -- Count unique identifier1 that dropped at this sortbad level
    COUNT(DISTINCT CASE WHEN id1_min_sortbad.sortbad = wf.sortbad THEN id1_min_sortbad.identifier1 END) AS identifier1_dropped,
    -- Count unique identifier1 that have not failed by this sortbad level yet
    COUNT(DISTINCT CASE WHEN id1_min_sortbad.sortbad > wf.sortbad THEN id1_min_sortbad.identifier1 END) AS identifier1_remaining,
    -- Count unique identifier1:identifier2 pairs that dropped at this sortbad level
    COUNT(DISTINCT CASE WHEN id1_id2_min_sortbad.sortbad = wf.sortbad THEN id1_id2_min_sortbad.identifier1 || ':' || id1_id2_min_sortbad.identifier2 END) AS identifier1_identifier2_dropped,
    -- Count unique identifier1:identifier2 pairs that have not failed by this sortbad level yet
    COUNT(DISTINCT CASE WHEN id1_id2_min_sortbad.sortbad > wf.sortbad THEN id1_id2_min_sortbad.identifier1 || ':' || id1_id2_min_sortbad.identifier2 END) AS identifier1_identifier2_remaining
FROM 
    user_work.waterfall wf
    INNER JOIN (
        SELECT identifier1, MIN(sortbad) AS sortbad
        FROM user_work.waterfall
        GROUP BY identifier1
    ) id1_min_sortbad
    ON wf.sortbad >= id1_min_sortbad.sortbad
    INNER JOIN (
        SELECT identifier1, identifier2, MIN(sortbad) AS sortbad
        FROM user_work.waterfall
        GROUP BY identifier1, identifier2
    ) id1_id2_min_sortbad
    ON wf.sortbad >= id1_id2_min_sortbad.sortbad
GROUP BY 
    wf.sortbad
ORDER BY 
    wf.sortbad;
