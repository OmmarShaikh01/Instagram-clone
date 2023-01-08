#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram_clone.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # Available subcommands:
    #
    # [auth]
    #     changepassword
    #     createsuperuser
    #
    # [contenttypes]
    #     remove_stale_contenttypes
    #
    # [django]
    #     check
    #     compilemessages
    #     createcachetable
    #     dbshell
    #     diffsettings
    #     dumpdata
    #     flush
    #     inspectdb
    #     loaddata
    #     makemessages
    #     makemigrations
    #     migrate
    #     optimizemigration
    #     sendtestemail
    #     shell
    #     showmigrations
    #     sqlflush
    #     sqlmigrate
    #     sqlsequencereset
    #     squashmigrations
    #     startapp
    #     startproject
    #     test
    #     testserver
    #
    # [sessions]
    #     clearsessions
    #
    # [staticfiles]
    #     collectstatic
    #     findstatic
    #     runserver
    main()
