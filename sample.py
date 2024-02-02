'''
This script is an example of creating the campaign BS024.
'''

import tlp_tools
import pyodbc
import pyarrow as pa
import pyarrow.parquet as pq
import polars as pl
import os

def main():
    # create database connection; this method assumes you are using kerberos authentication
    conn = pyodbc.connect('DSN=rchtera', user=os.getlogin(), password='l') # password cannot be left blank, so l is used as a placeholder
    cursor = conn.cursor()

    # sql query
    query = '''
        SELECT 
            mdm.pty_id,
            CASE 
                WHEN mdm.has_open_smbus_prod NE 'Y' THEN 11
                WHEN mdm.anti_money_scrub = Y' THEN 12 
                WHEN mdm.assoc_in = 'Y' THEN 13 
                WHEN mdm.badhh_in = 'Y' THEN 14
                WHEN mdm.bbk_in = 'N' OR smbus_cra_in = 'Y' THEN 15
                WHEN mdm.com_in = 'N' THEN 16
                WHEN mdm.dcsd_in = 'Y' THEN 17
                WHEN mdm.dlq_in = 'Y' THEN 18
                WHEN mdm.fcls_in = 'Y' THEN 19
                WHEN mdm.invalid_ssn = 'Y' THEN 20
                WHEN mdm.minor_18yr = 'Y' THEN 21
                WHEN mdm.pbk_in = 'Y' then 22
                WHEN mdm.pne_in = 'Y' THEN 23
                WHEN mdm.spec_in = 'Y' THEN 24
                WHEN mdm.rego_in = 'Y' THEN 25
                WHEN mdm.stat_in = 'Y' THEN 26
                WHEN mdm.divestiture = 'Y' THEN 27
                WHEN (ofr.offer_code = 'BS024' AND CURRENT_DATE - ofr.last_refusal_date < 90) OR ofr.last_refusal_date IS NOT NULL THEN 28
                WHEN mdm.rwd_elig_dda_flg = 'Y' THEN 29
                WHEN NOT (prb.rwd_tier_cd = '010' AND three_mo_agrgt_avg_bal GE 20000 AND three_mo_agrgt_avg_bal LT 50000) AND NOT (prb.rwd_tier_cd = '020' AND three_mo_agrgt_avg_bal GE 50000 AND three_mo_agrgt_avg_bal LT 100000) THEN 30
                WHEN COALESCE(prb.rwd_tier_cd NE 'ENROLLED') THEN 31
                WHEN bs020.pty_id IS NOT NULL THEN 32
                WHEN mdm.ptycl_id IS NULL THEN 33
                WHEN mdm.disaster_incdnt_dt IS NULL OR mdm.disaster_incdnt_dt >= CURRENT_DATE - 90 THEN 34
                ELSE 99 END AS sortbad 
        FROM
            vpilot_mts.mdm_party_vw mdm 
        LEFT JOIN (
            SELECT 
                pty_id,
                food_ofr_cd AS offer_code,
                MAX(CASE WHEN ofr_decsn_stat_cd = '1000009' THEN lst_pres_ts END) AS last_accept_date,
                MAX(CASE WHEN ofr_decsn_stat_cd <> '1000009' THEN lst_pres_ts END) AS last_refusal_date
            FROM 
                vpilot_mts.mdm_dail_ofr_vw 
            WHERE
                food_ofr_cd = 'BS024'
                AND ofr_descn_stat_cd NOT IN ('1000010', '1000011', '1000017', '1000019')
                AND NOT (ofr_descn_stat_cd = '1000007' AND lst_pres_lob_chn_unit_nm = 'BCTLR')
            GROUP BY 1,2
        ) ofr ON mdm.pty_id = ofr.pty_id
        
            
    '''

    # execute query
    cursor.execute(query)

    # prep pyarrow table
    fields = [pa.field(column_name, pa.string()) for column_name in cursor.description]
    schema = pa.schema(fields)

    # fetch data
    rows = cursor.fetchall()

    # store data in pyarrow
    data = [list(row) for row in rows]
    table = pa.Table.from_arrays(data, schema=schema)

    # import parquet into polars
    df = pl.from_arrow(table)

    # find eligible party id's
    eligible = df.filter(pl.col('sortbad') == 99)

    # create waterfall
    wf = df.groupby('sortbad').agg(pl.count('sortbad').alias('count')).sort('count')

    eligible.write_parquet('BS024.parquet')
    wf.write_csv('BS024_waterfall.csv')

if __name__ == '__main__':
    main()
