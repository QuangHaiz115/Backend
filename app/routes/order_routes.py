from flask import Blueprint, jsonify, request
from app.services.order_service import (
    get_all_orders,
    get_order_by_id,
    add_order,
    update_order,
    delete_order
)

order_bp = Blueprint('order_bp', __name__)

# Lấy tất cả đơn hàng
@order_bp.route('/getall', methods=['GET'])
def get_orders():
    try:
        result = get_all_orders()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lấy đơn hàng theo ID
@order_bp.route('/get/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = get_order_by_id(order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        return jsonify(order)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Thêm đơn hàng mới
@order_bp.route('/add', methods=['POST'])
def create_order():
    try:
        data = request.json
        add_order(data)
        return jsonify({"message": "Order added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Cập nhật đơn hàng
@order_bp.route('/update/<int:order_id>', methods=['PUT'])
def edit_order(order_id):
    try:
        data = request.json
        update_order(order_id, data)
        return jsonify({"message": "Order updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Xóa đơn hàng
@order_bp.route('/delete/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    try:
        delete_order(order_id)
        return jsonify({"message": "Order deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
