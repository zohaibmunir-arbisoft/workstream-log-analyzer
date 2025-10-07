from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from typing import List
import traceback
import logs_language_generation_unit  as llg
import logs_language_understanding_unit as llu
import uvicorn
import os
from pydantic import Field

load_dotenv()
env_path = Path('WorkstreamLogAnalyzer/.env')
load_dotenv(dotenv_path=env_path)


app = FastAPI()



# === Request model ===
class LogEntry(BaseModel):
    # DayDetailID: str
    # PersonID: str
    TaskLabel: str = Field("Standup")
    CompetencyRoles: str = Field("Software Engineer")
    DecimalHours: float = Field(1.0)
    TaskDescription: str = Field("Stand-up and Team discussions Meeting with colleagues")

@app.post("/validate-logs/")
async def validate_logs(logs: List[LogEntry]):

    result_row = {}
    for row in logs:
        hours_per_task_rule =  llu.check_hours_per_task(row.DecimalHours)

        if hours_per_task_rule:
            if llu.check_description_len(row.TaskDescription):
                try:
                    gpt_result = llg.gpt_check(row.TaskDescription)
                    reason = gpt_result.get("reason", "")
                    status = gpt_result.get("status", "")

                    result_row = {
                        "description": row.TaskDescription,
                        "status": status,
                        "reason": reason
                    }

                except Exception as e:
                    reason = "Response structure was not correct." + str(e)
                    status = "fail"
                    traceback.print_exc()
                    result_row = {
                        "description": row.TaskDescription,
                        "status": status,
                        "reason": reason
                    }
            else:
                status = 'fail'
                reason = "Description is too short."
                result_row = {
                    "description": row.TaskDescription,
                    "status": status,
                    "reason": reason
                }

        else:
            status = 'fail'
            reason = "Each task should not exceed 3 hours of work."
            result_row = {
                "description": row.TaskDescription,
                "status": status,
                "reason": reason
            }

    return result_row



# === Entry point ===
def main():
    uvicorn.run("logs_language_processing_unit:app", host=os.getenv("HOST"),
                port=8000, reload=True)

if __name__ == "__main__":
    main()