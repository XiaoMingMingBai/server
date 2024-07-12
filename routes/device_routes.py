from flask import Blueprint, request, jsonify
from services.device_service import get_device_status, get_device_history, control_device

device_bp = Blueprint('device', __name__)

@device_bp.route('/', methods=['GET'])
def get_statuses():
    return jsonify(get_device_status())

@device_bp.route('/<device_id>', methods=['GET'])
def get_status(device_id):
    return jsonify(get_device_status(device_id))

@device_bp.route('/<device_id>/history', methods=['GET'])
def get_history(device_id):
    return jsonify(get_device_history(device_id))

@device_bp.route('/<device_id>/actions', methods=['POST'])
def perform_action(device_id):
    data = request.json
    return jsonify(control_device(device_id, data))
