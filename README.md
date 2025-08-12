<!-- Header block for project -->
<hr>

<div align="center">

[INSERT YOUR LOGO IMAGE HERE (IF APPLICABLE)]
<!-- ☝️ Replace with your logo (if applicable) via ![](https://uri-to-your-logo-image) ☝️ -->
<!-- ☝️ If you see logo rendering errors, make sure you're not using indentation, or try an HTML IMG tag -->

<h1 align="center">[Flask Forward Proxy Using KeyCloak OIDC]</h1>

</div>

<pre align="center">[A simple Flask app that provides KeyCloak OIDC authN support for any web-app]</pre>

<!-- Header block for project -->

[This repository provides a simple Flask app that (a) performs user authentication with a KeyCloak server using the OIDC Authorization Code Flow and then (b) forward proxies authenticated user requests to a web-app running on the same server.  This Flask app must be running locally on the same server as this web-app, e.g., web-app is running as a set of containers running on a docker network.  The KeyCloak authN endpoint is assumed to be deployed already. ]

## Features

* Authentication is enforced by: (1) requiring an access token in the user request header; (2) validating the access token; (3) only forwarding requests with valid access tokens to your web-app.  If no token is provided in the user request or the provided token is not valid (e.g., is expired), the user will be redirected to the KeyCloak login page which then kicks off the OIDC authN flow.
* Uses the Flask OIDC library to (a) check user authentication status, (b) keep track of authenticated sessions and (c) perform OIDC Authorization Code Flow authentication before forwarding user requests to the web-app
* Uses the Flask KeyCloak library to broker the OIDC Authorization Code Flow between the Flask app and the KeyCloak server
* Since KeyCloak is used, this provides a very flexible OIDC authN solution since a user can authenticate directly with KeyCloak, or KeyCloak can be used as an identity broker with an external Identity Provider (e.g., github, google) and KeyCloak will handle the additional OIDC authN flow with the Identiy Provider.  Either way, this Flask app only needs to integrate ONCE with the KeyCloak server.
  

## Contents

* [Quick Start](#quick-start)
* [Changelog](#changelog)
* [FAQ](#frequently-asked-questions-faq)
* [Contributing Guide](#contributing)
* [License](#license)
* [Support](#support)

## Quick Start

This guide provides a quick way to get started with our project. Please see our [docs]([INSERT LINK TO DOCS SITE / WIKI HERE]) for a more comprehensive overview.  
* Deploy your web-app on your server and have it listen on localhost on your INTERNAL_APPLICATION_PORT of your choosing
* Setup your web server to listen your desired INBOUND_PORT (e.g., using NGINX server listening on INBOUND_PORT, an AWS ALB with a listener on INBOUND_PORT that forwards requests to the EC2 that your web-app is running on, etc)
* Build a python environment using the environment.yml file provided in this repo.  See the Requirements and Setup Instructions below for more details on how to do it
* Set the following environment variables for the Flask app to use internally for the OIDC autnN flow with your KeyCloak server:
1. INTERNAL_APPLICATION_PORT: after the user successfully authenticates with the KeyCloak server, the Flask app will forward proxy the user request on this port (i.e., on http://localhost:{INTERNAL_APPLICATION_PORT}); default is port 80
2. INBOUND_PORT: this is the inbound port that the user request comes in on, the Flask app listens on this port; default is port 8088
3. FLASK_SECRET_KEY: secret key for the Flask app itself, this can be set to any arbitrary value; default is "my_secret_key"
4. KEYCLOAK_SERVER_METADATA_URL: OIDC configuration URL that the Flask app will use to identify auth/token/userinfo/certs/etc endpoints for the KeyCloak server, it will be of the form https://{KeyCloak_server_domain_name}/realms/{KeyCloak_realm}/.well-known/openid-configuration; there is no default value
5. KEYCLOAK_CLIENT_ID: the KeyCloak Client ID where the Flask app will send the OIDC authN requests; there is no default value
6. KEYCLOAK_CLIENT_SECRET: the secret for the client specified in KEYCLOAK_CLIENT_ID; there is no default value
7. KEYCLOAK_LOGOUT_URL: the KeyCloak server's logout URL, it will be of the form https://{KeyCloak_server_domain_name}/realms/{KeyCloak_realm}/protocol/openid-connect/logout
* Run the following command:
```
python flaskProxyWithAuth.py
```
* If you set up everything correctly, this should work!

To test that auth is working, simply navigate to your web-app at https://{your_webapp_domain_name}:{INBOUND_PORT} and you should be redirected to your KeyCloak server login page.  Login and if successful, the Flask app should forward you to your web-app and voila, you've got OIDC authentication with KeyCloak up and running!


### Requirements

1. [INSERT LIST OF REQUIREMENTS HERE]
  
<!-- ☝️ Replace with a numbered list of your requirements, including hardware if applicable ☝️ -->

#### Build System Requirements
Certain properties and permission settings are necessary in GitHub for builds to run automatically. On local development systems builds may be tested in similar fashion with proper tooling installed.

##### Required repository settings
1. [Shared PyPi API Token](https://test.pypi.org/help#apitoken) installed in [GitHub Repository Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `PYPI_API_TOKEN`.
2. Permissions to [execute GitHub Actions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#managing-github-actions-permissions-for-your-repository) and [perform software tag and release](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-personal-account-settings/permission-levels-for-a-personal-account-repository#collaborator-access-for-a-repository-owned-by-a-personal-account).
<!-- ☝️ If necessary, update with a numbered list of your build requirements, including hardware if applicable ☝ -->

##### Required local tooling
1. Build tooling modules
```
pip3 install --upgrade build setuptools_scm twine wheel
```
2. Product required modules (`requirements.txt`)
``` 
pip3 --exists-action w install -r requirements.txt
```  
<!-- ☝️ If necessary, update with a numbered list of your build requirements, including hardware if applicable ☝ -->

### Setup Instructions

1. [INSERT STEP-BY-STEP SETUP INSTRUCTIONS HERE, WITH OPTIONAL SCREENSHOTS]
   
<!-- ☝️ Replace with a numbered list of how to set up your software prior to running ☝️ -->

### Run Instructions

1. [INSERT STEP-BY-STEP RUN INSTRUCTIONS HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a numbered list of your run instructions, including expected results ☝️ -->

### Usage Examples

* [INSERT LIST OF COMMON USAGE EXAMPLES HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a list of your usage examples, including screenshots if possible, and link to external documentation for details ☝️ -->

### Build Instructions
A [GitHub Action](.github/workflows/python-publish.yml) configuration specifies the series of commands to release and publish the product. Commands are staged and carried out automatically when a tagged release is published to the main branch.

#### Automated Build Kickoff
1. Edit the `[INSERT YOUR PACKAGE NAME]/version.py` file with the next release version using the web UI on GitHub `main` branch.
2. [Perform a release](releases/new) using the web UI on GitHub `main` branch
3. Build, packaging and release to PyPi will execute automatically using [GitHub Actions Workflows](actions)

<!-- ☝️ If necessary, update with a numbered list of your build instructions, including expected results / outputs with optional screenshots ☝️ -->

#### Manual Build
These instructions must be entered from the local directory checked out from source control.
1. Manually update `[INSERT YOUR PACKAGE NAME]/version.py` with the next release version, commit and push to the `main` branch:
``` 
git add [INSERT YOUR PACKAGE NAME]/version.py && git commit -m "Issue #<issue_number>: Updated version for release." && git push
```
2. Tag using the Git command line: 
``` 
git tag -a -m "Issue #<issue_number>: Release version <version>" <version>
```
**Note:** The `<version>` must match that in the `[INSERT YOUR PACKAGE NAME]/version.py` file.
3. Package the product:
- Package an `sdist` and a `tarball`: (traditional)
``` 
git checkout [INSERT YOUR PACKAGE NAME]/version.py && python3 -m build --wheel
```
- ... or package an `sdist` and a `zip` ...
``` 
python3 -m build --wheel && python3 setup.py sdist --format=zip
```
4. Publish product to PyPi for public distribution by using [Twine](https://twine.readthedocs.io/en/latest/):
``` 
twine check dist/* && twine upload --verbose
```
... or as a ZIP ...
``` 
twine check dist/* && twine upload --verbose dist/*.whl dist/*.zip
```

<!-- ☝️ If necessary, update with a numbered list of your build instructions, including expected results / outputs with optional screenshots ☝️ -->

### Test Instructions (if applicable)

1. [INSERT STEP-BY-STEP TEST INSTRUCTIONS HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a numbered list of your test instructions, including expected results / outputs with optional screenshots ☝️ -->

#### Local Build Testing
These instructions must be entered from the local directory checked out from source control.
A simplified build and release workflow is available for testing locally. Publishing directly to PyPi is not recommended as PyPi permits one upload per release version.  

1. Clean application:
``` 
rm -r build dist __pycache__ *.egg* .egg* ; git checkout [INSERT YOUR PACKAGE NAME]/version.py ; pip3 uninstall [INSERT YOUR PACKAGE NAME] -y
```
2. Build and install release locally:
``` 
python3 -m build --wheel && python3 setup.py sdist --format=zip
pip3 install [INSERT YOUR PACKAGE NAME] --no-index --find-links file://${PWD}/dist/
```  
... alternately, install an editable build using [Pip tooling](https://pypi.org/project/pip/) ...
``` 
pip install -e
```
3. [Testing publication to Test PyPi](https://packaging.python.org/en/latest/guides/using-testpypi/)  
Twine will prompt for your Test PyPi username and password.
```
twine check dist/*
twine upload --repository testpypi --verbose dist/*
```
<!-- ☝️ If necessary, update with numbered list of your test instructions, including expected results / outputs with optional screenshots ☝️ -->

## Changelog

See our [CHANGELOG.md](CHANGELOG.md) for a history of our changes.

See our [releases page]([INSERT LINK TO YOUR RELEASES PAGE]) for our key versioned releases.

<!-- ☝️ Replace with links to your changelog and releases page ☝️ -->

## Frequently Asked Questions (FAQ)

[INSERT LINK TO FAQ PAGE OR PROVIDE FAQ INLINE HERE]
<!-- example link to FAQ PAGE>
Questions about our project? Please see our: [FAQ]([INSERT LINK TO FAQ / DISCUSSION BOARD])
-->

<!-- example FAQ inline format>
1. Question 1
   - Answer to question 1
2. Question 2
   - Answer to question 2
-->

<!-- example FAQ inline with no questions yet>
No questions yet. Propose a question to be added here by reaching out to our contributors! See support section below.
-->

<!-- ☝️ Replace with a list of frequently asked questions from your project, or post a link to your FAQ on a discussion board ☝️ -->

## Contributing

Interested in contributing to our project? Please see our: [CONTRIBUTING.md](CONTRIBUTING.md)

<!-- example inline contributing guide>
1. Create an GitHub issue ticket describing what changes you need (e.g. issue-1)
2. [Fork](INSERT LINK TO YOUR REPO FORK PAGE HERE, e.g. https://github.com/my_org/my_repo/fork) this repo
3. Make your modifications in your own fork
4. Make a pull-request in this repo with the code in your fork and tag the repo owner / largest contributor as a reviewer

**Working on your first pull request?** See guide: [How to Contribute to an Open Source Project on GitHub](https://kcd.im/pull-request)
-->

For guidance on how to interact with our team, please see our code of conduct located at: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

<!-- ☝️ Replace with a text describing how people may contribute to your project, or link to your contribution guide directly ☝️ -->

For guidance on our governance approach, including decision-making process and our various roles, please see our governance model at: [GOVERNANCE.md](GOVERNANCE.md)

## License

See our: [LICENSE](LICENSE)
<!-- ☝️ Replace with the text of your copyright and license, or directly link to your license file ☝️ -->

## Support

[INSERT CONTACT INFORMATION OR PROFILE LINKS TO MAINTAINERS AMONG COMMITTER LIST]

<!-- example list of contacts>
Key points of contact are: [@github-user-1](link to github profile) [@github-user-2](link to github profile)
-->

<!-- ☝️ Replace with the key individuals who should be contacted for questions ☝️ -->

