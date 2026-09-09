from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

alerts = []


@app.get("/")
def home():
    return jsonify({
        "system": "Smart Flood Alert API",
        "status": "online",
        "message": "Flood emergency response system is running"
    })


@app.get("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.post("/api/alerts")
def create_alert():
    data = request.get_json(silent=True) or {}

    message = data.get("message")
    location = data.get("location")
    severity = data.get("severity", "HIGH").upper()

    if not message or not location:
        return jsonify({
            "error": "message and location are required"
        }), 400

    if severity not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        return jsonify({
            "error": "Invalid severity"
        }), 400

    alert = {
        "id": str(uuid.uuid4()),
        "message": message,
        "location": location,
        "severity": severity,
        "status": "ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }

    alerts.append(alert)

    return jsonify({
        "success": True,
        "alert": alert
    }), 201


@app.get("/api/alerts")
def get_alerts():
    return jsonify({
        "count": len(alerts),
        "alerts": alerts
    })


@app.get("/api/alerts/<alert_id>")
def get_alert(alert_id):

    for alert in alerts:
        if alert["id"] == alert_id:
            return jsonify(alert)

    return jsonify({
        "error": "Alert not found"
    }), 404


@app.patch("/api/alerts/<alert_id>")
def update_alert(alert_id):

    for alert in alerts:

        if alert["id"] == alert_id:

            data = request.get_json(silent=True) or {}

            status = data.get("status")

            if status not in ["ACTIVE", "ACKNOWLEDGED", "RESOLVED"]:
                return jsonify({
                    "error": "Invalid status"
                }), 400

            alert["status"] = status

            return jsonify({
                "success": True,
                "alert": alert
            })

    return jsonify({
        "error": "Alert not found"
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
