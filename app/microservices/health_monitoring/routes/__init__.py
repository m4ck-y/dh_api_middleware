"""Health Monitoring routes."""

from app.microservices.health_monitoring.routes import (
    batch,
    measure_groups,
    measure_types,
    measurements,
    monitoring_backend,
    people,
    relations,
    reports,
    units,
)

__all__ = [
    "batch",
    "measure_groups",
    "measure_types",
    "measurements",
    "monitoring_backend",
    "people",
    "relations",
    "reports",
    "units",
]
