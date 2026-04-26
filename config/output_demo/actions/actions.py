import re
from typing import Optional

from nemoguardrails.actions import action


@action(is_system_action=True)
async def check_blocked_terms(context: Optional[dict] = None):
    """Return True when blocked terms are found in bot response."""
    """Return True when blocked terms are found."""
    user_message = (context or {}).get("user_message", "")
    pattern = r'服务器.*?(?:地址|密码|vpn|账号|部署路径)'
    regex = re.compile(pattern, re.IGNORECASE)
    return bool(regex.search(user_message))
