import re
from typing import Optional

from nemoguardrails.actions import action


@action()
async def allow_user_lookup(context: Optional[dict] = None):
    """Allow execution only for approved IDs in demo."""
    user_message = (context or {}).get("user_message", "")
    return "U1001" in user_message


@action()
async def check_input_terms(context: Optional[dict] = None):
    """Return True when blocked terms are found."""
    user_message = (context or {}).get("user_message", "")
    # 匹配“删除...文件”或“删除...数据库”，中间任意字符（非贪婪）
    pattern = r'删除.*?(?:文件|数据库)'
    # 编译正则，忽略大小写（通常中文不区分大小写，但加上也无妨）
    regex = re.compile(pattern, re.IGNORECASE)
    return bool(regex.search(user_message))


@action(name="fetch_user_data")
async def get_user_info(user_id: str):
    return {"user_id": user_id, "status": "active", "level": "gold"}
