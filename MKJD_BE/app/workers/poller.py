from sqlalchemy.orm import Session


def poll_targets(db: Session, youtube_client, model_service) -> None:
    raise NotImplementedError("Polling worker is not wired yet")
