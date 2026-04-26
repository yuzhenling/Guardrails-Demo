import re
from typing import Optional

from nemoguardrails.actions import action


@action()
async def check_input_terms(context: Optional[dict] = None):
    """Return True when blocked terms are found."""
    user_message = (context or {}).get("user_message", "")
    pattern = r'.*?(?:枪|子弹|炸弹|火药|王水|气弹枪)'
    regex = re.compile(pattern, re.IGNORECASE)
    return bool(regex.search(user_message))
