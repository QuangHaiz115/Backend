from flask import Blueprint, jsonify, request
from app.db import get_connection

drink_bp = Blueprint('drink_bp', __name__)

# Lấy toàn bộ đồ uống
@drink_bp.route('/getall', methods=['GET'])
def get_all_drinks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Drink")
    keys = [i[0] for i in cursor.description]
    result = [dict(zip(keys, row)) for row in cursor.fetchall()]
    return jsonify(result)


# Lấy đồ uống theo ID
@drink_bp.route('/get/<int:drink_id>', methods=['GET'])
def get_drink_by_id(drink_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Drink WHERE DrinkID = ?", (drink_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"message": "Drink not found"}), 404
        keys = [i[0] for i in cursor.description]
        return jsonify(dict(zip(keys, row)))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Thêm đồ uống mới
@drink_bp.route('/add', methods=['POST'])
def add_drink():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO Drink (Name, Description, Price)
        VALUES (?, ?, ?)
    """
    values = (
        data.get("Name"),
        data.get("Description"),
        data.get("Price")
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "Drink added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Cập nhật đồ uống
@drink_bp.route('/update/<int:drink_id>', methods=['PUT'])
def update_drink(drink_id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE Drink
        SET Name = ?, Description = ?, Price = ?
        WHERE DrinkID = ?
    """
    values = (
        data.get("Name"),
        data.get("Description"),
        data.get("Price"),
        drink_id
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "Drink updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Xóa đồ uống
@drink_bp.route('/delete/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Drink WHERE DrinkID = ?", (drink_id,))
        conn.commit()
        return jsonify({"message": "Drink deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
