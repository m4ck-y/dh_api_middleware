"""Health Monitoring domain schemas."""

from app.shared.domain import (
    ApiResponse,
    PaginationResponse,
    BackendHealthStatusResponse,
    BackendVersionResponse,
    CountResponse,
    JsonObjectResponse,
    MessageResponse,
)
from app.microservices.health_monitoring.domain.measure_group import (
    MeasureGroupCreate,
    MeasureGroupRead,
)
from app.microservices.health_monitoring.domain.measure_type import (
    MeasureTypeCreate,
    MeasureTypeRead,
)
from app.microservices.health_monitoring.domain.measure_type_group import (
    LinkTypeToGroupResponse,
    MeasureTypeGroupCreate,
    MeasureTypeGroupRead,
    MeasureTypeGroupRelation,
)
from app.microservices.health_monitoring.domain.measurement import (
    MeasurementAggregation,
    MeasurementCreate,
    MeasurementRead,
    MeasureTypeStatsResponse,
)
from app.microservices.health_monitoring.domain.person import (
    PersonCreate,
    PersonRead,
    PersonUpdate,
)
from app.microservices.health_monitoring.domain.unit import (
    UnitCreate,
    UnitRead,
)

__all__ = [
    # API Response
    "ApiResponse",
    "PaginationResponse",
    # Person
    "PersonCreate",
    "PersonRead",
    "PersonUpdate",
    # Measurement
    "MeasurementCreate",
    "MeasurementRead",
    "MeasurementAggregation",
    "MeasureTypeStatsResponse",
    # MeasureType
    "MeasureTypeCreate",
    "MeasureTypeRead",
    # MeasureGroup
    "MeasureGroupCreate",
    "MeasureGroupRead",
    # MeasureTypeGroup
    "MeasureTypeGroupCreate",
    "MeasureTypeGroupRead",
    "MeasureTypeGroupRelation",
    "LinkTypeToGroupResponse",
    # Unit
    "UnitCreate",
    "UnitRead",
    # Common
    "CountResponse",
    "MessageResponse",
    "BackendHealthStatusResponse",
    "BackendVersionResponse",
    "JsonObjectResponse",
]
