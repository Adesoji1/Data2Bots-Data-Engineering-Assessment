WITH PublicHolidays AS (
    SELECT calendar_dt
    FROM if_common.dim_dates
    WHERE day_of_the_week_num BETWEEN 1 AND 5 
    AND working_day = false
    AND calendar_dt BETWEEN '2021-09-05' AND '2022-09-05' -- Considering the past year from the given current_date
)

INSERT INTO adesalu8398_analytics.agg_public_holiday (
    ingestion_date,
    tt_order_hol_jan,
    tt_order_hol_feb,
    tt_order_hol_mar,
    tt_order_hol_apr,
    tt_order_hol_may,
    tt_order_hol_jun,
    tt_order_hol_jul,
    tt_order_hol_aug,
    tt_order_hol_sep,
    tt_order_hol_oct,
    tt_order_hol_nov,
    tt_order_hol_dec
)
SELECT
    '2022-09-05' AS ingestion_date, -- Given current_date
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 1 THEN 1 ELSE 0 END) AS tt_order_hol_jan,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 2 THEN 1 ELSE 0 END) AS tt_order_hol_feb,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 3 THEN 1 ELSE 0 END) AS tt_order_hol_mar,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 4 THEN 1 ELSE 0 END) AS tt_order_hol_apr,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 5 THEN 1 ELSE 0 END) AS tt_order_hol_may,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 6 THEN 1 ELSE 0 END) AS tt_order_hol_jun,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 7 THEN 1 ELSE 0 END) AS tt_order_hol_jul,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 8 THEN 1 ELSE 0 END) AS tt_order_hol_aug,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 9 THEN 1 ELSE 0 END) AS tt_order_hol_sep,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 10 THEN 1 ELSE 0 END) AS tt_order_hol_oct,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 11 THEN 1 ELSE 0 END) AS tt_order_hol_nov,
    SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date::date) = 12 THEN 1 ELSE 0 END) AS tt_order_hol_dec
FROM orders o
JOIN PublicHolidays ph ON o.order_date::date = ph.calendar_dt::date;
