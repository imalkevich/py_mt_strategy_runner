""" """
import configparser
import io
import os

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + "/../config.yaml")
