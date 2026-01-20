import enum


class Decision(str, enum.Enum):
    PUBLISHED = "PUBLISHED"
    HELD = "HELD"
    REJECTED = "REJECTED"
    BORDERLINE = "BORDERLINE"


class YTStatus(str, enum.Enum):
    PUBLISHED = "published"
    HELD_FOR_REVIEW = "heldForReview"
    REJECTED = "rejected"


class TargetType(str, enum.Enum):
    CHANNEL = "CHANNEL"
    VIDEO = "VIDEO"


class PipelineState(str, enum.Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
