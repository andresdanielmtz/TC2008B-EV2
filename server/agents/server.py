from flask import Flask, request, jsonify
import os
import dotenv


app = Flask(__name__)

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["POST"])
def main():
    pass


if __name__ == "__main__":
    app.run(debug=True)
