import os
import ConfigParser

def getConfig():
    conf = ConfigParser.ConfigParser()
    conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.ini'))
    #conf.read("conf/conf.ini")
    return conf
