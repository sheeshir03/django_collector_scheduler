import os
import hashlib
from django.conf import settings
from .models import ScraperScript

def discover_scraper_scripts():
    scripts_dir = settings.SCRAPER_SCRIPTS_DIR
    scripts = []
    for filename in os.listdir(scripts_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            script_name = filename[:-3]  # Remove .py extension
            script_path = os.path.join(scripts_dir, filename)
            scripts.append({
                'name': script_name,
                'path': script_path,
            })
    return scripts

def load_scraper_scripts():
    existing_scripts = ScraperScript.objects.values_list('name', flat=True)
    scripts = discover_scraper_scripts()
    for script in scripts:
        if script['name'] not in existing_scripts:
            ScraperScript.objects.create(
                name=script['name'],
                description=f"Scraper script: {script['name']}",
                script_path=script['path']
            )
