from flask import Blueprint, request, jsonify
from models import get_connection
import uuid

devices_bp = Blueprint('devices', __name__)


# GET ALL DEVICES
@devices_bp.route('/devices', methods=['GET'])
def get_devices():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, created_at, created_by
        FROM devices;
    """)
    devices = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for d in devices:
        result.append({
            "id": str(d[0]),
            "name": d[1],
            "created_at": str(d[2]),
            "created_by": str(d[3]) if d[3] else None
        })

    return jsonify(result), 200


# CREATE DEVICE
@devices_bp.route('/devices', methods=['POST'])
def create_device():
    data = request.json

    name = data.get('name')
    created_by = data.get('created_by')

    # validation
    if not name or not created_by:
        return jsonify({"error": "Missing name or created_by"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # check if user exists 
    cur.execute("SELECT id FROM users WHERE id=%s;", (created_by,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "created_by user does not exist"}), 404

    device_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO devices (id, name, created_by)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (device_id, name, created_by))

    returned_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Device created",
        "id": str(returned_id)
    }), 201


# UPDATE DEVICE
@devices_bp.route('/devices/<id>', methods=['PUT'])
def update_device(id):
    data = request.json

    name = data.get('name')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE devices
        SET name=%s
        WHERE id=%s;
    """, (name, id))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "Device not found"}), 404

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Device updated"}), 200


# 
# DELETE DEVICE
@devices_bp.route('/devices/<id>', methods=['DELETE'])
def delete_device(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM devices WHERE id=%s;", (id,))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "Device not found"}), 404

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Device deleted"}), 200