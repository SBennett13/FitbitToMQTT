#!/usr/bin/env python

# -------------------------------------
#
# Scott Bennett, scottbenett027@gmail.com
#
# fitbit-to-mqtt.py : push Fitbit information from Fitbit
#       servers to an MQTT server
#
# -------------------------------------
import configparser
import argparse
import logging
import time
import datetime

import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd
import paho.mqtt.client as mqtt


class FitbitToMqtt():
    def __init__(self, cfgFile, debug=False, getOauth=False):
        self.cfgFile = cfgFile
        self.debug = debug
        valid = self.loadConfig()
        if getOauth:
            self.getOauth()
            return

        if valid:
            self.init()

    def loadConfig(self):
        success = True
        if self.debug:
            print('Loading %s' % self.cfgFile)
        config = configparser.ConfigParser()
        config.read(self.cfgFile)

        section = 'Fitbit'
        try:
            self.client_id = config[section].get('client_id')
            self.client_secret = config[section].get('client_secret')
            self.access_token = config[section].get('access_token')
            self.refresh_token = config[section].get('refresh_token')
            self.expires_at = float(config[section].get('expires_at'))
        except Exception:
            print('Error getting Fitbit config')
            success = False
        section = 'MQTT'
        try:
            self.output_topic = config[section].get('output_topic')
            self.host = config[section].get('host')
            self.port = int(config[section].get('port'))
        except Exception:
            print('Error getting MQTT config')
            success = False

        if self.debug:
            print('Fitbit Client ID: %s' % self.client_id)
            print('Fitbit Client Secret: %s' % self.client_secret)
            print('Fitbit Access Token: %s' % self.access_token)
            print('Fitbit Refresh Token: %s' % self.refresh_token)
            print('MQTT Host: %s' % self.host)
            print('MQTT Port: %s' % self.port)
            print('MQTT Output Topic: %s' % self.output_topic)

        return success

    def on_message(self, client, userdata, msg):
        print("Got a message: %s" % msg.payload)

    def initMQTT(self):
        try:
            self.mqtt = mqtt.Client()
            # self.mqtt.enable_logger(self.logger)
            self.mqtt.connect(self.host, self.port, 60)
            self.mqtt.on_message = self.on_message
            return True
        except Exception:
            print('Error starting MQTT client')
            return False

    def on_refresh(self, refreshDict):
        self.access_token = str(refreshDict['access_token'])
        self.refresh_token = str(refreshDict['refresh_token'])
        self.expires_at = float(refreshDict['expires_at'])

    def initFitbit(self):

        self.fitbitClient = fitbit.Fitbit(self.client_id, self.client_secret, access_token=self.access_token,
                                          refresh_token=self.refresh_token, refresh_cb=self.on_refresh, expires_at=self.expires_at, oauth2=True)
        return True

    def init(self):
        success1 = self.initMQTT()
        success2 = self.initFitbit()
        return success1 and success2

    def getYesterday(self):
        return str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))

    def getToday(self):
        return str(datetime.datetime.now().strftime("%Y%m%d"))

    def run(self):
        while 1:
            time.sleep(4)
            test = self.fitbitClient.get_devices()
            print(test)


# ---------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', dest='c', help='Config file to use for the client', type=str, default="./config/config.cfg")
    parser.add_argument(
        '--debug', help='Enable debug print', dest="d", default=False, action="store_true")
    args = parser.parse_args()

    test = FitbitToMqtt(args.c, args.d)
    test.run()
