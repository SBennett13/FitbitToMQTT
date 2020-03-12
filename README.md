# Fitbit to MQTT

Scott Bennett - scottbennett027@gmail.com

### Introduction

Use Orcas Python module for Fitbit with Paho's MQTT module to poll for fitness
information and push it to an MQTT-connected host

#### Requirements

-   Orcas python-fitbit
-   paho-mqtt

### Configuration

Your configuration file must have the following categories:

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

-   get-oauth.py : get access token, refresh token, and expires at for
    the provided client id and secret. Run with -c argument as the path
    to your config.cfg
