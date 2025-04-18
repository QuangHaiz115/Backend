from app.db import get_connection

# Lấy tất cả đơn hàng
def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders")
    keys = [col[0] for col in cursor.description]
    return [dict(zip(keys, row)) for row in cursor.fetchall()]

# Lấy đơn hàng theo ID
def get_order_by_id(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders WHERE OrderID = ?", (order_id,))
    row = cursor.fetchone()
    if not row:
        return None
    keys = [col[0] for col in cursor.description]
    return dict(zip(keys, row))

# Thêm đơn hàng mới
def add_order(order_data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO Orders (CustomerID, OrderDate, TotalAmount, Status)
        VALUES (?, ?, ?, ?)
    """
    values = (
        order_data.get("CustomerID"),
        order_data.get("OrderDate"),
        order_data.get("TotalAmount"),
        order_data.get("Status")
    )
    cursor.execute(sql, values)
    conn.commit()

# Cập nhật đơn hàng
def update_order(order_id, order_data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE Orders
        SET CustomerID = ?, OrderDate = ?, TotalAmount = ?, Status = ?
        WHERE OrderID = ?
    """
    values = (
        order_data.get("CustomerID"),
        order_data.get("OrderDate"),
        order_data.get("TotalAmount"),
        order_data.get("Status"),
        order_id
    )
    cursor.execute(sql, values)
    conn.commit()

# Xóa đơn hàng
def delete_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Orders WHERE OrderID = ?", (order_id,))
    conn.commit()
