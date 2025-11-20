from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import traceback
import logs_language_generation_unit  as llg
import logs_language_understanding_unit as llu
import uvicorn
import os
from schema import LogsValidationResults, Logs

load_dotenv()
env_path = Path('WorkstreamLogAnalyzer/.env')
load_dotenv(dotenv_path=env_path)


app = FastAPI()

@app.post("/validate-logs/")
async def validate_logs(logs: Logs):

    result_rows = []
    remaining_logs = []
    for row in logs.logs:
        if llu.check_hours_per_task(row.decimal_hours):
            if llu.check_description_len(row.task_description):
                remaining_logs.append(row)
            else:
                status = 'fail'
                reason = "Description is too short."
                result_rows.append({
                    "id": row.id,
                    "status": status,
                    "reason": reason
                })

        else:
            status = 'fail'
            reason = "Each task should not exceed 3 hours of work."
            result_rows.append({
                "id": row.id,
                "status": status,
                "reason": reason
            })
    if len(remaining_logs) > 0:
        # Process remaining logs in groups of 10
        batch_size = 10
        for i in range(0, len(remaining_logs), batch_size):
            batch = remaining_logs[i:i + batch_size]
            try:
                    gpt_results: LogsValidationResults= llg.gpt_check(batch)
                    result_rows.extend(gpt_results.results)

            except Exception as e:
                reason = "Response structure was not correct." + str(e)
                status = "fail"
                traceback.print_exc()
                for row in batch:
                    result_rows.append({
                        "status": status,
                        "reason": reason,
                        "id": row.id
                    })

    return result_rows


# === Entry point ===
def main():
    uvicorn.run("logs_language_processing_unit:app", host=os.getenv("HOST"),
                port=8000, reload=True)

if __name__ == "__main__":
    main()