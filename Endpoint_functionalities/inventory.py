from typing import Optional, List

def get_inventory(db, low_stock_threshold: Optional[int] = None) -> List[dict]:
    conn = db.connection
    cursor = conn.cursor()

    query = """
        SELECT i.Inventory_ID, i.Product_ID, p.name, i.Quantity
        FROM Inventory i
        JOIN Products p ON i.Product_ID = p.Prod_ID
    """
    params = []
    if low_stock_threshold is not None:
        query += " WHERE i.Quantity <= %s"
        params.append(low_stock_threshold)
    query += " ORDER BY i.Quantity ASC;"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    inventory_list = []
    for row in results:
        inventory_list.append({
            "inventory_id": row[0],
            "product_id": row[1],
            "product_name": row[2],
            "quantity": row[3],
        })

    cursor.close()
    return inventory_list


def update_inventory(db, product_id: int, quantity: int) -> dict:
    conn = db.connection
    cursor = conn.cursor()

    # Check if product exists
    cursor.execute("SELECT COUNT(*) FROM Products WHERE Prod_ID = %s", (product_id,))
    if cursor.fetchone()[0] == 0:
        cursor.close()
        raise ValueError("Product not found")

    # Update or insert inventory record
    cursor.execute("UPDATE Inventory SET Quantity = %s WHERE Product_ID = %s", (quantity, product_id))
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO Inventory (Product_ID, Quantity) VALUES (%s, %s)", (product_id, quantity))

    conn.commit()
    cursor.close()
    return {"message": f"Inventory updated for product_id {product_id} with quantity {quantity}"}
