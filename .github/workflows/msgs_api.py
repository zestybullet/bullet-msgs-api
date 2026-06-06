"""
╔══════════════════════════════════════════════════════════════╗
║         BULLET MSGS API  ⚡  by Bullet                       ║
║         No IG login. Just serves msgs.                       ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("API_KEY", "bullet_key")

# ════════════════════════════════════════════════════════════
#  YOUR MSGS — edit these anytime, redeploy, all users get new msgs
# ════════════════════════════════════════════════════════════
SEP   = "______________________________________/"
BASE  = "{target} तू तू हिजड़ा"
EMOJIS = [
    "😀","😁","😂","🤣","😃","😄","😅","😆","😉","😊","😋","😎","😍","🥰","😘",
    "😜","😝","🤑","🤗","🤔","🤨","😐","😑","🙄","😏","😒","😓","😔","😕","🙃",
    "😲","😬","😰","😱","🥵","🥶","😳","🤪","😵","🥴","😠","😡","🤬","😷","🤒",
    "🤕","🤢","🤮","🤧","🥳","🥸","🥺","🤡","💩","👹","👺","💀","☠️","👻","👾",
    "🤖","😺","😸","😹","😻","😼","😽","🙀","😿","😾","🙈","🙉","🙊","💋","💘",
    "💝","💖","💗","💓","💞","💕","💟","❣️","💔","🧡","💛","💚","💙","💜","🖤",
    "🤍","🤎","💯","💢","💥","💫","💦","💨","👋","🤚","🖐️","✋","🖖","👌","🤌",
    "🤏","✌️","🤞","🤟","🤘","🤙","👈","👉","👆","🖕","👇","☝️","👍","👎","✊",
    "👊","🤛","🤜","👏","🙌","🫶","👐","🤲","🤝","🙏","✍️","💅","💪","🦾","🦵",
    "🦶","👂","🦻","👃","🧠","🦷","🦴","👀","👁️","👅","👄","🫦","🔥","⚡","🌈",
]

def build_msgs(target: str) -> list:
    return [(BASE.format(target=target) + e + SEP) * 12 for e in EMOJIS]


# ════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════

@app.route("/", methods=["GET"])
def home():
    return jsonify({"ok": True, "server": "Bullet Msgs API ⚡"})


@app.route("/msgs", methods=["GET"])
def get_msgs():
    """
    GET /msgs?target=shadow&limit=50
    Returns msg array with target name injected.
    No API key needed — msgs are public.
    """
    target = request.args.get("target", "target")
    limit  = int(request.args.get("limit", len(EMOJIS)))
    msgs   = build_msgs(target)[:limit]
    return jsonify({
        "ok":    True,
        "count": len(msgs),
        "msgs":  msgs
    })


@app.route("/msgs/index", methods=["GET"])
def get_msg_index():
    """
    GET /msgs/index?target=shadow&index=5
    Returns single msg at index.
    """
    target = request.args.get("target", "target")
    idx    = int(request.args.get("index", 0))
    msgs   = build_msgs(target)
    if idx >= len(msgs):
        return jsonify({"ok": False, "error": "index out of range"}), 400
    return jsonify({"ok": True, "index": idx, "msg": msgs[idx]})


@app.route("/count", methods=["GET"])
def get_count():
    return jsonify({"ok": True, "total": len(EMOJIS)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
