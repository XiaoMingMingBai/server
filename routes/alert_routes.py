from flask import Blueprint, request, jsonify
from services.alert_service import get_alerts, create_alert

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/', methods=['GET'])
def get_all_alerts():
    return jsonify(get_alerts())

@alert_bp.route('/', methods=['POST'])
def create_new_alert():
    data = request.json
    return jsonify(create_alert(data))
