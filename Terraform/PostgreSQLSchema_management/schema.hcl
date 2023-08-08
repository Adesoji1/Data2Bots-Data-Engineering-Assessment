schema "adesalu8398_staging" {
  comment = "Schema for adesalu8398_staging"
}

// dim_addresses
table "dim_addresses" {
  schema = schema.adesalu8398_staging
  column "postal_code" {
    type = int
    primary_key = true
  }
  column "country" {
    type = varchar(255)
  }
  column "region" {
    type = varchar(255)
  }
  column "state" {
    type = varchar(255)
  }
  column "address" {
    type = varchar(255)
  }
}

// dim_dates
table "dim_dates" {
  schema = schema.adesalu8398_staging
  column "calendar_dt" {
    type = date
    primary_key = true
  }
  column "year_num" {
    type = int
  }
  column "month_of_the_year_num" {
    type = int
  }
  column "day_of_the_month_num" {
    type = int
  }
  column "day_of_the_week_num" {
    type = int
  }
  column "working_day" {
    type = bool
  }
}

// dim_products
table "dim_products" {
  schema = schema.adesalu8398_staging
  column "product_id" {
    type = int
    primary_key = true
  }
  column "product_category" {
    type = varchar(255)
  }
  column "product_name" {
    type = varchar(255)
  }
}

// dim_customers
table "dim_customers" {
  schema = schema.adesalu8398_staging
  column "customer_id" {
    type = int
    primary_key = true
  }
  column "customer_name" {
    type = char(50)
  }
  column "postal_code" {
    type = int
  }
  foreign_key "postal_code_fk" {
    columns = [column.postal_code]
    ref_columns = [dim_addresses.postal_code]
  }
}

// orders
table "orders" {
  schema = schema.adesalu8398_staging
  column "order_id" {
    type = int
    primary_key = true
  }
  column "product_id" {
    type = varchar(255)
  }
  column "customer_id" {
    type = int
  }
  column "order_date" {
    type = date
  }
  foreign_key "product_id_fk" {
    columns = [column.product_id]
    ref_columns = [dim_products.product_id]
  }
  foreign_key "customer_id_fk" {
    columns = [column.customer_id]
    ref_columns = [dim_customers.customer_id]
  }
}

// reviews
table "reviews" {
  schema = schema.adesalu8398_staging
  column "review_id" {
    type = int
    primary_key = true
  }
  column "product_id" {
    type = varchar(255)
  }
  foreign_key "product_id_fk_reviews" {
    columns = [column.product_id]
    ref_columns = [dim_products.product_id]
  }
}

// shipments_deliveries
table "shipments_deliveries" {
  schema = schema.adesalu8398_staging
  column "shipment_id" {
    type = int
    primary_key = true
  }
  column "order_id" {
    type = int
  }
  foreign_key "order_id_fk_shipments" {
    columns = [column.order_id]
    ref_columns = [orders.order_id]
  }
}
