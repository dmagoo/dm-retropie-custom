import ConfigParser

def getConfig():
    conf = ConfigParser.ConfigParser()
    conf.read("conf/conf.ini")
    return conf
