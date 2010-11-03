import logging
from twisted.application import internet, service
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from couchdb_connect import CouchDBConnect
from charun import Charun

## configuration parameters
## Twisted configuration
port = 9999
host = 'localhost'
loglevel = logging.INFO
#loglevel = logging.DEBUG

# this is the initial forwarding function used in the UDP Server. It is applied to incoming dicts
initial = lambda x: x

## CouchDB configuration
couchdb_url = "http://localhost:5984"
db_name = "charun"
# Test DB
test_db_name = "test_charun"

# create the application service
application = service.Application("charun couchdb bridge")
#define the UDP server on the specified port and hand the handler-class in
udp_service = internet.UDPServer(port, Charun(CouchDBConnect(couchdb_url, db_name),initial))
# this hooks the udp-service to the application
udp_service.setServiceParent(application)
# when started with twistd it will start the child services.

#LOGGING
logfile = DailyLogFile("charun.log", "tmp")
logname = "charun" 
logging.basicConfig(stream=logfile, format="[%(asctime)s]:charun: %(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(logname)
logger.setLevel(loglevel) 
application.setComponent(ILogObserver, log.PythonLoggingObserver(logname).emit)

# when started with twistd it will start the child services.
