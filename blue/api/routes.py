from flask import Blueprint, jsonify, request, make_response
from utils import summarize
# from requests.exceptions import Timeout



mod = Blueprint('api',__name__)


@mod.route('/summary', methods=['POST'])
def apiSummarize():
    url = request.form['url']

    result = summarize.apply_async(args=[url])
    return make_response(jsonify(id=result.id), 202)


@mod.route('/_results/<string:job_key>', methods=['GET'])
def get_results(job_key):

    job = summarize.AsyncResult(job_key)

    if job.state == 'PENDING':
        return make_response(jsonify(status='Pending'), 202)

    elif job.state != 'FAILURE':
        #if 'result' in job.info:
        return make_response(jsonify(job.info), 200)

        # else:
        #     return make_response(jsonify(status='Progress...', job=), 202)


    else:
        return make_response(jsonify(error='Bad url.', status=str(job.info)), 400)



    # job = Job.fetch(job_key, connection=conn)
    #
    # if job.is_finished:
    #     if True:
    #         # dummy = Job.result
    #         # title = dummy['title']
    #         # summary = dummy['summary']
    #         # print(title)
    #     # except Timeout:
    #     #     return make_response(jsonify(error="Too long."), 400)
    #     # except:
    #     #     return make_response(jsonify(error="Bad url."), 400)
    #     #return make_response(jsonify(title=title, summary=summary), 200)
    #         return Job.result
    #         #return make_response(jsonify(result=Job.result), 200)
    #
    # else:
    #     return 'NO YET'
