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
