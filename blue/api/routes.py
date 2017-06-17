from flask import Blueprint, jsonify, request, make_response
from utils import summarize
from requests.exceptions import Timeout


mod = Blueprint('api',__name__)

@mod.route('/summary', methods=['POST'])
def apiSummarize():
    url = request.form['url']
    try:
        title, summary = summarize(url)
    except Timeout:
        return make_response(jsonify(error="Too long."), 400)
    except:
        return make_response(jsonify(error="Bad url."), 400)
    return make_response(jsonify(title=title, summary=summary), 200)
