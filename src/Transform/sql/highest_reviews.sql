CREATE TABLE adesalu8398_analytics.best_performing_product_metrics AS

-- Get the product with the highest reviews
WITH HighestReviews AS (
    SELECT product_id, COUNT(review) as total_reviews
    FROM reviews
    GROUP BY product_id
    ORDER BY total_reviews DESC
    LIMIT 1
)

-- Get the day the product was ordered the most
, MostOrderedDay AS (
    SELECT order_date, COUNT(order_id) as total_orders
    FROM orders
    WHERE product_id = (SELECT product_id FROM HighestReviews)
    GROUP BY order_date
    ORDER BY total_orders DESC
    LIMIT 1
)

-- Check if the most ordered day was a public holiday
, PublicHolidayCheck AS (
    SELECT 
        CASE 
            WHEN COUNT(*) > 0 THEN 'Yes'
            ELSE 'No'
        END AS is_public_holiday
    FROM if_common.dim_dates
    WHERE calendar_dt = (SELECT order_date::date FROM MostOrderedDay) -- Add the explicit cast here
    AND day_of_the_week_num BETWEEN 1 AND 5 
    AND working_day = false
)


-- Get the total review points for the product
, TotalReviewPoints AS (
    SELECT SUM(review) as total_review_points
    FROM reviews
    WHERE product_id = (SELECT product_id FROM HighestReviews)
)

-- Get the percentage distribution of the review points
, ReviewDistribution AS (
    SELECT review, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as pct
    FROM reviews
    WHERE product_id = (SELECT product_id FROM HighestReviews)
    GROUP BY review
)

-- Get the percentage distribution of early shipments to late shipments
, ShipmentDistribution AS (
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

-- Combine the results
SELECT 
    hr.product_id,
    hr.total_reviews,
    mod.order_date AS most_ordered_day,
    phc.is_public_holiday,
    trp.total_review_points,
    rd.review,
    rd.pct AS review_distribution_pct,
    sd.shipment_status,
    sd.pct AS shipment_distribution_pct
FROM HighestReviews hr
CROSS JOIN MostOrderedDay mod
CROSS JOIN PublicHolidayCheck phc
CROSS JOIN TotalReviewPoints trp
CROSS JOIN ReviewDistribution rd
CROSS JOIN ShipmentDistribution sd;