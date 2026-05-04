"""IAM microservice."""

from app.microservices.iam.app import create_app

__all__ = ["create_app"]