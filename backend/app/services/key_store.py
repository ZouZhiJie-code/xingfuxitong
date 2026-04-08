from __future__ import annotations

import base64
import os
from hashlib import sha256
from threading import Lock

from cryptography.fernet import Fernet

_STORE: dict[str, bytes] = {}
_LOCK = Lock()


def _fernet() -> Fernet:
    secret = os.getenv("KEY_ENCRYPTION_SECRET", "local-dev-only-secret")
    key = base64.urlsafe_b64encode(sha256(secret.encode("utf-8")).digest())
    return Fernet(key)


def save_minimax_key(user_id: str, api_key: str) -> None:
    token = _fernet().encrypt(api_key.encode("utf-8"))
    with _LOCK:
        _STORE[user_id] = token


def get_minimax_key(user_id: str) -> str | None:
    with _LOCK:
        token = _STORE.get(user_id)
    if not token:
        return None
    return _fernet().decrypt(token).decode("utf-8")


def delete_minimax_key(user_id: str) -> None:
    with _LOCK:
        _STORE.pop(user_id, None)


def has_minimax_key(user_id: str) -> bool:
    with _LOCK:
        return user_id in _STORE
