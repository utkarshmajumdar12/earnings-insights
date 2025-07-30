import os, psycopg2, psycopg2.extras as extras
def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST","localhost"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE")
    )
def upsert_df(df, table, cols):
    tuples = [tuple(x) for x in df[cols].to_numpy()]
    cols_str = ",".join(cols)
    query = f"INSERT INTO {table} ({cols_str}) VALUES %s ON CONFLICT DO NOTHING"
    conn = get_conn(); cur = conn.cursor()
    extras.execute_values(cur, query, tuples)
    conn.commit(); cur.close(); conn.close()
