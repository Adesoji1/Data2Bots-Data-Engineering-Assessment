# # import psycopg2

# # try:
# #     # Connect to your postgres DB
# #     conn = psycopg2.connect(
# #         dbname="d2b_accessment",
# #         user="adesalu8398",
# #         password="c7CPYwmPGm",
# #         host="34.89.230.185",
# #         port="5432"
# #     )

# #     # Open a cursor to perform database operations
# #     cur = conn.cursor()

# #     print("Connected to the database.")

# #     # Execute the SQL query
# #     cur.execute("""
# #         INSERT INTO adesalu8398_analytics.agg_public_holiday (
# #             ingestion_date,
# #             tt_order_hol_jan,
# #             tt_order_hol_feb,
# #             tt_order_hol_mar,
# #             tt_order_hol_apr,
# #             tt_order_hol_may,
# #             tt_order_hol_jun,
# #             tt_order_hol_jul,
# #             tt_order_hol_aug,
# #             tt_order_hol_sep,
# #             tt_order_hol_oct,
# #             tt_order_hol_nov,
# #             tt_order_hol_dec
# #         )
# #         SELECT 
# #             DATE_TRUNC('month', o.order_date) AS ingestion_date,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 1) AS tt_order_hol_jan,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 2) AS tt_order_hol_feb,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 3) AS tt_order_hol_mar,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 4) AS tt_order_hol_apr,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 5) AS tt_order_hol_may,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 6) AS tt_order_hol_jun,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 7) AS tt_order_hol_jul,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 8) AS tt_order_hol_aug,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 9) AS tt_order_hol_sep,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 10) AS tt_order_hol_oct,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 11) AS tt_order_hol_nov,
# #             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 12) AS tt_order_hol_dec
# #         FROM 
# #             adesalu8398_staging.orders AS o
# #         JOIN 
# #             if_common.dim_dates AS d
# #         ON 
# #             o.order_date = d.calendar_dt
# #         WHERE 
# #             d.day_of_the_week_num BETWEEN 1 AND 5
# #             AND d.working_day = false
# #             AND o.order_date >= (CURRENT_DATE - INTERVAL '1 year')
# #         GROUP BY 
# #             ingestion_date;
# #     """)

# #     print("Executed the SQL query.")

# #     # Commit the changes
# #     conn.commit()

# # except Exception as e:
# #     print(f"An error occurred: {e}")
# #     conn.rollback()

# # finally:
# #     # Close the cursor and the connection
# #     if cur is not None:
# #         cur.close()
# #     if conn is not None:
# #         conn.close()
# #         print("Closed the connection to the database.")



# import psycopg2

# try:
#     # Connect to your postgres DB
#     conn = psycopg2.connect(
#         dbname="d2b_accessment",
#         user="adesalu8398",
#         password="c7CPYwmPGm",
#         host="34.89.230.185",
#         port="5432"
#     )

#     # Open a cursor to perform database operations
#     cur = conn.cursor()

#     print("Connected to the database.")

#     # Execute the SQL query to calculate the total number of orders placed on a public holiday every month for the past year
#     cur.execute("""
#         INSERT INTO adesalu8398_analytics.agg_public_holiday (
#             ingestion_date,
#             tt_order_hol_jan,
#             tt_order_hol_feb,
#             tt_order_hol_mar,
#             tt_order_hol_apr,
#             tt_order_hol_may,
#             tt_order_hol_jun,
#             tt_order_hol_jul,
#             tt_order_hol_aug,
#             tt_order_hol_sep,
#             tt_order_hol_oct,
#             tt_order_hol_nov,
#             tt_order_hol_dec
#         )
#         SELECT 
#             DATE_TRUNC('month', o.order_date) AS ingestion_date,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 1) AS tt_order_hol_jan,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 2) AS tt_order_hol_feb,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 3) AS tt_order_hol_mar,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 4) AS tt_order_hol_apr,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 5) AS tt_order_hol_may,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 6) AS tt_order_hol_jun,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 7) AS tt_order_hol_jul,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 8) AS tt_order_hol_aug,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 9) AS tt_order_hol_sep,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 10) AS tt_order_hol_oct,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 11) AS tt_order_hol_nov,
#             COUNT(*) FILTER (WHERE EXTRACT(MONTH FROM o.order_date) = 12) AS tt_order_hol_dec
#         FROM 
#             adesalu8398_staging.orders AS o
#         JOIN 
#             if_common.dim_dates AS d
#         ON 
#             o.order_date = d.calendar_dt
#         WHERE 
#             d.day_of_the_week_num BETWEEN 1 AND 5
#             AND d.working_day = false
#             AND o.order_date >= (CURRENT_DATE - INTERVAL '1 year')
#         GROUP BY 
#             ingestion_date;
#     """)

#     print("Inserted data into adesalu8398_analytics.agg_public_holiday.")

#     # Execute the SQL query to calculate the total number of late shipments
#     cur.execute("""
#         SELECT COUNT(*)
#         FROM adesalu8398_staging.shipments_deliveries AS sd
#         JOIN adesalu8398_staging.orders AS o
#         ON sd.order_id = o.order_id
#         WHERE sd.shipment_date >= o.order_date + INTERVAL '6 days'
#         AND sd.delivery_date IS NULL
#     """)

#     # Fetch the result
#     result = cur.fetchone()

#     print(f"Total number of late shipments: {result[0]}")

#     # # Execute the SQL query to calculate the total number of undelivered shipments
#     # cur.execute("""
#     #     SELECT COUNT(*)
#     #     FROM adesalu8398_staging.shipments_deliveries
#     #     WHERE delivery_date IS NULL
#     #     AND shipment_date IS NULL
#     #     AND '2022-09-05'::date - order_date >= 15
#     # """)

#     # # Fetch the result
#     # result = cur.fetchone()

#     # print(f"Total number of undelivered shipments: {result[0]}")

#     # Commit the changes
#     conn.commit()

# except Exception as e:
#     print(f"An error occurred: {e}")
#     conn.rollback()

# finally:
#     # Close the cursor and the connection
#     if cur is not None:
#         cur.close()
#     if conn is not None:
#         conn.close()
#         print("Closed the connection to the database.")


import psycopg2

try:
    # Connect to your postgres DB
    conn = psycopg2.connect(
        dbname="d2b_accessment",
        user="adesalu8398",
        password="c7CPYwmPGm",
        host="34.89.230.185",
        port="5432"
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    print("Connected to the database.")

    # Execute the SQL query to calculate the total number of late shipments
    cur.execute("""
    SELECT COUNT(*) 
    FROM adesalu8398_staging.shipments_deliveries AS s
    JOIN adesalu8398_staging.orders AS o ON s.order_id = o.order_id
    WHERE s.shipment_date >= o.order_date + INTERVAL '6 days' 
    AND s.delivery_date IS NULL
""")


    # Fetch the result
    result = cur.fetchone()

    print(f"Total number of late shipments: {result[0]}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and the connection
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print("Closed the connection to the database.")
