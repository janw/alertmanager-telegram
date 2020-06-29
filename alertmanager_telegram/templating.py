from flask import render_template
from telegram.constants import MAX_MESSAGE_LENGTH

from alertmanager_telegram.logging import logger


def render(content):
    alerts = content["alerts"]

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
