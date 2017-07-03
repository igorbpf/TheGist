# TheGist
A Web app for automatic summarization

This app is a miscellaneous of different topics: from web scraping to Natural Language Processing. 
It uses Natural Language Processing and Machine learnning to process and summarize the text. TheGist has a chrome extension
available at https://github.com/igorbpf/TheGist-extension. 

In order to use it, open 3 terminal tabs.

First of all, start a new virtual environment (python 3 used here) and pip install -r requirements.txt to install the dependencies;

Start redis in one of them with redis-server (https://redis.io/download);

In the order 2 tabs, set environment variables:

export APP_SETTINGS='config.DevelopmentConfig'

export REDIS_URL='redis://localhost:6379' (if redis is serving on other port, change 6379 for the correct port)

Fire up celery in one of the tabs with: celery worker -A blue.celery --loglevel=info

In the last tab run the app with python run.py

The app will listen to port 5000. Browse it at localhost:5000

Live demo at http://thegist.herokuapp.com

