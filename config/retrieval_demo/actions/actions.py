import re
from typing import Optional

from nemoguardrails.actions import action


@action()
async def check_retrieval_sensitive_data(context: Optional[dict] = None):
    """Return True when retrieved chunks appear to include sensitive data."""
    print("===========check_retrieval_sensitive_data=============")
    data = context or {}
    retrieved = data.get("relevant_chunks", "") or ""

    lowered = retrieved.lower()
    keyword_hits = [
        "手机号",
        "联系方式",
        "身份证",
        "邮箱",
        "address",
        "email",
        "phone",
        "财报",
        "住址",
    ]
    if any(k in lowered for k in keyword_hits):
        return True

    # Generic patterns for phone and email.
    phone_pattern = re.compile(r"\b1[3-9]\d{9}\b")
    email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    is_phone = bool(phone_pattern.search(retrieved) or email_pattern.search(retrieved))
    print(f"retrieved----->{retrieved}")
    print(f"-------------->is_phone:  {is_phone}")
    return is_phone
