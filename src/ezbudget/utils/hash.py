import hashlib


def get_hashed_password(password: str) -> str:
    """Return the hashed string from a given password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    verify_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if verify_hash == hashed_password:
        return True
    else:
        return False
