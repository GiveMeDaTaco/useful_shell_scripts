WITH RECURSIVE SplitCTE (id, value, rest, idx) AS (
    SELECT 
        id,
        CASE 
            WHEN POSITION(';' IN col) > 0 THEN SUBSTRING(col FROM 1 FOR POSITION(';' IN col) - 1)
            ELSE col
        END AS value,
        CASE 
            WHEN POSITION(';' IN col) > 0 THEN SUBSTRING(col FROM POSITION(';' IN col) + 1)
            ELSE NULL
        END AS rest,
        1 AS idx
    FROM your_table
    WHERE col IS NOT NULL

    UNION ALL

    SELECT 
        id,
        CASE 
            WHEN POSITION(';' IN rest) > 0 THEN SUBSTRING(rest FROM 1 FOR POSITION(';' IN rest) - 1)
            ELSE rest
        END AS value,
        CASE 
            WHEN POSITION(';' IN rest) > 0 THEN SUBSTRING(rest FROM POSITION(';' IN rest) + 1)
            ELSE NULL
        END AS rest,
        idx + 1
    FROM SplitCTE
    WHERE rest IS NOT NULL
)
SELECT 
    value,
    COUNT(*) AS value_count
FROM SplitCTE
GROUP BY value
ORDER BY value_count DESC;
