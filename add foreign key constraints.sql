USE store_inventory_db;

-- Adding foreign keys to purchases table
ALTER TABLE purchases
ADD COLUMN supplier_id INT;

ALTER TABLE purchases
ADD COLUMN product_id INT;

ALTER TABLE purchases
ADD CONSTRAINT fk_supplier
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id);

ALTER TABLE purchases
ADD CONSTRAINT fk_product_purchases
FOREIGN KEY (product_id) REFERENCES products(product_id);


-- Adding foreign keys to sales table
ALTER TABLE sales
ADD COLUMN customer_id INT;

ALTER TABLE sales
ADD COLUMN product_id INT;

ALTER TABLE sales
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE sales
ADD CONSTRAINT fk_product_sales
FOREIGN KEY (product_id) REFERENCES products(product_id);