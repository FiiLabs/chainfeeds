

jwt_revoked_blocklist = {}

def check_if_token_is_revoked(jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_revoked_blocklist.get(jti)
    return token_in_redis is not None

def revoke_token(jti: str):
    jwt_revoked_blocklist[jti] = True