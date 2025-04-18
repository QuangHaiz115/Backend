from flask import Blueprint, jsonify, request
from app.db import get_connection
from utils.password import verify_password
from utils.auth import generate_token

user_bp = Blueprint('user_bp', __name__)

# Lấy toàn bộ user
@user_bp.route('/getall', methods=['GET'])
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [User]")
    keys = [i[0] for i in cursor.description]
    result = [dict(zip(keys, row)) for row in cursor.fetchall()]
    return jsonify(result)


# Lấy user theo ID
@user_bp.route('/get/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [User] WHERE UserID = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"message": "User not found"}), 404
        keys = [i[0] for i in cursor.description]
        return jsonify(dict(zip(keys, row)))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Thêm user mới
@user_bp.route('/add', methods=['POST'])
def add_user():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO [User] (Username, PasswordHash, FullName, Email, Phone, Address, Role)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        data.get("Username"),
        data.get("PasswordHash"),
        data.get("FullName"),
        data.get("Email"),
        data.get("Phone"),
        data.get("Address"),
        data.get("Role")
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Cập nhật user
@user_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE [User]
        SET Username = ?, PasswordHash = ?, FullName = ?, Email = ?, Phone = ?, Address = ?, Role = ?
        WHERE UserID = ?
    """
    values = (
        data.get("Username"),
        data.get("PasswordHash"),
        data.get("FullName"),
        data.get("Email"),
        data.get("Phone"),
        data.get("Address"),
        data.get("Role"),
        user_id
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Xóa user
@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM [User] WHERE UserID = ?", (user_id,))
        conn.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Đăng nhập
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("Username")
        password = data.get("Password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Kết nối database và lấy thông tin user
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT UserID, Username, PasswordHash, Role FROM [User] WHERE Username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Chuyển dữ liệu user thành dictionary
        keys = [i[0] for i in cursor.description]
        user_dict = dict(zip(keys, user))

        # Kiểm tra mật khẩu
        if not verify_password(password, user_dict["PasswordHash"]):
            return jsonify({"error": "Invalid credentials"}), 401

        # Tạo JWT token
        token = generate_token(user_dict["UserID"], role=user_dict["Role"])
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "UserID": user_dict["UserID"],
                "Username": user_dict["Username"],
                "Role": user_dict["Role"]
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
