import os
from flask import Flask, render_template, request

from config   import WILAYAS
from database import init_db, add_subscriber, get_stats
from checker  import start_checker
from logger   import log

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))


@app.route("/", methods=["GET"])
def index():
    total, watched = get_stats()
    return render_template("index.html",
        wilayas=WILAYAS,
        total_subscribers=total,
        watched_wilayas=watched,
        message=None,
        message_type=None,
        email=None,
        selected_wilaya=None,
    )


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email       = request.form.get("email", "").strip()
    wilaya_code = request.form.get("wilaya_code", "").strip()
    wilaya_name = next(
        (w["wilayaNameFr"] for w in WILAYAS if w["wilayaCode"] == wilaya_code),
        None
    )

    total, watched = get_stats()

    if not email or not wilaya_code or not wilaya_name:
        log.warning(f"Invalid form submission: email={email}, wilaya_code={wilaya_code}")
        return render_template("index.html",
            wilayas=WILAYAS,
            total_subscribers=total,
            watched_wilayas=watched,
            message="Veuillez remplir tous les champs.",
            message_type="error",
            email=email,
            selected_wilaya=wilaya_code,
        )

    result = add_subscriber(email, wilaya_code, wilaya_name)

    if result == "added":
        msg      = f"Inscrit ! Vous serez notifié dès que {wilaya_name} sera disponible."
        msg_type = "success"
    elif result == "exists":
        msg      = f"Cet email est déjà inscrit pour {wilaya_name}."
        msg_type = "info"
    else:
        msg      = "Une erreur est survenue. Veuillez réessayer."
        msg_type = "error"

    total, watched = get_stats()
    return render_template("index.html",
        wilayas=WILAYAS,
        total_subscribers=total,
        watched_wilayas=watched,
        message=msg,
        message_type=msg_type,
        email=email if result != "added" else None,
        selected_wilaya=wilaya_code if result != "added" else None,
    )


if __name__ == "__main__":
    init_db()
    start_checker()
    log.info("Server running on http://0.0.0.0:3344")
    from waitress import serve
    serve(app, host="0.0.0.0", port=3344)