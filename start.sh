#!/bin/bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker webscrapper:webscrapper --bind 0.0.0.0:8000