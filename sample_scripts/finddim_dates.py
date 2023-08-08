import psycopg2
def find_dim_dates_schema():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="d2b_accessment",
        user="adesalu8398",
        password="c7CPYwmPGm",
        host="34.89.230.185",
        port="5432"
    )
    
    # Create a cursor object
    cur = conn.cursor()
    
    # SQL to find the schema of dim_dates
    sql_find_schema = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_name = 'dim_dates';
    """
    
    cur.execute(sql_find_schema)
    result = cur.fetchone()
    
    # Close the cursor and the connection
    cur.close()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

schema_name = find_dim_dates_schema()
print(f"The 'dim_dates' table is in the '{schema_name}' schema.")
