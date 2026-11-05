
from flask import Flask, jsonify, request
from flask_cors import CORS
from GetWordData import getJson, gradeAnswer, getUsers, createUser

app = Flask(__name__)

CORS(app, origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
])


@app.route("/api/data", methods=["POST"])
def fetch_data():
    try:
        body = request.get_json()
        user = body.get("user")

        result = getJson(user)

        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/answer", methods=["POST"])
def fetch_word_info():
    try:
        body = request.get_json()
        word = body.get("word")
        user = body.get("user")

        result = gradeAnswer(word, user)

        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/users", methods=["GET"])
def fetch_users():
    try:
        result = getUsers()
        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/new-user", methods=["POST"])
def create_new_user():
    try:
        body = request.get_json()
        user = body.get("user")

        if not user:
            return jsonify({"error": "Missing user"}), 400

        createUser(user)

        return jsonify({
            "message": "User created successfully"
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
