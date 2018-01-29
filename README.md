# AddressBook


AddressBook is a Flask based REST API with an ElasticSearch backend.


### Setup

AddressBook requires [Elastic Search 6+](https://www.elastic.co/support/matrix) and [Java 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) to run.


**If you are running ElasticSearch on a port other than default(9200). Set "testing = False" in server.py.** 

Clone the repository and start a terminal instance in the project folder.



**Run the following commands to activate the Virtual Enviornment and run the server.**
```sh
$ cd AddressBook
$ source test/bin/activate
$ python3 server.py
```

The server is now running...


Now, we can run the test script. Open another instance of a terminal in the project folder


```sh
$ cd AddressBook
$ source test/bin/activate
$ python3 test.py
```


The script will create two new contacts, test primary functionality and delete the contacts before exit.


*AddressBook uses a Python 3 Virtual-Env so you do not need to install any external modules.*

*In case of any problems, requirements.txt includes the modules and their versions used during development.*


### API Definition:
 - GET /contact?pageSize={}&page={}&query={}
 - POST /contact
 - GET /contact/{name}
 - PUT /contact/{name}
 - DELETE /contact/{name}


### Todos

 - Write MORE Tests
 - Add more routes to make full use of the power of ElasticSearch
