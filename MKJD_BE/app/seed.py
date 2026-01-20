import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.db.session import SessionLocal
from app.db.models.enums import TargetType
from app.services import model_metrics as metrics_service
from app.services import oauth as oauth_service
from app.services import pipeline as pipeline_service
from app.services import settings as settings_service
from app.services import targets as targets_service
from app.db.models.model_metrics import ModelMetrics
from app.db.models.monitoring_target import MonitoringTarget


def seed_base(db) -> None:
    settings_service.get_settings(db)
    pipeline_service.get_pipeline_status(db)
    oauth_service.get_oauth_account(db)


def seed_sample(db) -> None:
    if db.query(ModelMetrics).count() == 0:
        metrics_service.create_metric(
            db,
            {
                "model_name": "IndoBERTweet",
                "version": "v1.2.0",
                "precision": 0.93,
                "recall": 0.88,
                "f1": 0.9,
                "pr_auc": 0.91,
                "avg_latency_ms": 220,
                "is_active": True,
            },
        )

    if db.query(MonitoringTarget).count() == 0:
        targets_service.create_target(
            db,
            {
                "type": TargetType.CHANNEL,
                "label": "Kanal YouTube Saya",
                "target": "UC0FILAMSI123",
                "filter": "slot, gacor, bonus",
                "active": True,
            },
        )
        targets_service.create_target(
            db,
            {
                "type": TargetType.VIDEO,
                "label": "Podcast Ep 1",
                "target": "vid_podcast_1",
                "filter": "promo, link",
                "active": True,
            },
        )
        targets_service.create_target(
            db,
            {
                "type": TargetType.VIDEO,
                "label": "Tutorial",
                "target": "vid_tutorial_1",
                "filter": "daftar, deposit",
                "active": True,
            },
        )
        targets_service.create_target(
            db,
            {
                "type": TargetType.VIDEO,
                "label": "Live Stream",
                "target": "vid_live_1",
                "filter": "vip, bonus",
                "active": False,
            },
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed MKJD database")
    parser.add_argument("--sample", action="store_true", help="Insert sample rows")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        seed_base(db)
        if args.sample:
            seed_sample(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
