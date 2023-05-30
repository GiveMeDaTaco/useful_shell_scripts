import pandas as pd
import pyodbc
import pyarrow.parquet as pq
import pyarrow as pa

# Establish a connection to your SQL database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=server_name;'
                      'DATABASE=database_name;'
                      'UID=user;'
                      'PWD=password')

# Define your SQL query
sql_query = "SELECT * FROM table_name"

# Initialize an empty ParquetWriter
writer = None

# Execute the query in chunks
for chunk in pd.read_sql(sql_query, conn, chunksize=10000):
    # Convert the chunk to arrow Table
    table = pa.Table.from_pandas(chunk)
    
    # If our writer is None, initialize it
    if writer is None:
        writer = pq.ParquetWriter('output.parquet', table.schema)
    
    # Write the table chunk
    writer.write_table(table)

# Close the writer
if writer:
    writer.close()

