from news import get_summary
from blue import celery

@celery.task
def summarize(url):
    title, summary, language = get_summary(url)
    return {'title': title, 'summary': summary}
