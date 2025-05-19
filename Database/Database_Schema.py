import random
from datetime import date, timedelta

#I am using the Base Table to create table, and also allow to populate these tables which have been created as well
class Base_Table:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    #Table creation would be done through this function
    def create_table(self, query_string, name_of_table):
        try:
            #Executing the query, given to the Base_Table as query string 
            self.cursor.execute(query_string)
            print(f"{name_of_table} has been created")
        except Exception as excepton_occured:
            print(f"Faield to created table, exception is : {excepton_occured}")

    
#I am inheriting the entities table from the above table to accomodate insertion in the database
#It passes a qeury string to its parent table so that it can allow insertion
class Catergory_Table(Base_Table):
    def create(self):
        query_string = """
        Create Table If Not Exists Category (
            Category_ID INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
        """
        self.create_table(query_string, "Category")

class Products_Table(Base_Table):
    def create(self):
        query_string = """
        Create Table If Not Exists Products (
            Prod_ID INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            category_ID INT,
            FOREIGN KEY (category_ID) REFERENCES Category(Category_ID)
        );
        """
        self.create_table(query_string, "Products")

class Sales_Table(Base_Table):
    def create(self):
        query_string = """
        Create Table If Not Exists Sales (
            Sales_ID INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL
        );
        """
        self.create_table(query_string, "Sales")

class Product_Sales_Table(Base_Table):
    def create(self):
        query_string = """
        Create Table If Not Exists Product_Sales (
            Prod_ID INT NOT NULL,
            Sales_ID INT NOT NULL,
            Quantity INT NOT NULL,
            PRIMARY KEY (Prod_ID, Sales_ID),
            FOREIGN KEY (Prod_ID) REFERENCES Products(Prod_ID),
            FOREIGN KEY (Sales_ID) REFERENCES Sales(Sales_ID)
        );
        """
        self.create_table(query_string, "Product_Sales")

class InventoryTable(Base_Table):
    def create(self):
        query_string = """
        Create Table If Not Exists Inventory (
            Inventory_ID INT AUTO_INCREMENT PRIMARY KEY,
            Product_ID INT NOT NULL,
            Quantity INT NOT NULL,
            FOREIGN KEY (Product_ID) REFERENCES Products(Prod_ID)
        );
        """
        self.create_table(query_string, "Inventory")

#Creation of the schema using above classes
def create_all_tables(db):
    print("Creating all tables...")

    conn = db.connection
    cursor = conn.cursor()

    Catergory_Table(conn, cursor).create()
    Products_Table(conn, cursor).create()
    Sales_Table(conn, cursor).create()
    Product_Sales_Table(conn, cursor).create()
    InventoryTable(conn, cursor).create()

    print("All tables created.")

#Note don't run this function more than once, so that is correctly stored in the table and FK constraints are not breached.
#If it is necessary to run this function first reset the table using "reset_all_tables" funtion and then you can run this function again
def populate_all_tables(db):
    print("Population of Tables Started...")

    conn = db.connection
    cursor = conn.cursor()

    try:
        #First data is stored in array and the respective table is being populated
        
        #Inserting data into the category table, and category is named as {category 1, category 2, ... etc}, adding 100 categories
        #Firstly the data is stored in the array and then these statements would be executed by the 
        category_data = [(f"Category_{i}",) for i in range(1, 101)]
        cursor.executemany("Insert into Category (name) values (%s);", category_data)
        print("Categories Have been inserted into the table")

        #Inserting procuts with name, price and cateogry_ID (foreign key), price is 2 decimally rounded value between {10, 1000} and name is like
        #{Product_1, Product_2, ... etc}
        #The touple contains (name, price, category_ID)
        product_data = [(f"Product_{i}", round(random.uniform(10, 1000), 2), random.randint(1, 100)) for i in range(1, 20001)]
        cursor.executemany("Insert INTO Products (name, price, category_ID) values (%s, %s, %s);", product_data)
        print("Products Have been inserted into the table")

        #Inserting Sales with the Date values, we are getting 20000 last year values and they are formatted as tuples 
        sales_data = [ ((date.today() - timedelta(days=random.randint(0, 365))),) for _ in range(20000)]
        cursor.executemany("Insert INTO Sales (date) Values (%s);", sales_data)
        print("Sales Have been inserted into the table")

        #We are adding the products in our inventory with there qunatity as well, with product_id being the foreign key in this case

        inventory_data = [(i, random.randint(10, 200)) for i in range(1, 20001)]
        cursor.executemany("Insert INTO Inventory (Product_ID, Quantity) values (%s, %s);", inventory_data)
        print("Inventory Have been inserted into the table")

        # Note: as the relationship between sales and products is many to many so, that is we are creating a seperate table and both foreign keys 
        # will be there that we are adding, and foreign key constaint would be satisfied as we have alraeady added 20,000 products already
        #First we will have to put the values in a set so only unique values are inserted into the table
        product_sales_set = set()
        while len(product_sales_set) < 50000:
            prod_id = random.randint(1, 20000)
            sale_id = random.randint(1, 20000)
            key = (prod_id, sale_id) #As this tuple is what we are inserting into the table
            if key not in product_sales_set:
                product_sales_set.add(key)
        product_sales_data = [(prod_id, sale_id, random.randint(1, 10)) for prod_id, sale_id in product_sales_set]
        cursor.executemany("Insert INTO Product_Sales (Prod_ID, Sales_ID, Quantity) values (%s, %s, %s);", product_sales_data)
        print("Products_sales Have been inserted into the table")

        conn.commit()
        print("All data inserted successfully.")
    except Exception as failed_population:
        print(f"Failed to populate tables, exception is {failed_population}")

def reset_all_tables(db):
    print("Resetting all tables...")

    conn = db.connection
    cursor = conn.cursor()

    try: 
        # Delete in this order, so that no foreign key constraint is voilated, and no error is given
        cursor.execute("Delete FROM Product_Sales;")
        cursor.execute("Delete FROM Inventory;")
        cursor.execute("Delete FROM Products;")
        cursor.execute("Delete FROM Sales;")
        cursor.execute("Delete FROM Category;")

        # Reset auto increments as well to start the auto_increment value to 1
        cursor.execute("Alter Table Product_Sales auto_increment = 1;")
        cursor.execute("Alter Table Inventory auto_increment = 1;")
        cursor.execute("Alter Table Products auto_increment = 1;")
        cursor.execute("Alter Table Sales auto_increment = 1;")
        cursor.execute("Alter Table Category auto_increment = 1;")

        conn.commit()
        print("All tables have been reset. Now you can call the {populate_all_data} function again to populate the tables.")
    except Exception as failed_reset:
        print(f"Failed to reset tables, exception is {failed_reset}")

def create_indexes(db):
    # I noticed that sales endpoint was taking most time so indexing the date, products_id and category_id for fast queries and lookups
    print("Creating indexes to optimize sales query...")

    conn = db.connection
    cursor = conn.cursor()

    try:
        #I am creating a tuple with index name along with the column that needs to be indexed
        indexes = [
            ("idx_sales_date", "Sales(date)"),
            ("idx_products_prod_id", "Products(Prod_ID)"),
            ("idx_category_id", "Category(Category_ID)"),
            ("idx_ps_sales_id", "Product_Sales(Sales_ID)"),
            ("idx_ps_prod_id", "Product_Sales(Prod_ID)"),
            ("idx_products_category_id", "Products(category_ID)")
        ]

        #I am iterating so that duplicate indexing is not done
        for index_name, table_column in indexes:
            try:
                cursor.execute(f"create index {index_name} on {table_column};")
            except Exception as e:
                 # Index already exists so I am now creating it again am continuing
                if "Duplicate key name" in str(e):
                    continue 
                else:
                    print(f"Failed to create index {index_name}: {e}")

        print("Indexing has been completed...")
    except Exception as failed_indexing:
        print(f"Failed to create indexing, exception is {failed_indexing}")

