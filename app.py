import os

import humanloop as hl
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

hl.init(
    api_key=os.getenv("HUMANLOOP_API_KEY"),
    provider_api_keys={"openai": os.getenv("OPENAI_API_KEY")},
)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        result=request.args.get("result"),
        data_id=request.args.get("data_id"),
        feedback=request.args.get("feedback"),
        copied=request.args.get("copied", False),
    )


@app.route("/get-question", methods=["POST"])
def get_question():
    # Make the request to GPT-3
    expert = request.form["Expert"]
    topic = request.form["Topic"]

    # hl.generate automatically logs the data to your project.
    generation = hl.generate(
        project="learn-anything", 
        inputs={"expert": expert, "topic": topic},
    )
    data_id = generation.data[0].id
    result = generation.data[0].output

    print("data_id from generation: ", data_id)
    return redirect(url_for("index", result=result, data_id=data_id))


@app.route("/actions/thumbs-up", methods=["POST"])
def thumbs_up():
    data_id = request.args.get("data_id")

    # Send rating feedback to Humanloop
    hl.feedback(type="rating", value="good", data_id=data_id)
    print(f"Recorded 👍 feedback to datapoint: {data_id}")

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            data_id=data_id,
            feedback="👍",
            copied=request.args.get("copied", False),
        )
    )


@app.route("/actions/thumbs-down", methods=["POST"])
def thumbs_down():
    data_id = request.args.get("data_id")

    # Send rating feedback to Humanloop
    hl.feedback(type="rating", value="bad", data_id=data_id)
    print(f"Recorded 👎 feedback to datapoint: {data_id}")

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            data_id=data_id,
            feedback="👎",
            copied=request.args.get("copied", False),
        )
    )


@app.route("/actions/copy", methods=["POST"])
def feedback():
    data_id = request.args.get("data_id")

    # Send implicit feedback to Humanloop
    hl.feedback(type="action", value="copy", data_id=data_id)
    print(f"Recorded implicit feedback that user copied to datapoint: {data_id}")

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            data_id=data_id,
            feedback=request.args.get("feedback"),
            copied=True,
        )
    )
