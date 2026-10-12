"""SQLite persistence, local PIN hashing, and authorization primitives."""

from core.db.database import create_session_factory, create_sqlite_engine, initialize_database
from core.db.models import Role, SessionStatus, TraineeEventRecord, TrainingSessionRecord, User
from core.db.security import AuthorizationError, PinValidationError, hash_pin, verify_pin

__all__ = [
    "AuthorizationError",
    "PinValidationError",
    "Role",
    "SessionStatus",
    "TraineeEventRecord",
    "TrainingSessionRecord",
    "User",
    "create_session_factory",
    "create_sqlite_engine",
    "hash_pin",
    "initialize_database",
    "verify_pin",
]
