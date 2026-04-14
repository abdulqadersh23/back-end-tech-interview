from flask import Blueprint, request, jsonify
from models import get_connection
from flask_jwt_extended import jwt_required

telemetry_bp = Blueprint('telemetry', __name__)


# GET TELEMETRY
@telemetry_bp.route('/telemetry', methods=['GET'])
@jwt_required()  
def get_telemetry():

    device_id = request.args.get('device_id')
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))

    conn = get_connection()
    cur = conn.cursor()

    # CASE 1: filter by device_id
    if device_id:
        cur.execute("""
            SELECT id, device_id, key, value, timestamp
            FROM telemetry
            WHERE device_id=%s
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s;
        """, (device_id, limit, offset))

    # CASE 2: all telemetry
    else:
        cur.execute("""
            SELECT id, device_id, key, value, timestamp
            FROM telemetry
            ORDER BY timestamp DESC
            LIMIT %s OFFSET %s;
        """, (limit, offset))

    data = cur.fetchall()

    cur.close()
    conn.close()

    # format response
    result = []
    for t in data:
        result.append({
            "id": str(t[0]),
            "device_id": str(t[1]),
            "key": t[2],
            "value": t[3],
            "timestamp": str(t[4])
        })

    return jsonify(result), 200