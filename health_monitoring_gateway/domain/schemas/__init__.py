"""Pydantic DTOs aligned with health_monitoring/backend/app/schemas for OpenAPI parity."""

from health_monitoring_gateway.domain.schemas.aggregations import (
    MeasurementAggregation,
    MeasurementAggregationList,
)
from health_monitoring_gateway.domain.schemas.common import (
    CountResponse,
    JsonObjectResponse,
    LinkTypeToGroupResponse,
    MeasureTypeStatsResponse,
    MessageResponse,
    BackendHealthStatusResponse,
    BackendVersionResponse,
)
from health_monitoring_gateway.domain.schemas.measure_groups import (
    MeasureGroupCreate,
    MeasureGroupRead,
)
from health_monitoring_gateway.domain.schemas.measure_type_groups import (
    MeasureTypeGroupCreate,
    MeasureTypeGroupRead,
    MeasureTypeGroupRelation,
)
from health_monitoring_gateway.domain.schemas.measure_types import (
    MeasureTypeCreate,
    MeasureTypeRead,
)
from health_monitoring_gateway.domain.schemas.measurements import (
    MeasurementCreate,
    MeasurementRead,
)
from health_monitoring_gateway.domain.schemas.person import (
    PersonCreate,
    PersonRead,
    PersonUpdate,
)
from health_monitoring_gateway.domain.schemas.units import UnitCreate, UnitRead

__all__ = [
    "CountResponse",
    "JsonObjectResponse",
    "LinkTypeToGroupResponse",
    "MeasureTypeStatsResponse",
    "MeasurementAggregation",
    "MeasurementAggregationList",
    "MeasurementCreate",
    "MeasurementRead",
    "MeasureGroupCreate",
    "MeasureGroupRead",
    "MeasureTypeCreate",
    "MeasureTypeGroupCreate",
    "MeasureTypeGroupRead",
    "MeasureTypeGroupRelation",
    "MeasureTypeRead",
    "MessageResponse",
    "BackendHealthStatusResponse",
    "BackendVersionResponse",
    "PersonCreate",
    "PersonRead",
    "PersonUpdate",
    "UnitCreate",
    "UnitRead",
]
