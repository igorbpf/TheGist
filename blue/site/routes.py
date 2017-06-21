from flask import Blueprint, render_template, request, url_for, make_response, jsonify
from utils import summarize_text

mod = Blueprint('site',__name__,template_folder="templates")


@mod.route('/', methods=['GET'])
def mainPage():
    return render_template('index.html')

@mod.route('/_summary', methods=['POST'])
def apiSummarize():
    size = request.form['size']
    text = request.form['text']

    result = summarize_text.apply_async(args=[text, size])
    return make_response(jsonify(id=result.id), 202)


@mod.route('/_summary/<string:job_key>', methods=['GET'])
def get_results(job_key):

    job = summarize_text.AsyncResult(job_key)

    if job.state == 'PENDING':
        return make_response(jsonify(status='Pending'), 202)

    elif job.state != 'FAILURE':
        #if 'result' in job.info:
        return make_response(jsonify(job.info), 200)

        # else:
        #     return make_response(jsonify(status='Progress...', job=), 202)


    else:
        return make_response(jsonify(error='Bad url.', status=str(job.info)), 400)
