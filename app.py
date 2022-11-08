import os
import textwrap
import os
from uuid import uuid4

import openai
import humanloop as hl
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

hl.init(
    api_key=os.getenv('HUMANLOOP_API_KEY'),
    provider_api_keys={"OpenAI":os.getenv("OPENAI_API_KEY")}
)




@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        result=request.args.get("result"),
        log_id=request.args.get("log_id"),
        feedback=request.args.get("feedback"),
        copied=request.args.get("copied", False),
    )


@app.route("/get-question", methods=["POST"])
def get_question():
    # Make the request to GPT-3
    expert = request.form["Expert"]
    topic = request.form["Topic"]

    generation = hl.generate(
        project="LearnAnythingFromAnyone",
        inputs={
            "expert": expert,
            "topic": topic
    }
)
    log_id = generation.logs[0].id
    result = generation.logs[0].output

    return redirect(url_for("index", result=result, log_id=log_id))


@app.route("/actions/thumbs-up", methods=["POST"])
def thumbs_up():
    log_id = request.args.get("log_id")

    # Send explicit feedback 👍 to Humanloop
    hl.feedback(group="feedback", label="👍", log_id=log_id)

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            log_id=log_id,
            feedback="👍",
            copied=request.args.get("copied", False),
        )
    )


@app.route("/actions/thumbs-down", methods=["POST"])
def thumbs_down():
    log_id = request.args.get("log_id")

    # Send explicit feedback 👎 to Humanloop
    hl.feedback(group="feedback", label="👎", log_id=log_id)
    print(f"Recorded 👎 feedback to log: {log_id}")

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            log_id=log_id,
            feedback="👎",
            copied=request.args.get("copied", False),
        )
    )


@app.route("/actions/copy", methods=["POST"])
def feedback():
    log_id = request.args.get("log_id")

    # Send implicit feedback to Humanloop
    hl.feedback(group="implicit", label="copy", log_id=log_id)

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            log_id=log_id,
            feedback=request.args.get("feedback"),
            copied=True,
        )
    )
