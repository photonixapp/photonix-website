import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


def notify_mattermost(
    text: str,
    alias: str = "Epix Bot",
    webhook_url: Optional[str] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
) -> bool:
    """
    Send a notification to Mattermost (only in production environment).

    Args:
        text: The message text to send
        alias: The bot alias to display (default: "Epix Bot")
        webhook_url: Optional webhook URL (defaults to MATTERMOST_WEBHOOK_URL env var)
        attachments: Optional list of attachment dictionaries. Each attachment can contain:
            - title: Attachment title
            - title_link: URL for the title to link to
            - text: Main attachment text content
            - image_url: URL of an image to display
            - color: Hex color code for the attachment border (e.g. "#36a64f")
            - fields: List of field objects with:
                - title: Field title
                - value: Field value
                - short: Boolean, whether field should display inline (default: False)
            - author_name: Name of the author
            - author_link: URL to link the author name to
            - author_icon: URL of author icon/avatar
            - thumb_url: URL of thumbnail image
            - footer: Footer text
            - footer_icon: URL of footer icon
            - ts: Timestamp (Unix time)

    Example attachment:
        {
            "title": "Deployment Status",
            "color": "#36a64f",
            "fields": [
                {"title": "Environment", "value": "production", "short": True},
                {"title": "Version", "value": "v1.2.3", "short": True}
            ],
            "footer": "Deploy Bot",
            "ts": 1234567890
        }

    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    if not webhook_url:
        webhook_url = os.getenv("MATTERMOST_WEBHOOK_URL")

    if not webhook_url:
        logger.warning("No Mattermost webhook URL configured")
        return False

    payload = {
        "alias": alias,
        "text": text,
    }

    if attachments:
        payload["attachments"] = attachments

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        if response.status_code == 200:
            logger.info(f"Rocket Chat notification sent successfully: {text}")
            return True
        else:
            logger.error(f"Failed to send Rocket Chat notification. Status: {response.status_code}, Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending Rocket Chat notification: {e}")
        return False
