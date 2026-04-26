from typing import Optional
from nemoguardrails.actions import action

@action()
async def check_input_terms(context: Optional[dict] = None):
    """Check if the input complies with custom policy."""
    user_message = context.get("user_message", "")
    print(f"*************{context}")
    print(f"*************{user_message}")
    # Custom validation logic
    forbidden_words = ["毒品","赌博"]
    for word in forbidden_words:
        if word in user_message:
            return True

    return False


@action(is_system_action=True)
async def check_blocked_terms(context: Optional[dict] = None):
    """Check if bot response contains blocked terms."""
    bot_response = context.get("bot_message", "")

    blocked_terms = ["银行卡密码"]

    for term in blocked_terms:
        if term in bot_response:
            return True  # Term found, block the response

    return False  # No blocked terms found

@action(name="fetch_user_data")
async def get_user_info(user_id: str):
    """Fetch user data from external service."""
    # External API call
    return {"user_id": user_id, "status": "active"}