from sqlalchemy.orm import Session

from app.db.models.oauth_account import OAuthAccount

DEFAULT_OAUTH_ID = "default"


def get_oauth_account(db: Session) -> OAuthAccount:
    instance = db.get(OAuthAccount, DEFAULT_OAUTH_ID)
    if instance:
        return instance
    instance = OAuthAccount(id=DEFAULT_OAUTH_ID, connected=False, permission_granted=False)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_oauth_account(db: Session, patch: dict) -> OAuthAccount:
    instance = get_oauth_account(db)
    for key, value in patch.items():
        if hasattr(instance, key) and value is not None:
            setattr(instance, key, value)
    db.commit()
    db.refresh(instance)
    return instance
