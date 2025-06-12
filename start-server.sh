#!/bin/bash

source .venv/bin/activate
fastapi run tinyfocus/app.py --port 9080 --workers 1
