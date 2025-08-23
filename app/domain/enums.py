from enum import Enum


class FineStatus(Enum):
    UNPAID = "unpaid"
    SUSPENDED = "suspended"


class RiskClassification(Enum):
    NORMAL = "normal"
    SPECIAL_MONITORING = "special_monitoring"
    WITH_PROBLEMS = "with_problems"
    HIGH_RISK_OF_INSOLVENCY = "high_risk_of_insolvency"
    IRRECOVERABLE = "irrecoverable"


class RiskLevel(Enum):
    NORMAL = "normal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    IRRECOVERABLE = "irrecoverable"


class RequestType(Enum):
    SINGLE = "single"
    BATCH = "batch"
    MONITORING = "monitoring"


class RequestStatus(Enum):
    SUCCESSFUL = "successful"
    ERROR = "error"
    TIMEOUT = "timeout"
