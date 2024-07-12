from flask_pymongo import PyMongo
from datetime import datetime

def get_device_status(device_id=None):
    if device_id:
        status = mongo.db.statuses.find_one({'device_id': device_id}, sort=[('timestamp', -1)])
        return status
    else:
        statuses = mongo.db.statuses.find().sort('timestamp', -1).limit(10)
        return list(statuses)

def get_device_history(device_id):
    history = mongo.db.statuses.find({'device_id': device_id}).sort('timestamp', -1)
    return list(history)

def control_device(device_id, action):
    # 这里可以添加设备控制逻辑
    return {"status": "success", "message": f"Action {action['action']} performed on device {device_id}"}
