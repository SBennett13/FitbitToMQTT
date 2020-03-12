# Fitbit to MQTT

Scott Bennett - scottbennett027@gmail.com

### Introduction

Use Orcas Python module for Fitbit with Paho's MQTT module to poll
for fitness information and push it to an MQTT-connected host

### Configuration

1. You will need to sign in at the [Fitbit Developers Page](https://dev.fitbit.com/).

Once you have an account, go to "Manage" -> "Register An App" and create a new app.
The only requirements are:

-   Oauth 2.0 Application Type: Personal
-   Callback URL: http://127.0.0.1:8080/

You'll need the resulting client ID and client secret for the next step.

2. Your configuration file must have the following categories:

```
[Fitbit]
    client_id=id
    client_secret=secret
[MQTT]
    output_topic=helloWorld
    host=broker location
    port=broker port
```

Optionally, you can add your access token (access_token), refresh token
(refresh_token), and expiration (expires_at), or you can let the
get-oauth.py script do it for you. See the section below...

### Useful scripts

-   setup.sh : Run this directly after cloning your repo. It will create
    a python virtual environment (venv), install the dependencies, and start the
    venv.

-   get-oauth.py : get access token, refresh token, and expires at for
    the provided client id and secret. Run with -c argument as the path
    to your config.cfg
