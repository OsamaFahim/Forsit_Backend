# Forsit Backend

## To run the backend on your system

1. **Rename `.env.example` to `.env`** and add your environment variables there.

---

### 🔧 Note:
In `main.py`, the following function calls are commented. They take the singleton instance `db` as a parameter, which contains the connection and all:

- `create_all_tables(db)`: Used to create tables in the database (use only once)
- `populate_all_tables(db)`: Use to populate the data in tables which have been created (for repopulation, first call `reset_all_tables(db)`)
- `create_indexes(db)`: Use to create indexes for queries which takes longer time (recreate them if db has been reset)
- `reset_all_tables(db)`: Reset only when recreation is required, after that populate the tables again and indexing as well

---

### 📦 Install Required Packages

Run the following command to install required packages:

```bash
pip install -r requirements.txt

Below are the endpoints provided by the API:

- **GET /**: Returns a welcome message to the user, explaining how to access other endpoints.

- **GET /sales**: Returns sales data from the database.

- **GET /revenue/daily**: Returns daily revenue statistics.

- **GET /revenue/weekly**: Returns weekly revenue statistics.

- **GET /revenue/monthly**: Returns monthly revenue statistics.

- **GET /revenue/yearly**: Returns yearly revenue statistics.

- **GET /inventory**: Returns inventory information.

- **POST /inventory/update**: Update the quantity of a product.  
  Use [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and navigate to the update inventory endpoint to perform updates.

- **GET /revenue/compare**:  
  Example usage:  
  `http://127.0.0.1:8000/revenue/compare?start_date1=2025-01-01&end_date1=2025-01-31&start_date2=2025-02-01&end_date2=2025-02-28&category_id=3`  
  Use this format to compare revenue between two date ranges, optionally filtered by category.

- You can also filter sales by date using:  
  `GET /sales?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
