# import psycopg2

# # Connect to your postgres DB
# conn = psycopg2.connect(
#     dbname="d2b_accessment",
#     user="adesalu8398",
#     password="c7CPYwmPGm",
#     host="34.89.230.185",
#     port="5432"
# )

# # Open a cursor to perform database operations
# cur = conn.cursor()

# print("Connected to the database.")

# # Create a view for most ordered day for each product
# cur.execute("""
#     CREATE OR REPLACE VIEW adesalu8398_staging.product_most_ordered_day AS
#     SELECT product_id, order_date AS most_ordered_day
#     FROM (
#         SELECT product_id, order_date, COUNT(*) AS order_count
#         FROM adesalu8398_staging.orders
#         GROUP BY product_id, order_date
#         ORDER BY product_id, order_count DESC
#     ) AS subquery
#     GROUP BY product_id, most_ordered_day;
# """)

# print("Created the view for most ordered day for each product.")

# # Execute the SQL query to calculate the metrics and insert them into the best_performing_product table
# cur.execute("""
#     INSERT INTO adesalu8398_analytics.best_performing_product (
#         ingestion_date,
#         product_name,
#         most_ordered_day,
#         is_public_holiday,
#         tt_review_points,
#         pct_one_star_review,
#         pct_two_star_review,
#         pct_three_star_review,
#         pct_four_star_review,
#         pct_five_star_review,
#         pct_early_shipments,
#         pct_late_shipments
#     )
#     SELECT
#         CURRENT_DATE,
#         p.product_name,
#         mod.most_ordered_day,
#             CASE 
#                 WHEN d.day_of_the_week_num BETWEEN 1 AND 5 AND d.working_day = false THEN true
#                 ELSE false
#             END AS is_public_holiday,
#         SUM(r.review) AS tt_review_points,
#         SUM(CASE WHEN r.review = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_one_star_review,
#         SUM(CASE WHEN r.review = 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_two_star_review,
#         SUM(CASE WHEN r.review = 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_three_star_review,
#         SUM(CASE WHEN r.review = 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_four_star_review,
#         SUM(CASE WHEN r.review = 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_five_star_review,
#         SUM(CASE WHEN s.delivery_date < s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_early_shipments,
#         SUM(CASE WHEN s.delivery_date > s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_late_shipments


#     FROM
#         adesalu8398_staging.dim_products AS p
#     JOIN
#         adesalu8398_staging.product_most_ordered_day AS mod ON p.product_id::integer = mod.product_id::integer
#     JOIN
#         adesalu8398_staging.orders AS o ON p.product_id::integer = o.product_id::integer
#     JOIN
#         adesalu8398_staging.dim_dates AS d ON o.order_date = d.calendar_dt
#     JOIN
#         adesalu8398_staging.reviews AS r ON p.product_id::integer = r.product_id::integer
#     JOIN
#         adesalu8398_staging.shipments_deliveries AS s ON o.order_id = s.order_id
#     WHERE
#         p.product_id::integer = (
#             SELECT
#                 product_id::integer
#             FROM
#                 adesalu8398_staging.reviews
#             ORDER BY
#                 review DESC
#             LIMIT 1
#         )
# """)

# # Commit the changes
# conn.commit()

# print("Inserted the results into the best_performing_product table.")

# # Fetch the results from the best_performing_product table
# cur.execute("""
#     SELECT *
#     FROM adesalu8398_analytics.best_performing_product
# """)

# results = cur.fetchall()

# # Write the results to a CSV file
# with open('best_performing_product.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow([desc[0] for desc in cur.description])  # write the header
#     writer.writerows(results)  # write the data

# print("Saved the results to best_performing_product.csv")

# # Close the cursor and the connection
# cur.close()
# conn.close()


# import psycopg2
# import csv

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

#     # Create a view for most ordered day for each product
#     cur.execute("""
#         CREATE OR REPLACE VIEW product_most_ordered_day AS
#         SELECT
#             product_id,
#             order_date AS most_ordered_day
#         FROM
#             (
#                 SELECT
#                     product_id,
#                     order_date,
#                     ROW_NUMBER() OVER(PARTITION BY product_id ORDER BY COUNT(*) DESC) as rn
#                 FROM
#                     adesalu8398_staging.orders
#                 GROUP BY
#                     product_id,
#                     order_date
#             ) q
#         WHERE
#             rn = 1
#     """)

#     print("Created the view for most ordered day for each product.")

#     # Execute the SQL query to calculate the metrics and insert them into the best_performing_product table
#     cur.execute("""
#         INSERT INTO adesalu8398_analytics.best_performing_product (
#             ingestion_date,
#             product_name,
#             most_ordered_day,
#             is_public_holiday,
#             tt_review_points,
#             pct_one_star_review,
#             pct_two_star_review,
#             pct_three_star_review,
#             pct_four_star_review,
#             pct_five_star_review,
#             pct_early_shipments,
#             pct_late_shipments
#         )
#         SELECT
#             CURRENT_DATE,
#             p.product_name,
#             mod.most_ordered_day,
#             CASE 
#                 WHEN d.day_of_the_week_num BETWEEN 1 AND 5 AND d.working_day = false THEN true
#                 ELSE false
#             END AS is_public_holiday,
#             SUM(r.review) AS tt_review_points,
#             SUM(CASE WHEN r.review = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_one_star_review,
#             SUM(CASE WHEN r.review = 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_two_star_review,
#             SUM(CASE WHEN r.review = 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_three_star_review,
#             SUM(CASE WHEN r.review = 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_four_star_review,
#             SUM(CASE WHEN r.review = 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_five_star_review,
#             SUM(CASE WHEN s.delivery_date < s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_early_shipments,
#             SUM(CASE WHEN s.delivery_date > s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_late_shipments
        # FROM
        #     adesalu8398_staging.dim_products AS p
        # JOIN
        #     adesalu8398_staging.product_most_ordered_day AS mod ON p.product_id::integer = mod.product_id::integer
        # JOIN
        #     adesalu8398_staging.orders AS o ON p.product_id::integer = o.product_id::integer
        # JOIN
        #     adesalu8398_staging.dim_dates AS d ON o.order_date = d.calendar_dt
        # JOIN
        #     adesalu8398_staging.reviews AS r ON p.product_id::integer = r.product_id::integer
        # JOIN
        #     adesalu8398_staging.shipments_deliveries AS s ON o.order_id = s.order_id
#         WHERE
#             p.product_id = (
#                 SELECT
#                     product_id
#                 FROM
#                     adesalu8398_staging.reviews
#                 ORDER BY
#                     review DESC
#                 LIMIT 1
#             )
#         GROUP BY
#             p.product_name,
#             mod.most_ordered_day,
#             d.day_of_the_week_num,
#             d.working_day,
#             s.shipment_date,
#             s.delivery_date
#     """)

#     # Commit the changes
#     conn.commit()

#     print("Inserted the results into the best_performing_product table.")

#     # Fetch the results from the best_performing_product table
#     cur.execute("""
#         SELECT *
#         FROM adesalu8398_analytics.best_performing_product
#     """)

#     results = cur.fetchall()

#     # Write the results to a CSV file
#     with open('best_performing_product.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([desc[0] for desc in cur.description])  # write the header
#         writer.writerows(results)  # write the data

#     print("Saved the results to best_performing_product.csv")

# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     # Close the cursor and the connection
#     if cur is not None:
#         cur.close()
#     if conn is not None:
#         conn.close()
#         print("Closed the connection to the database.")



import psycopg2
import csv

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

    # Create a view for most ordered day for each product
    cur.execute("""
        CREATE OR REPLACE VIEW adesalu8398_staging.product_most_ordered_day AS
        SELECT
            product_id,
            order_date AS most_ordered_day
        FROM
            (
                SELECT
                    product_id,
                    order_date,
                    ROW_NUMBER() OVER(PARTITION BY product_id ORDER BY COUNT(*) DESC) as rn
                FROM
                    adesalu8398_staging.orders
                GROUP BY
                    product_id,
                    order_date
            ) q
        WHERE
            rn = 1
    """)

    print("Created the view for most ordered day for each product.")

    # Execute the SQL query to calculate the metrics and insert them into the best_performing_product table
    cur.execute("""
        INSERT INTO adesalu8398_analytics.best_performing_product (
            ingestion_date,
            product_name,
            most_ordered_day,
            is_public_holiday,
            tt_review_points,
            pct_one_star_review,
            pct_two_star_review,
            pct_three_star_review,
            pct_four_star_review,
            pct_five_star_review,
            pct_early_shipments,
            pct_late_shipments
        )
        SELECT
            CURRENT_DATE,
            p.product_name,
            mod.most_ordered_day,
            CASE 
                WHEN d.day_of_the_week_num BETWEEN 1 AND 5 AND d.working_day = false THEN true
                ELSE false
            END AS is_public_holiday,
            SUM(r.review) AS tt_review_points,
            SUM(CASE WHEN r.review = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_one_star_review,
            SUM(CASE WHEN r.review = 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_two_star_review,
            SUM(CASE WHEN r.review = 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_three_star_review,
            SUM(CASE WHEN r.review = 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_four_star_review,
            SUM(CASE WHEN r.review = 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_five_star_review,
            SUM(CASE WHEN s.delivery_date < s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_early_shipments,
            SUM(CASE WHEN s.delivery_date > s.shipment_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_late_shipments
        FROM
            adesalu8398_staging.dim_products AS p
        JOIN
            adesalu8398_staging.product_most_ordered_day AS mod ON p.product_id::integer = mod.product_id::integer
        JOIN
            adesalu8398_staging.orders AS o ON p.product_id::integer = o.product_id::integer
        JOIN
            adesalu8398_staging.dim_dates AS d ON o.order_date = d.calendar_dt
        JOIN
            adesalu8398_staging.reviews AS r ON p.product_id::integer = r.product_id::integer
        JOIN
            adesalu8398_staging.shipments_deliveries AS s ON o.order_id = s.order_id
        WHERE
            p.product_id = (
                SELECT
                    product_id
                FROM
                    adesalu8398_staging.reviews
                ORDER BY
                    review DESC
                LIMIT 1
            )
        GROUP BY
            p.product_name,
            mod.most_ordered_day,
            d.day_of_the_week_num,
            d.working_day,
            s.shipment_date,
            s.delivery_date
    """)

    # Commit the changes
    conn.commit()

    print("Inserted the results into the best_performing_product table.")

    # Fetch the results from the best_performing_product table
    cur.execute("""
        SELECT *
        FROM adesalu8398_analytics.best_performing_product
    """)

    results = cur.fetchall()

    # Write the results to a CSV file
    with open('best_performing_product.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([desc[0] for desc in cur.description])  # write the header
        writer.writerows(results)  # write the data

    print("Saved the results to best_performing_product.csv")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and the connection
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print("Closed the connection to the database.")
