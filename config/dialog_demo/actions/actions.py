import re
from typing import Optional

from nemoguardrails.actions import action


@action(is_system_action=False)
async def get_current_time():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@action(is_system_action=False)
async def check_forbidden_words(context: dict = None):
    user_message = (context or {}).get("user_message", "")
    pattern = r'制造.*?(?:枪|炸弹|毒药)'
    if re.search(pattern, user_message, re.IGNORECASE):
        return {"contains_blocked": True}
    return {"contains_blocked": False}