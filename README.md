==========================================================================================================

**CHARUN - A python bridge to CouchDB**  
<http://github.com/kr1/charun>

ABOUT
-----

***CHARUN*** is a server that listens on a UDP socket for incoming json-formatted data which is transformed in python objects, manipulated and sent to a couchdb instance. Think of it as a doorman.  
Intended use cases are: logging app data which has to be filtered, aggregated or otherwise tagged before being stored.

It is written in python and uses uses the [twisted](http://twistedmatrix.com/trac/wiki/Documentation) framework.
The basic modules are:

1.  **charun** 

holds the code that handles incoming data.

2.  **CouchDBConnect**

couchdb related code for connection ad storage

3.  **charun_tac.py**

application configuration (twisted.application) that holds all connection informations, database names.


INSTALL INSTRUCTIONS
-------------------

1.  **dependencies**

you need to have python and the [twisted](http://twistedmatrix.com/trac/wiki/Documentation) framework installed.
furthermore, you need a [couchdb](http://couchdb.apache.org/) instance to write to.

2.  **Run**

run charun as a daemon with:  
<code>twistd -y charun_tac.py</code>

it will log to the tmp directory and will write its pid to a file called twistd.pid to the current directory.  
stop the application with:  
<code>kill `cat twistd.pid`</code>

you can run the application in foreground with:  
<code>twistd -noy charun_tac.py</code>

