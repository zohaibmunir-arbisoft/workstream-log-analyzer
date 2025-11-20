from pydantic import BaseModel, Field
import random

class LogEntry(BaseModel):
    # DayDetailID: str
    # PersonID: str
    id: int = Field(random.randint(1, 100000))
    task_label: str = Field("Standup")
    competency_roles: str = Field("Software Engineer")
    decimal_hours: float = Field(1.0)
    task_description: str = Field("Stand-up and Team discussions Meeting with colleagues")

class Logs(BaseModel):
    logs: list[LogEntry] = Field(
        [LogEntry(), LogEntry(task_description="Code Review"), LogEntry(task_description="Writing unit tests for new comprehension task for schoolgram's new activity.")]
    )

class ValidationResult(BaseModel):
    id: int
    status: str
    reason: str

class LogsValidationResults(BaseModel):
    results: list[ValidationResult]