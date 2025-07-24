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

@app.route("/<string:path0>/<string:path1>/<string:path2>/<string:filename>", methods=["GET", "POST", "PUT", "DELETE"])
def _app(path0, path1, path2, filename):
    user = session.get("user")
    print(f"path0: {path0}")
    print(f"path1: {path1}")
    print(f"path2: {path2}")
    print(f"filename: {filename}")
    print(f"request method: {request.method}")
    if user:
        #return jsonify({"message": "You are authenticated!", "user": user}), 200
        #if path1=='..':
        #    path1 = 'immutable' # this is such a kludge, we'll see if it works
        target_url = f'http://localhost:{internal_app_port}/{path0}/{path1}/{path2}/{filename}'

        return internal_request_handler(request, target_url)
    else:
        return jsonify({"message": "You are not logged in."}), 401

@app.route("/<string:path1>/<string:path2>", methods=["GET", "POST", "PUT", "DELETE"])
def _app2(path1, path2):
    user = session.get("user")
    if user:
        target_url = f'http://localhost:{internal_app_port}/{path1}/{path2}'

        return internal_request_handler(request, target_url)
    else:
        return jsonify({"message": "You are not logged in."}), 401

@app.route("/<string:data>", methods=["GET", "POST", "PUT", "DELETE"])
def _app3(data):
    user = session.get("user")
    print(f"data: {data}")
    print(f"request method: {request.method}")
    allowed_paths = ['plans', 'models', 'scheduling', 'sequencing', 'constraints', 'tags', 'external_sources', 'dictionaries', 'expansion', 'parcels', 'documentation', 'gateway', 'about']
    if user:
    #if user and (('__data.json' in data) or ('favicon.svg' in data) or (data in allowed_paths) ):
        target_url = f'http://localhost:{internal_app_port}/{data}'

        return internal_request_handler(request, target_url)
    else:
        return jsonify({"message": "You are not logged in."}), 401

@app.route("/login", methods=["GET", "POST", "PUT", "DELETE"])
def _app4():
    user = session.get("user")
    if user:
        target_url = f'http://localhost:{internal_app_port}/login'

        return internal_request_handler(request, target_url)
    else:
        return jsonify({"message": "You are not logged in."}), 401

@app.route("/_app/<string:filename>", methods=["GET", "POST", "PUT", "DELETE"])
def _app5(filename):
    user = session.get("user")
    print(f"filename: {filename}")
    print(f"request method: {request.method}")
    if user:
    #if user and (('version.json' in filename) ):
        target_url = f'http://localhost:{internal_app_port}/_app/{filename}'

        return internal_request_handler(request, target_url)
    else:
        return jsonify({"message": "You are not logged in."}), 401

@app.route("/<string:path0>/<string:path1>/<string:path2>", methods=["GET", "POST", "PUT", "DELETE"])
def _app6(path0, path1, path2):
    user = session.get("user")
    if user:
        #return jsonify({"message": "You are authenticated!", "user": user}), 200
        #if path1=='..':
        #    path1 = 'immutable' # this is such a kludge, we'll see if it works
        target_url = f'http://localhost:{internal_app_port}/{path0}/{path1}/{path2}'

        return internal_request_handler(request, target_url)
    else:
        return jsonify({"message": "You are not logged in."}), 401

@app.route("/<string:path0>/<string:path1>/<string:path2>/<string:path3>/<string:filename>", methods=["GET", "POST", "PUT", "DELETE"])
def _app7(path0, path1, path2, path3, filename):
    user = session.get("user")
    # print(f"path0: {path0}")
    # print(f"path1: {path1}")
    # print(f"path2: {path2}")
    # print(f"path3: {path3}")
    # print(f"filename: {filename}")
    # print(f"request method: {request.method}")
    if user:
        #return jsonify({"message": "You are authenticated!", "user": user}), 200
        #if path1=='..':
        #    path1 = 'immutable' # this is such a kludge, we'll see if it works
        target_url = f'http://localhost:{internal_app_port}/{path0}/{path1}/{path2}/{path3}/{filename}'

        return internal_request_handler(request, target_url)
    else:
        return jsonify({"message": "You are not logged in."}), 401

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
