-- Define the CTEs and the final SELECT statement

WITH 
-- Get the product with the highest reviews
HighestReviews AS (
    SELECT product_id, COUNT(review) as total_reviews
    FROM reviews
    GROUP BY product_id
    ORDER BY total_reviews DESC
    LIMIT 1
),

-- Get the day the product was ordered the most
MostOrderedDay AS (
    SELECT order_date, COUNT(order_id) as total_orders
    FROM orders
    WHERE product_id = (SELECT product_id FROM HighestReviews)
    GROUP BY order_date
    ORDER BY total_orders DESC
    LIMIT 1
),

-- Check if the most ordered day was a public holiday
PublicHolidayCheck AS (
    SELECT 
        CASE 
            WHEN COUNT(*) > 0 THEN 'Yes'
            ELSE 'No'
        END AS is_public_holiday
    FROM if_common.dim_dates
    WHERE calendar_dt = (SELECT order_date::date FROM MostOrderedDay)
    AND day_of_the_week_num BETWEEN 1 AND 5 
    AND working_day = false
),

-- Get the total review points for the product
TotalReviewPoints AS (
    SELECT SUM(review) as total_review_points
    FROM reviews
    WHERE product_id = (SELECT product_id FROM HighestReviews)
),

-- Get the percentage distribution of the review points
ReviewDistribution AS (
    SELECT review, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as pct
    FROM reviews
    WHERE product_id = (SELECT product_id FROM HighestReviews)
    GROUP BY review
),

-- Get the percentage distribution of early shipments to late shipments
ShipmentDistribution AS (
    SELECT
        CASE 
            WHEN delivery_date < shipment_date THEN 'Early'
            ELSE 'Late'
        END as shipment_status,
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as pct
    FROM shipment_deliveries
    JOIN orders ON shipment_deliveries.order_id = orders.order_id
    WHERE orders.product_id = (SELECT product_id FROM HighestReviews)
    GROUP BY shipment_status
)


-- Combine the results and insert into the desired table
-- ... [rest of the CTEs remain unchanged]

-- Combine the results and insert into the desired table
INSERT INTO adesalu8398_analytics.best_performing_product (
    ingestion_date, -- Added this column
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
    '2022-09-05'::date AS ingestion_date, -- Added this static date
    p.product_name, 
    mod.order_date::date AS most_ordered_day,
    CASE WHEN phc.is_public_holiday = 'Yes' THEN TRUE ELSE FALSE END,
    trp.total_review_points,
    COALESCE(MAX(CASE WHEN rd.review = 1 THEN rd.pct END), 0) AS pct_one_star_review,
    COALESCE(MAX(CASE WHEN rd.review = 2 THEN rd.pct END), 0) AS pct_two_star_review,
    COALESCE(MAX(CASE WHEN rd.review = 3 THEN rd.pct END), 0) AS pct_three_star_review,
    COALESCE(MAX(CASE WHEN rd.review = 4 THEN rd.pct END), 0) AS pct_four_star_review,
    COALESCE(MAX(CASE WHEN rd.review = 5 THEN rd.pct END), 0) AS pct_five_star_review,
    COALESCE(MAX(CASE WHEN sd.shipment_status = 'Early' THEN sd.pct END), 0) AS pct_early_shipments,
    COALESCE(MAX(CASE WHEN sd.shipment_status = 'Late' THEN sd.pct END), 0) AS pct_late_shipments
FROM HighestReviews hr
JOIN if_common.dim_products p ON hr.product_id = p.product_id
CROSS JOIN MostOrderedDay mod
CROSS JOIN PublicHolidayCheck phc
CROSS JOIN TotalReviewPoints trp
CROSS JOIN ReviewDistribution rd
CROSS JOIN ShipmentDistribution sd
GROUP BY 
    p.product_name,
    mod.order_date,
    phc.is_public_holiday,
    trp.total_review_points;

