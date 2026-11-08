from app.core.security import hash_password, hash_token, new_session_token, verify_password


def test_password_hash_roundtrip():
    h = hash_password("s3cret-pass")
    assert h.startswith("$argon2")
    assert verify_password("s3cret-pass", h)
    assert not verify_password("wrong", h)


def test_session_tokens_are_random_and_hashed():
    a, b = new_session_token(), new_session_token()
    assert a != b and len(a) >= 40
    assert hash_token(a) != a.encode() and len(hash_token(a)) == 32
