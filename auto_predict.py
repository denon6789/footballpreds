import time
import subprocess
from datetime import datetime

# Run main.py every day at a specified hour (e.g., 08:00 UTC)
RUN_HOUR = 8

while True:
    now = datetime.utcnow()
    if now.hour == RUN_HOUR and now.minute == 0:
        print(f"[{now}] Running football score prediction...")
        subprocess.run(["python", "main.py"])
        print(f"[{now}] Prediction complete. Next run in 24 hours.")
        time.sleep(60)  # Wait a minute to avoid running multiple times in the same minute
    else:
        time.sleep(30)  # Check every 30 seconds
