import os
import time
from datetime import datetime
from croniter import croniter
from main import main
from config.logger import Logger
from config.version import __version__

logger = Logger("entrypoint")

def run_scheduler():
    """
    Runs the main function either once or on a schedule defined by CRON_SCHEDULE.
    """
    cron_schedule = os.environ.get("CRON_SCHEDULE", "")
    if not cron_schedule:
        # If no schedule is set, run main once and exit
        logger.info("CRON_SCHEDULE not set, running once.")
        main()
        return

    # Run once immediately at start
    logger.info(f"Starting MediaFlowrr v{__version__} with cron schedule '{cron_schedule}'")
    logger.info("Running initial check immediately.")
    main()
    
    # Set up cron schedule based on current time
    base = datetime.now()
    cron = croniter(cron_schedule, base)

    while True:
        # Calculate next scheduled run time
        next_run = cron.get_next(datetime)
        sleep_sec = (next_run - datetime.now()).total_seconds()
        logger.info(f"Sleeping for {sleep_sec:.2f} seconds until next run at {next_run}")
        if sleep_sec > 0:
            time.sleep(sleep_sec)
        # Run the main function at the scheduled time
        main()

if __name__ == "__main__":
    # Entry point for the script
    run_scheduler()
