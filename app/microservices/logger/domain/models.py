from enum import Enum
from typing import Optional, Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field

# Base Models
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class UserContext(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier of the user (e.g., UUID)", examples=["user_123"])
    name: Optional[str] = Field(None, description="Name or username associated with the user", examples=["John Doe"])
    ip_address: Optional[str] = Field(None, description="IP address from which the user initiated the action", examples=["192.168.1.1"])

class HttpContext(BaseModel):
    method: Optional[str] = Field(None, description="HTTP verb used for the request (GET, POST, etc.)", examples=["POST"])
    route: Optional[str] = Field(None, description="Endpoint route that was accessed", examples=["/api/v1/auth/login"])
    status_code: Optional[int] = Field(None, description="HTTP status code returned to the client", examples=[200])
    user_agent: Optional[str] = Field(None, description="User-Agent string from the client browser or application")
    ip: Optional[str] = Field(None, description="Client IP address detected by the gateway", examples=["203.0.113.42"])

class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"

# Events
class EventEntry(BaseModel):
    service: str = Field(..., description="Service or application originating the event", examples=["frontend-web"])
    event: str = Field(..., description="Unique event identifier or name", examples=["ui.button_click"])
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC datetime when the event occurred", examples=["2024-01-15T10:30:00Z"])
    user_id: Optional[str] = Field(None, description="Optional identifier for the user", examples=["user_123"])
    session_id: str = Field(..., description="Tracking identifier linking multiple actions", examples=["sess_999"])
    page: Optional[str] = Field(None, description="UI View or page where the event happened", examples=["/dashboard"])
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary JSON payload", examples=[{"button_id": "submit-form", "form_name": "contact"}])

# Logs
class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC datetime", examples=["2024-01-15T10:30:00Z"])
    level: LogLevel = Field(LogLevel.INFO, description="Severity level of the log entry", examples=["INFO"])
    event: str = Field(..., description="Short name classifying the log event", examples=["user.login"])
    message: str = Field(..., description="Detailed textual description of what happened", examples=["User successfully logged in"])
    service: str = Field(..., description="Name of the service emitting this log", examples=["auth-service"])
    environment: str = Field(..., description="Deployment environment", examples=["production"])
    trace_id: Optional[str] = Field(None, description="Correlated trace identifier", examples=["tr_abc123"])
    span_id: Optional[str] = Field(None, description="Specific span identifier within the trace", examples=["sp_456def"])
    user: Optional[UserContext] = Field(default_factory=UserContext, description="User involved in the event")
    http: Optional[HttpContext] = Field(default_factory=HttpContext, description="Technical context of the original request")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary key-value pairs", examples=[{"request_id": "req_123", "duration_ms": 150}])

# Metrics
class MetricEntry(BaseModel):
    service: str = Field(..., description="Service emitting the aggregated metric", examples=["auth-service"])
    name: str = Field(..., description="Standardized name of the metric being recorded", examples=["http.request.duration"])
    type: MetricType = Field(MetricType.COUNTER, description="Type of metric", examples=["histogram"])
    value: float = Field(..., description="The numeric observation", examples=[0.245])
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC datetime", examples=["2024-01-15T10:30:00Z"])
    labels: Dict[str, str] = Field(default_factory=dict, description="Dimensional breakdowns", examples=[{"method": "POST", "status": "200"}])
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary JSON payload", examples=[{"p95": 0.5, "p99": 1.2}])

# Traces
class TraceEntry(BaseModel):
    trace_id: str = Field(..., description="Unique identifier for the entire distributed trace", examples=["tr_abc123def456"])
    span_id: str = Field(..., description="Unique identifier for this specific segment of the trace", examples=["sp_789xyz"])
    parent_span_id: Optional[str] = Field(None, description="ID of the caller span, null if it is the root span", examples=["sp_parent123"])
    name: str = Field(..., description="Human-readable name of the operation being timed", examples=["POST /api/v1/auth/login"])
    start_time: float = Field(..., description="Unix timestamp of when the operation started", examples=[1705315800.123])
    end_time: float = Field(..., description="Unix timestamp of when the operation completed", examples=[1705315800.456])
    status: str = Field(..., description="Outcome status of the operation (ok, error, timeouts)", examples=["ok"])
    service: str = Field(..., description="The microservice or application that executed this span", examples=["auth-service"])
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Key-value pairs for technical metadata", examples=[{"db_query": "SELECT * FROM users", "cache_hit": False}])

# Batch
class BatchEntry(BaseModel):
    logs: List[LogEntry] = Field(default_factory=list, description="Array of zero or more log entries")
    traces: List[TraceEntry] = Field(default_factory=list, description="Array of zero or more distributed tracing spans")
    metrics: List[MetricEntry] = Field(default_factory=list, description="Array of zero or more mathematical metrics")
    events: List[EventEntry] = Field(default_factory=list, description="Array of zero or more user or system events")
