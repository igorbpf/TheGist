from flask import Blueprint, jsonify, request
from utils import summarize
from flask_cors import CORS, cross_origin

mod = Blueprint('api',__name__)
cors = CORS(mod)

@mod.route('/summary', methods=['POST'])
@cross_origin()
def apiSummarize():
    url = request.form['url']
    try:
        title, summary = summarize(url)
    except:
        summary = None
        title = None
    return jsonify(title=title, summary=summary)
