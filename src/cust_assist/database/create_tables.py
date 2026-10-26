from src.cust_assist.database.connection import get_connection
from src.cust_assist.logger import logger

class CreateTables:

    def __init__(self):
        pass

    def execute(self,cmd):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(cmd)
                conn.commit()

            logger.info("Executed successfully")

        except Exception as e:
            logger.info(e)

    def create_customer(self):

        customer="""
        CREATE TABLE customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(150) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(30),
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(customer)
        logger.info("created customer table")

    def create_product(self):

        product="""
        CREATE TABLE products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            sku VARCHAR(64) UNIQUE NOT NULL,
            product_name VARCHAR(200) NOT NULL,
            category VARCHAR(80),
            warranty_months INT DEFAULT 12,
            warranty_type VARCHAR(30) DEFAULT 'limited'
        );
        """ 
        self.execute(product)
        logger.info("created products table")
    
    def create_orders(self):

        orders="""
        CREATE TABLE orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10,2),
            status VARCHAR(20) DEFAULT 'delivered',

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        );
                """
        self.execute(orders)
        logger.info("created orders table")


    def create_order_items(self):

        order_items="""
        CREATE TABLE order_items (
            order_item_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT DEFAULT 1,
            unit_price DECIMAL(10,2),
            serial_number VARCHAR(100) UNIQUE,

            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        );
        """
        
        self.execute(order_items)
        logger.info("created order items table")

    def create_warranty_claims(self):
        
        claims="""
            CREATE TABLE warranty_claims (
                claim_id INT AUTO_INCREMENT PRIMARY KEY,
                order_item_id INT NOT NULL,
                claim_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                issue_description TEXT NOT NULL,
                status ENUM(
                    'submitted',
                    'under_review',
                    'approved',
                    'rejected',
                    'repaired',
                    'replaced',
                    'closed'
                ) DEFAULT 'submitted',

                FOREIGN KEY (order_item_id)
                    REFERENCES order_items(order_item_id)

            );
            """
        self.execute(claims)
        logger.info("created warranty claims table")

    def create(self): 
        
        self.create_customer()
        self.create_product()
        self.create_orders()
        self.create_order_items()
        self.create_warranty_claims()

        return self
    