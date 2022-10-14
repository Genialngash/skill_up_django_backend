#!/bin/bash
/opt/venv/bin/celery -A core.settings worker -l INFO
