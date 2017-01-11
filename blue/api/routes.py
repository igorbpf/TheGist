from flask import Blueprint, jsonify, request
from utils import summarize


mod = Blueprint('api',__name__)

@mod.route('/', methods=['POST'])
def apiSummarize():
    url = request.form['url']
    try:
        title, summary = summarize(url)
    except:
        summary = None
        title = None
    return jsonify(title=title, summary=summary)




