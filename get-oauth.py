#!/usr/bin/env python3
# ----------------------------------
#
# Scott Bennett, scottbennett027@gmail.com
#
# get-oauth.py: Use client id and client secret to get
#           access token, refresh token, and expires at
#
# ---------------------------------

import configparser
import argparse

import gather_keys_oauth2 as oauth2

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config', help="Path to config file", type=str, dest='c')
    args = parser.parse_args()

    if not args.c:
        parser.print_help()
        exit(1)

    config = configparser.ConfigParser()
    config.read(args.c)
    section = 'Fitbit'
    creds = dict()
    try:
        creds['client_id'] = config[section].get("client_id")
        creds['client_secret'] = config[section].get("client_secret")
    except Exception:
        print("Couldn't find credentials. Make sure they are in the following format:")
        print("""
        [Fitbit]
            CLIENT_ID=<client id here>
            CLIENT_SECRET=<client secret here>

        """)
        exit(1)

    server = oauth2.OAuth2Server(creds['client_id'], creds['client_secret'])
    server.browser_authorize()

    creds['access_token'] = str(
        server.fitbit.client.session.token['access_token'])
    creds['refresh_token'] = str(
        server.fitbit.client.session.token['refresh_token'])
    creds['expires_at'] = str(server.fitbit.client.session.token['expires_at'])

    print("""
        Your Oauth Info:

        Access Token: {access}

        Refresh Token: {refresh}
        Expires at: {expire}


        Writing these to your config because I'm nice :)

    """.format(access=creds['access_token'], refresh=creds['refresh_token'], expire=creds['expires_at']))

    for k, v in creds.items():
        config.set(section, k, v)
    with open(args.c, 'w') as cfgFile:
        config.write(cfgFile)
