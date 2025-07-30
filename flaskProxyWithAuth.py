import os
from flask import request, jsonify, Response, Flask, redirect, url_for, session, render_template_string, render_template
from authlib.integrations.flask_client import OAuth
#from dotenv import load_dotenv
import requests
from http.client import HTTPConnection
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

#load_dotenv()

def internal_request_handler(request, target_url="http://localhost:80"):
    """
    Internal request handler to forward requests to the docker containers.
    """
    # Construct the new request to the target service
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True,
        params=request.args
    )

    # Create a Flask response object from the target service's response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    # Fix for JS files
    if request.path.endswith('.js'):
        response.headers["Content-Type"] = "application/javascript"

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    print(f"Response from target URL: {target_url}")
    print(f"Response status code: {resp.status_code}")
    print(f"Response headers: {headers}")

    return response


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

internal_app_port = os.getenv("INTERNAL_APPLICATION_PORT", 80)

oauth = OAuth(app)
oauth.register(
    name="keycloak",
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url=os.getenv("KEYCLOAK_SERVER_METADATA_URL"),
    client_kwargs={"scope": "openid profile email"},
)

@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def index():
    user = session.get("user")
    if user:
        #return jsonify({"message": "You are authenticated!", "user": user}), 200
        target_url = f"http://localhost:{internal_app_port}/"
        return internal_request_handler(request, target_url)
    else:
        redirect_uri = url_for("oauth2", _external=True)
        return oauth.keycloak.authorize_redirect(redirect_uri)
        # return render_template_string('''
        #     <h1>Hello, you are not logged in.</h1>
        #     <form action="{{ url_for('login_flask') }}" method="post">
        #         <button type="submit">Login</button>
        #     </form>
        # ''')

# Custom route to handle arbitrary path sequences
@app.route("/<path:some_path>", methods=["GET", "POST", "PUT", "DELETE"])
def flask_internal_proxy(some_path):
    user = session.get("user")
    if user:
        target_url = f"http://localhost:{internal_app_port}/{some_path}"
        return internal_request_handler(request, target_url)
    else:
        redirect_uri = url_for("oauth2", _external=True)
        return oauth.keycloak.authorize_redirect(redirect_uri)
        # return render_template_string('''
        #     <h1>Hello, you are not logged in.</h1>
        #     <form action="{{ url_for('login_flask') }}" method="post">
        #         <button type="submit">Login</button>
        #     </form>
        # ''')

# Login page
@app.route("/login_flask", methods=["POST"])
def login_flask():
    redirect_uri = url_for("oauth2", _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)

# Auth callback
@app.route("/oauth2")
def oauth2():
    token = oauth.keycloak.authorize_access_token()
    #print(token)
    session["user"] = oauth.keycloak.parse_id_token(token, None)
    return redirect("/")

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    logout_url = f"{os.getenv('KEYCLOAK_LOGOUT_URL')}?redirect_uri={url_for('index', _external=True)}"
    return redirect(logout_url)

if __name__ == "__main__":
    HTTPConnection.debuglevel = 3

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    app.run(host="0.0.0.0", port=8088, debug=True)
