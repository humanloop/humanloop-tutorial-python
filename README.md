# Humanloop API Quickstart - Python example app

This is an example app that shows you how to use the Humanloop API in a GPT-3 app. It uses the [Flask](https://flask.palletsprojects.com/en/2.2.x/) web framework and [Humanloop](https://humanloop.com) for data logging and model improvement. Check out the tutorial or follow the instructions below to get set up.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   $ cd humanloop-tutorial-python
   ```

4. Create a new virtual environment

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

7. Add your [OpenAI API key](https://beta.openai.com/account/api-keys) and [Humanloop API key](https://app.humanloop.com/llama/settings) to the newly created `.env` file

8. Run the app

   ```bash
   $ flask --debug run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)! For the full context behind this example app, check out the [tutorial](https://beta.openai.com/docs/quickstart).
