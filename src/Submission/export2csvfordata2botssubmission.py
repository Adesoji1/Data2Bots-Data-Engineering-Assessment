import psycopg2
import csv

conn = psycopg2.connect(
    # your connection details
        dbname="d2b_accessment",
        user="adesalu8398",
        password="c7CPYwmPGm",
        host="34.89.230.185",
        port="5432"
    )

cur = conn.cursor()

with open('best_performing_product.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    cur.execute("SELECT * FROM adesalu8398_analytics.best_performing_product;")
    rows = cur.fetchall()
    for row in rows:
        writer.writerow(row)

cur.close()
conn.close()
