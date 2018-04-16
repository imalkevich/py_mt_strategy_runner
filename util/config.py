""" """
import configparser
import io
import os

config = configparser.ConfigParser()
if os.path.isfile(os.path.dirname(__file__) + "/../config.yaml"):
    config.read(os.path.dirname(__file__) + "/../config.yaml")
