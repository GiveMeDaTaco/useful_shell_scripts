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

WITH RankedData AS (
  SELECT sortbad, identifier1, identifier2,
         DENSE_RANK() OVER (ORDER BY sortbad) AS rank
  FROM user_work.waterfall
)
SELECT sortbad,
       SUM(CASE WHEN rank = sortbad THEN 1 ELSE 0 END) AS identifier1_dropped,
       COUNT(DISTINCT identifier1) FILTER (WHERE rank = 1) AS identifier1_remaining,
       SUM(CASE WHEN rank = sortbad THEN 1 ELSE 0 END) AS identifier2_dropped,
       COUNT(DISTINCT CONCAT(identifier1, ':', identifier2)) FILTER (WHERE rank = 1) AS identifier2_remaining
FROM RankedData
GROUP BY sortbad
ORDER BY sortbad;


WITH 
  -- Get the maximum sortbad for each identifier1
  max_sortbad AS (
    SELECT identifier1, MAX(sortbad) AS max_sortbad
    FROM user_work.waterfall
    GROUP BY identifier1
  ),
  
  -- Get the count of identifier1 dropped at each sortbad level
  dropped_identifier1 AS (
    SELECT 
      sb.sortbad, 
      COUNT(DISTINCT mw.identifier1) AS identifier1_dropped
    FROM 
      max_sortbad mw
    JOIN 
      user_work.waterfall w ON mw.identifier1 = w.identifier1
    WHERE 
      w.sortbad = mw.max_sortbad
    GROUP BY 
      sb.sortbad
  ),
  
  -- Get the count of unique identifier1 remaining at each sortbad level
  remaining_identifier1 AS (
    SELECT 
      sb.sortbad, 
      COUNT(DISTINCT w.identifier1) AS identifier1_remaining
    FROM 
      user_work.waterfall w
    JOIN 
      (SELECT DISTINCT identifier1 FROM user_work.waterfall WHERE sortbad < sb.sortbad) mw 
      ON w.identifier1 = mw.identifier1
    GROUP BY 
      sb.sortbad
  ),
  
  -- Get the count of identifier1:identifier2 dropped at each sortbad level
  dropped_identifier1_identifier2 AS (
    SELECT 
      sb.sortbad, 
      COUNT(DISTINCT w.identifier1, w.identifier2) AS identifier1_identifier2_dropped
    FROM 
      max_sortbad mw
    JOIN 
      user_work.waterfall w ON mw.identifier1 = w.identifier1
    WHERE 
      w.sortbad = mw.max_sortbad
    GROUP BY 
      sb.sortbad
  ),
  
  -- Get the count of unique identifier1:identifier2 remaining at each sortbad level
  remaining_identifier1_identifier2 AS (
    SELECT 
      sb.sortbad, 
      COUNT(DISTINCT w.identifier1, w.identifier2) AS identifier1_identifier2_remaining
    FROM 
      user_work.waterfall w
    JOIN 
      (SELECT DISTINCT identifier1, identifier2 FROM user_work.waterfall WHERE sortbad < sb.sortbad) mw 
      ON w.identifier1 = mw.identifier1 AND w.identifier2 = mw.identifier2
    GROUP BY 
      sb.sortbad
  )

SELECT 
  sb.sortbad,
  di1.identifier1_dropped,
  ri1.identifier1_remaining,
  di2.identifier1_identifier2_dropped,
  ri2.identifier1_identifier2_remaining
FROM 
  (SELECT DISTINCT sortbad FROM user_work.waterfall) sb
LEFT JOIN 
  dropped_identifier1 di1 ON sb.sortbad = di1.sortbad
LEFT JOIN 
  remaining_identifier1 ri1 ON sb.sortbad = ri1.sortbad
LEFT JOIN 
  dropped_identifier1_identifier2 di2 ON sb.sortbad = di2.sortbad
LEFT JOIN 
  remaining_identifier1_identifier2 ri2 ON sb.sortbad = ri2.sortbad
ORDER BY 
  sb.sortbad;
