#!/usr/bin/python
from django.core.management import execute_manager

# put apps dir in python path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

try:
    import settings  # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the" \
        " directory containing %r. It appears you've customized things.\n" \
        "You'll have to run django-admin.py, passing it your settings" \
        " module.\n(If the file settings.py does indeed exist, it's" \
        " causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)


# Custom application commands
def command_fetch_hn():
    """ Scrape hacker news items """
    from articles.parsers.hackernews import HackerNews
    inst = HackerNews()
    inst.update_items()

# Main processing
if __name__ == "__main__":
    commands = {
        'fetch_hn': command_fetch_hn,
    }
    param = len(sys.argv) > 1 and sys.argv[1]

    if param in commands:
        os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
        commands[param]()
    else:
        execute_manager(settings)
