import os

def serve():

    config_dir = os.path.join(os.path.dirname(__file__), 'db.config')

    inpFile = open(config_dir, 'r')
    inp = inpFile.readline().split(',')
    db = inp[0]
    user = inp[1]
    pwd = inp[2]

    connectorStr = "mysql+pymysql://%s:%s@localhost/%s" % (user, pwd, db)
    
    return str(connectorStr)
