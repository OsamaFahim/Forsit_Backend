from typing import Optional, List, Tuple
from datetime import date

def get_sales( db,start_date: Optional[date] = None,end_date: Optional[date] = None,product_id: Optional[int] = None,
category_id: Optional[int] = None, ) -> List[dict]:
    
    conn = db.connection
    cursor = conn.cursor()

    query_string = """
        SELECT s.Sales_ID, s.date, p.Prod_ID, p.name, p.price, c.Category_ID, c.name as category_name, ps.Quantity
        FROM Sales s
        JOIN Product_Sales ps ON s.Sales_ID = ps.Sales_ID
        JOIN Products p ON ps.Prod_ID = p.Prod_ID
        JOIN Category c ON p.category_ID = c.Category_ID
        WHERE 1=1
    """
    params = []

    if start_date:
        query_string += " AND s.date >= %s"
        params.append(start_date)
    if end_date:
        query_string += " AND s.date <= %s"
        params.append(end_date)
    if product_id:
        query_string += " AND p.Prod_ID = %s"
        params.append(product_id)
    if category_id:
        query_string += " AND c.Category_ID = %s"
        params.append(category_id)

    cursor.execute(query_string, tuple(params))
    results = cursor.fetchall()

    sales_list = []
    for row in results:
        sales_list.append({
            "sales_id": row[0],
            "date": row[1],
            "product_id": row[2],
            "product_name": row[3],
            "price": float(row[4]),
            "category_id": row[5],
            "category_name": row[6],
            "quantity": row[7],
        })

    cursor.close()
    return sales_list


def get_revenue_grouped(db,group_by_expr: str,start_date: Optional[date] = None,end_date: Optional[date] = None,) -> List[Tuple]:
    conn = db.connection
    cursor = conn.cursor()

    query = f"""
        SELECT {group_by_expr} as period, SUM(p.price * ps.Quantity) as revenue
        FROM Sales s
        JOIN Product_Sales ps ON s.Sales_ID = ps.Sales_ID
        JOIN Products p ON ps.Prod_ID = p.Prod_ID
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND s.date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND s.date <= %s"
        params.append(end_date)
    query += f" GROUP BY {group_by_expr} ORDER BY {group_by_expr} ASC;"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    cursor.close()
    return results


def revenue_daily(db, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[dict]:
    results = get_revenue_grouped(db, "DATE(s.date)", start_date, end_date)
    return [{"date": r[0], "revenue": float(r[1])} for r in results]


def revenue_weekly(db, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[dict]:
    # Returns Year and Week number
    conn = db.connection
    cursor = conn.cursor()

    query = """
        SELECT YEAR(s.date) as yr, WEEK(s.date, 1) as wk, SUM(p.price * ps.Quantity) as revenue
        FROM Sales s
        JOIN Product_Sales ps ON s.Sales_ID = ps.Sales_ID
        JOIN Products p ON ps.Prod_ID = p.Prod_ID
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND s.date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND s.date <= %s"
        params.append(end_date)
    query += " GROUP BY yr, wk ORDER BY yr, wk ASC;"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()

    return [{"week": f"{r[0]}-W{r[1]}", "revenue": float(r[2])} for r in results]


def revenue_monthly(db, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[dict]:
    conn = db.connection
    cursor = conn.cursor()

    query = """
        SELECT YEAR(s.date) as yr, MONTH(s.date) as mn, SUM(p.price * ps.Quantity) as revenue
        FROM Sales s
        JOIN Product_Sales ps ON s.Sales_ID = ps.Sales_ID
        JOIN Products p ON ps.Prod_ID = p.Prod_ID
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND s.date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND s.date <= %s"
        params.append(end_date)
    query += " GROUP BY yr, mn ORDER BY yr, mn ASC;"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()

    return [{"month": f"{r[0]}-{r[1]:02d}", "revenue": float(r[2])} for r in results]


def revenue_yearly(db, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[dict]:
    conn = db.connection
    cursor = conn.cursor()

    query = """
        SELECT YEAR(s.date) as yr, SUM(p.price * ps.Quantity) as revenue
        FROM Sales s
        JOIN Product_Sales ps ON s.Sales_ID = ps.Sales_ID
        JOIN Products p ON ps.Prod_ID = p.Prod_ID
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND s.date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND s.date <= %s"
        params.append(end_date)
    query += " GROUP BY yr ORDER BY yr ASC;"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()

    return [{"year": r[0], "revenue": float(r[1])} for r in results]


def revenue_compare(db,start_date1: date,end_date1: date,start_date2: date,end_date2: date,category_id: Optional[int] = None,) -> dict:
    conn = db.connection
    cursor = conn.cursor()

    def get_revenue(start_date, end_date):
        query = """
            SELECT SUM(p.price * ps.Quantity)
            FROM Sales s
            JOIN Product_Sales ps ON s.Sales_ID = ps.Sales_ID
            JOIN Products p ON ps.Prod_ID = p.Prod_ID
            WHERE s.date BETWEEN %s AND %s
        """
        params = [start_date, end_date]
        if category_id:
            query += " AND p.category_ID = %s"
            params.append(category_id)
        cursor.execute(query, tuple(params))
        return cursor.fetchone()[0] or 0

    rev1 = get_revenue(start_date1, end_date1)
    rev2 = get_revenue(start_date2, end_date2)

    cursor.close()
    return {
        "period_1": {"start_date": start_date1, "end_date": end_date1, "revenue": float(rev1)},
        "period_2": {"start_date": start_date2, "end_date": end_date2, "revenue": float(rev2)},
        "difference": float(rev2 - rev1),
    }
