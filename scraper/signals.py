from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .utils import load_scraper_scripts

@receiver(post_migrate)
def load_scripts(sender, **kwargs):
    if sender.name == 'scraper':
        load_scraper_scripts()