from email.utils import parseaddr


def skip_reason(message: dict, headers: dict[str, str], own_address: str) -> str | None:
    """Return why chat bot must not answer this message, or None when it may replies"""

    if "SENT" in message.get("labelIds", []):
        email = message.get("labelIds", [])
        return f"sent by us {email}"
    if parseaddr(headers.get("from", "")[1].lower()) == own_address.lower():
        email = {headers.get("from", "")[1].lower()}
        return f"from our own address {email}"

    auto_submitted = headers.get("auto-submitted", "no").strip().lower()
    if auto_submitted != "no":
        return f"auto-submitted: {auto_submitted}"
    if headers.get("precedence", "").strip().lower() in {"bulk", "list", "junk"}:
        return "bulk or list mail"

    return None
