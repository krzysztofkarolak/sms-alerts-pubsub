import os
import json
from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from google.oauth2 import service_account

app = Flask(__name__)

project_id = os.environ.get("GOOGLE_PROJECT_NAME")
topic_id = os.environ.get("PUBSUB_TOPIC_NAME")

sa_key_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
if not sa_key_json:
    raise ValueError("Service account key not found in the environment variable.")

sa_key_dict = json.loads(sa_key_json)
credentials = service_account.Credentials.from_service_account_info(sa_key_dict)

publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, topic_id)

default_phone_number = os.environ.get("DEFAULT_PHONE_NUMBER")

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    try:
        data = request.json

        alert_message = data.get("message", "An alert was triggered.")
        phone_number = data.get("phone_number", default_phone_number)

        pubsub_message = {
            "phone_number": phone_number,
            "text_message": alert_message
        }

        future = publisher.publish(topic_path, json.dumps(pubsub_message).encode("utf-8"))
        print(f"Published message to {topic_id} with phone number {phone_number}")

        return jsonify({"status": "success", "message": "Alert sent to Pub/Sub"}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)