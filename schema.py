from pydantic import BaseModel, Field
import random

class LogEntry(BaseModel):
    # DayDetailID: str
    # PersonID: str
    id: int = Field(random.randint(1, 100000))
    TaskLabel: str = Field("Standup")
    CompetencyRoles: str = Field("Software Engineer")
    DecimalHours: float = Field(1.0)
    TaskDescription: str = Field("Stand-up and Team discussions Meeting with colleagues")

class Logs(BaseModel):
    logs: list[LogEntry] = Field(
        [LogEntry(), LogEntry(TaskDescription="Code Review"), LogEntry(TaskDescription="Writing unit tests for new comprehension task for schoolgram's new activity.")]
    )

class ValidationResult(BaseModel):
    id: int
    status: str
    reason: str

class LogsValidationResults(BaseModel):
    results: list[ValidationResult]