import os

import humanloop as hl
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

hl.init(
    api_key=os.getenv("HUMANLOOP_API_KEY"),
    provider_api_keys={"OpenAI": os.getenv("OPENAI_API_KEY")},
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

    generation = hl.generate(
        project="LearnAnythingFromAnyone", inputs={"expert": expert, "topic": topic}
    )
    data_id = generation.data[0].id
    print("Data_id from generation: ", data_id)
    result = generation.data[0].output

    return redirect(url_for("index", result=result, data_id=data_id))


@app.route("/actions/thumbs-up", methods=["POST"])
def thumbs_up():
    data_id = request.args.get("data_id")
    print(data_id)

    # Send explicit feedback 👍 to Humanloop
    hl.feedback(group="feedback", label="👍", data_id=data_id)

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

    # Send explicit feedback 👎 to Humanloop
    hl.feedback(group="feedback", label="👎", data_id=data_id)
    print(f"Recorded 👎 feedback to data point: {data_id}")

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
    hl.feedback(group="implicit", label="copy", data_id=data_id)

    return redirect(
        url_for(
            "index",
            result=request.args.get("result"),
            data_id=data_id,
            feedback=request.args.get("feedback"),
            copied=True,
        )
    )
