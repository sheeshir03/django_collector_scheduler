import datetime
from celery import shared_task
from .models import ScraperTask, ScrapedData, ScraperLog
import subprocess
import sys
import os
from django.utils import timezone
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def run_scraper_task(task_id):
    try:
        task = ScraperTask.objects.get(id=task_id)
        task.status = 'running'
        print("Running")
        task.save()
        logger.info(f'Task {task.id} has started: {task.name}')

        script_path = os.path.abspath(task.script.script_path)
        allowed_dir = os.path.abspath(settings.SCRAPER_SCRIPTS_DIR)

        if not script_path.startswith(allowed_dir):
            raise PermissionError(f"Script Not Found In {settings.SCRAPER_SCRIPTS_DIR}. Invalid Script Location!")
        
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script Not Found: {script_path}")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        log_filename = f"{task.name}_{task.id}_{timestamp}.log"
        log_file_path = os.path.join(settings.SCRAPER_LOGS_DIR, log_filename) # Log file path
        
        # Execute the script using subprocess and redirect output to log file
        with open(log_file_path, 'w') as log_file:
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=log_file,
                stderr=subprocess.STDOUT,
                cwd=settings.SCRAPER_SCRIPTS_DIR
            )
            process.communicate()

        # stdout, stderr = process.communicate()

        log_entry = ScraperLog.objects.create(
            task=task,
            log_file_path= log_file_path,
            created_at = timezone.now()

        )
        logger.info(f"Task {task.id} log saved to {log_file_path}")

        if process.returncode !=0:
            task.status = 'failed'
            task.save()
            logger.error(f"Task {task.id} failed with return code {process.returncode}.")
            return
        

                # Read the log file to extract JSON data
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()
        
        # Attempt to extract JSON data from the log
        try:
            # Assuming the last JSON object in the log is the scraped data
            json_data = extract_scraped_data_from_logs(log_content)
            scraped_data = json.loads(json_data)
        except json.JSONDecodeError:
            raise ValueError("Scraper script did not return valid JSON.")
        except Exception as e:
            raise ValueError(f"Error extracting JSON from logs: {str(e)}")
        

        # Save to Scraper Data table
        ScrapedData.objects.create(
            task=task,
            data=scraped_data,
            scraped_at=timezone.now()
        )

        logger.info(f"Task {task.id} completed successfully.")

        task.status = 'completed'
        task.save()

    except ScraperTask.DoesNotExist:
        logger.error(f"ScraperTask with ID {task_id} does not exist.")
    except Exception as e:
        # Attempt to fetch the task to update its status
        try:
            task = ScraperTask.objects.get(id=task_id)
            task.status = 'failed'
            task.save()
            # Optionally, create a log entry for the error
            ScraperLog.objects.create(
                task=task,
                log_file_path='',
                created_at=timezone.now()
            )
        except ScraperTask.DoesNotExist:
            logger.error(f"ScraperTask with ID {task_id} does not exist for error handling.")
        logger.exception(f"Task {task_id} encountered an error: {str(e)}")

def extract_scraped_data_from_logs(log_content):
    import re
    json_pattern = re.compile(r'\{.*\}', re.DOTALL)
    matches = json_pattern.findall(log_content)
    if not matches:
        raise ValueError("No JSON data found in logs.")
    # Return the last JSON object found
    return matches[-1]