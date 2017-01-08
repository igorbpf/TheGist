from news import get_summary

def summarize(url):
    title, summary, language = get_summary(url)
    return title, summary
