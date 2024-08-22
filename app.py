import os

from humanloop import Humanloop
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

HUMANLOOP_API_KEY = os.getenv("HUMANLOOP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

hl = Humanloop(api_key=HUMANLOOP_API_KEY)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        result=request.args.get("result"),
        log_id=request.args.get("log_id"),
        evaluation=request.args.get("evaluation"),
    )


@app.route("/get-question", methods=["POST"])
def get_question():
    # Make the request to GPT-4
    expert = request.form["Expert"]
    topic = request.form["Topic"]

    # hl.prompts.call automatically logs the data to your prompt.
    call_response = hl.prompts.call(
        path="learn-anything",
        inputs={"expert": expert, "topic": topic},
        # If you havent previously created a prompt, you can uncomment the prompt template below
        # prompt={
        #     "template": [
        #         {
        #             "role": "system",
        #             "content": "You are {{expert}}. Write a joke about {{topic}}.",
        #         }
        #     ],
        #     "model": "gpt-4",
        # },
        provider_api_keys={"openai": OPENAI_API_KEY},
    )

    # The log_id is the ID of the log on Humanloop that was created by the call
    log_id = call_response.id
    log_response = call_response.logs[0]

    return redirect(url_for("index", result=log_response.output, log_id=log_id))


@app.route("/actions/thumbs-up", methods=["POST"])
def thumbs_up():
    log_id = request.args.get("log_id")

    # We fetch the log from Humanloop to find which prompt it's associated with
    log = hl.logs.get(id=log_id)
    prompt_id = log.prompt.id

    # We fetch the prompt to find which evaluator it's associated with
    prompt = hl.prompts.get(id=prompt_id)

    # Note this will be empty if you haven't assigned a monitoring evaluator to your prompt
    evaluator_id = prompt.evaluators[0].version_reference.file.id

    # Send rating evaluation to Humanloop using the evaluator_id and log_id
    hl.evaluators.log(parent_id=log_id, id=evaluator_id, judgment="2")
    print(f"Recorded 👍 evaluation to log: {log_id}")

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            log_id=log_id,
            evaluation="👍",
            copied=request.args.get("copied", False),
        )
    )


@app.route("/actions/thumbs-down", methods=["POST"])
def thumbs_down():
    log_id = request.args.get("log_id")

    # We fetch the log from Humanloop to find which prompt it's associated with
    log = hl.logs.get(id=log_id)
    prompt_id = log.prompt.id

    # We fetch the prompt to find which evaluator it's associated with
    prompt = hl.prompts.get(id=prompt_id)

    # Note this will be empty if you haven't assigned a monitoring evaluator to your prompt
    evaluator_id = prompt.evaluators[0].version_reference.file.id

    # Send rating evaluation to Humanloop using the evaluator_id and log_id
    hl.evaluators.log(parent_id=log_id, id=evaluator_id, judgment="1")
    print(f"Recorded 👎 evaluation to log: {log_id}")

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            log_id=log_id,
            evaluation="👎",
            copied=request.args.get("copied", False),
        )
    )
