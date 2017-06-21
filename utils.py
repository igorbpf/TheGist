from news import get_summary, get_summary_text
from blue import celery

@celery.task
def summarize(url):
    title, summary, language = get_summary(url)
    return {'title': title, 'summary': summary}


@celery.task
def summarize_text(text, size):
    if size == 'Small':
        bit = 0.25
    elif size == 'Medium':
        bit = 0.50
    elif size == 'Big':
        bit = 0.75
    summary = get_summary_text(text, bit)
    return {'summary': summary}
