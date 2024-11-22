import secrets, flask_socketio, flask

def run(port, host="0.0.0.0", allow_cors=False):
    app=flask.Flask(__name__)
    app.config['SECRET_KEY']=secrets.token_urlsafe(16)

    @app.route("/v")
    @app.route("/viewer")
    @app.route("/viewer.html")
    def viewer(): return flask.send_file("./web/v.html")

    @app.route("/")
    @app.route("/<path:path>")
    def index(path="index.html"): return flask.send_from_directory(f"./web/",path)
    socketio=flask_socketio.SocketIO(app, cors_allowed_origins=("*" if allow_cors else ""))

    print("Starting web server!")
    socketio.start_background_task(socketio.run, app=app, port=port, host=host, debug=False)
    return socketio