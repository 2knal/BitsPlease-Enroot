#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsBuster.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    # print(PROJECT_ROOT)
    # exec(open(PROJECT_ROOT + '/app/scraping/NewsScraper.py').read())
    execute_from_command_line(sys.argv)
