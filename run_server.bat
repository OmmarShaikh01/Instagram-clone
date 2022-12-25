@echo off
set ENV_FOR_DYNACONF=TESTING
.\.venv\Scripts\python.exe -m manage makemigrations
.\.venv\Scripts\python.exe -m manage migrate
.\.venv\Scripts\python.exe -m manage runserver
