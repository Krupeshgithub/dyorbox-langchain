#!/usr/bin/env python3
"""
Inialitation project to run this module.
"""
from __future__ import annotations
import os

import sqlite3

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from chat.conversation import ConversationalChain
from util import interval_cronjob

app = Flask(__name__)
CORS(app)

# Start Chat ConversationChain
interval_cronjob()
chat = ConversationalChain()
conversat = chat.conversation_retrieval_chain()


# Api
@app.route("/ask", methods=["POST"])
def ask_question():
    if request.headers.get("Authorization") != "df076c44-1018-4888-b3a7-6cd4d821e322":
        return jsonify({
            "answer": "Your user identity is invalid.",
        }), 400
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


@app.route("/clear-user-session", methods=["POST"])
def clear_user_session():
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()

    req = request.get_json(silent=True)
    session_id = req["user_id"]

    try:
        # Execute the DELETE statement
        cursor.execute(f"DELETE FROM message_store WHERE session_id = ?", (session_id,))
        # Commit the changes
        conn.commit()
        print(f"Entry with id {session_id} removed successfully.")
    except sqlite3.Error as e:
        print(f"Error removing entry with id {session_id}: {e}")
    finally:
        # Close the connection
        conn.close()

    return jsonify({
        "message": "success"
    }), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
