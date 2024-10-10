# Django Collector Scheduler

Django Collector Scheduler is a robust Django app designed to manage and automate the scheduling of web scraping tasks. Easily set up recurring or one-time schedules for web scrapers through an intuitive admin interface. Perfect for automating data collection workflows.

## Features

- **Web Scraper Management**: Add, edit, and manage web scrapers via the Django admin panel.
- **Flexible Scheduling**: Supports one-time and recurring schedules with custom intervals.
- **Admin-Friendly UI**: Enhanced admin forms with date-time pickers for selecting start and end dates.
- **Cascading Deletes**: Automatically removes schedules when the associated scraper is deleted.
- **Search & Filter**: Search scrapers and schedules by name, or filter schedules by type.

## Installation

1. Add `django_collector_scheduler` to your `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        ...,
        'django_collector_scheduler',
        ...,
    ]
    ```

2. Run the database migrations:
    ```bash
    python manage.py migrate
    ```

3. Access and manage scrapers and schedules via the Django admin interface.

## Usage

1. **Create a Web Scraper**: Navigate to the `WebScraper` model in the admin panel, and add new scrapers by providing a name, script path, and description.
2. **Schedule a Task**: Define a schedule for your scraper by setting the start/end dates, schedule type (one-time or recurring), and interval in the `Schedule` model.

## Roadmap

- **Task Monitoring**: Add logging to track task execution and status.
- **Notification System**: Implement notifications for completed or failed scraping tasks.
- **API Integration**: Provide an API for programmatically managing scrapers and schedules.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to help improve this project.

## License

This project is licensed under the MIT License.
