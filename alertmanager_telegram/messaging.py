from flask import Blueprint
from flask import jsonify
from flask import request
from flask import render_template
from flask import current_app
from telegram.constants import MAX_MESSAGE_LENGTH

from alertmanager_telegram.logging import logger

blueprint = Blueprint("messaging", __name__, template_folder="../templates")


def render(content):
    alerts = content["alerts"]
    content["alert_count"] = len(alerts)

    common_labels = content.get("commonLabels", {})
    common_annotations = content.get("commonAnnotations", {})

    for idx, alert in enumerate(alerts):
        if "labels" in alert:
            labels = alert["labels"]
            for label in common_labels.keys():
                labels.pop(label, None)

        if "annotations" in alert:
            annotations = alert["annotations"]
            for annotation in common_annotations.keys():
                annotations.pop(annotation, None)

    message = render_template("default.html", **content)
    while len(message) > MAX_MESSAGE_LENGTH and len(content["alerts"]) > 0:
        logger.debug("Truncating alerts list (with ellipsis)")
        content["alerts"].pop()
        content["ellipsis"] = True
        message = render_template("default.html", **content)

    if len(message) > MAX_MESSAGE_LENGTH:
        msg = "Message template is too long"
        logger.error(msg)
        return msg

    return message


@blueprint.route("/alerts", methods=["POST"])
def alerts():
    content = request.get_json()

    if "alerts" not in content or "status" not in content:
        logger.warning("Received invalid request")
        return jsonify(status="invalid"), 400

    alert_count = len(content["alerts"])
    alert_status = content["status"]
    chat_id = current_app.config["TELEGRAM_CHAT_ID"]

    logger.info(f"Received {alert_count} alerts (status={alert_status})")
    try:
        text = render(content)
    except Exception:
        logger.exception("Exception in message rendering")
        return jsonify(status="failed"), 500

    try:
        current_app.bot.send_message(
            chat_id=chat_id,
            parse_mode="HTML",
            disable_web_page_preview=True,
            text=text,
        )
    except Exception:
        logger.exception("Exception during sending message")
        return jsonify(status="failed"), 500

    logger.info("Sent message")
    return jsonify(status="success"), 200
