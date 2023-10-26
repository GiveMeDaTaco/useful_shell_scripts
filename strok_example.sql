WITH RECURSIVE SplitValues AS (
    SELECT
        request_id,
        offer_cd,
        designation,
        market_type,
        STRTOK(market_type, ';', 1) AS market_type_split,
        1 AS split_index
    FROM
        table1
    JOIN
        table2
    ON
        table1.offer_cd = table2.offer_code
    
    UNION ALL
    
    SELECT
        request_id,
        offer_cd,
        designation,
        market_type,
        STRTOK(market_type, ';', split_index + 1) AS market_type_split,
        split_index + 1
    FROM
        SplitValues
    WHERE
        split_index < LENGTH(market_type) - LENGTH(OREPLACE(market_type, ';', '')) + 1
)
SELECT
    request_id,
    offer_cd,
    designation,
    market_type_split
FROM
    SplitValues
WHERE
    market_type_split IS NOT NULL AND TRIM(market_type_split) <> ''
ORDER BY
    request_id,
    split_index;
