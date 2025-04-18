from flask import Blueprint, jsonify, request
from app.db import get_connection

food_bp = Blueprint('food_bp', __name__)

# Lấy toàn bộ món ăn
@food_bp.route('/getall', methods=['GET'])
def get_all_food():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [Food]")
    keys = [i[0] for i in cursor.description]
    result = [dict(zip(keys, row)) for row in cursor.fetchall()]
    return jsonify(result)

# Lấy món ăn theo ID
@food_bp.route('/get/<int:food_id>', methods=['GET'])
def get_food_by_id(food_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [Food] WHERE FoodID = ?", (food_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"message": "Food not found"}), 404
        keys = [i[0] for i in cursor.description]
        return jsonify(dict(zip(keys, row)))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Thêm món ăn mới
@food_bp.route('/add', methods=['POST'])
def add_food():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO [Food] (Name, Description, Price, Category, ImageUrl)
        VALUES (?, ?, ?, ?, ?)
    """
    values = (
        data.get("Name"),
        data.get("Description"),
        data.get("Price"),
        data.get("Category"),
        data.get("ImageUrl")
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "Food added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Cập nhật món ăn
@food_bp.route('/update/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE [Food]
        SET Name = ?, Description = ?, Price = ?, Category = ?, ImageUrl = ?
        WHERE FoodID = ?
    """
    values = (
        data.get("Name"),
        data.get("Description"),
        data.get("Price"),
        data.get("Category"),
        data.get("ImageUrl"),
        food_id
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "Food updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Xóa món ăn
@food_bp.route('/delete/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM [Food] WHERE FoodID = ?", (food_id,))
        conn.commit()
        return jsonify({"message": "Food deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
