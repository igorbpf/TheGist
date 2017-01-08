from flask import Blueprint, render_template, request, url_for
from utils import summarize

mod = Blueprint('site',__name__,template_folder="templates")

@mod.route('/', methods=['GET','POST'])
def mainPage():
    status = False
    if request.method == 'POST':
        url = request.form['url']
        try:
            title, summary = summarize(url)
        except:
            summary = None
            title = None
            status = True
        return render_template('index.html', status=status, summary=summary, title=title)
    return render_template('index.html')

