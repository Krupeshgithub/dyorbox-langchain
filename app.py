#!/usr/bin/env python3
"""
Inialitation project to run this module.
"""
from __future__ import annotations
import os

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from chat.conversation import ConversationalChain

app = Flask(__name__)
CORS(app)

# Start Chat ConversationChain
chat = ConversationalChain()
conversat = chat.conversation_retrieval_chain()


# Api
@app.route("/dev/question", methods=["POST"])
def post_question():
    req = request.get_json(silent=True)
    chat_history_count = 3
    try:
        chat_history_count = int(os.environ.get("chat_history_count"))
    finally:
        resp = chat.chat_conversation(
            query=req["question"],
            user_id=req["user_id"],
            conversat=conversat,
            chat_history_count=chat_history_count
        )

        return jsonify({
            "answer": resp
        }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, )
