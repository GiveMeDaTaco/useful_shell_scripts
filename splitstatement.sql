WITH RECURSIVE SplitCTE (id, value, rest, idx) AS (
    SELECT 
        id,
        CASE 
            WHEN CHARINDEX(';', col) > 0 THEN SUBSTRING(col, 1, CHARINDEX(';', col) - 1)
            ELSE col
        END AS value,
        CASE 
            WHEN CHARINDEX(';', col) > 0 THEN SUBSTRING(col, CHARINDEX(';', col) + 1)
            ELSE NULL
        END AS rest,
        1 AS idx
    FROM your_table
    WHERE col IS NOT NULL

    UNION ALL

    SELECT 
        id,
        CASE 
            WHEN CHARINDEX(';', rest) > 0 THEN SUBSTRING(rest, 1, CHARINDEX(';', rest) - 1)
            ELSE rest
        END AS value,
        CASE 
            WHEN CHARINDEX(';', rest) > 0 THEN SUBSTRING(rest, CHARINDEX(';', rest) + 1)
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
