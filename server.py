import requests
import json
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify

port_No = 9200

#Initialize 
es = Elasticsearch([{'host': 'localhost', 'port': port_No}])
app = Flask(__name__)
index = "address-book"
doc_type = "contact"
es.indices.create(index=index, ignore=400)

#Test route to check service
@app.route('/')
def test_elastic():
    res = requests.get('http://localhost:9200/')
    return res.content

#Route to Get, Update and Delete contact by name
@app.route('/contact/<name>', methods=['DELETE', 'GET', 'PUT'])
def del_contact(name):
    user_id = []
    resp = []

    #Search for matches to get ID
    res = es.search(index=index, doc_type=doc_type, body={"query": {"match": {"name":name}}})

    if res["hits"]["total"] == 0:
        return "Error: No matches\n", 400

    #Collect all matching ID's
    for doc in res['hits']['hits']:
        user_id.append(doc['_id'])

    #Handle Delete
    if request.method == 'DELETE':
        #Delete each match
        for i in user_id:
            res = es.delete(index=index, doc_type=doc_type, id=i, refresh=True)
            resp.append (res)
        return jsonify(resp)

    #Handle GET
    elif request.method == 'GET':
        for doc in res['hits']['hits']:
            resp.append(doc)
        return jsonify(resp)

    #Handle PUT
    elif request.method == 'PUT':
        if request.get_json().get("number") is None:
            return "Error: number field missing from JSON", 400
        else:
            number = request.get_json().get("number")
        for i in user_id:
            res = es.update(index=index, refresh=True, doc_type=doc_type, id=i, body={"doc": {"name": name, "number": number }})
            resp.append(res)
        return jsonify(resp)


#Route to create a new contact
@app.route('/contact', methods=['POST'])
def post_contact():
    #Checking required fields
    if request.get_json().get("name") is None:
        return "Error: name field missing from JSON \n", 400
    else:
        name = request.get_json().get("name")

    if request.get_json().get("number") is None:
        return "Error: number field missing from JSON \n", 400
    else:
        number = request.get_json().get("number")
    
    #Input Validation and API request
    if int(number) > 999999999999999 or int(number) < 0:
        return "Error: (Number < 0 or Number > 15 digits) \n", 400
    else:
        if name.isalpha() is False:
            return "Error: Name can only be alphabetic \n", 400
        else:
            #Check for duplicate names
            res = es.search(index=index, doc_type=doc_type, body={"query": {"match": {"name":name}}})
            if res['hits']['total'] is not 0:
                print(res)
                return "Error: Name already exists in database \n", 400
            
            #Else create new contact
            res = jsonify(es.index(index=index, refresh=True, doc_type=doc_type, body={"name": name, "number": number}))
    
    return res

#Route to get contacts (Match all by default)
@app.route('/contact', methods=['GET'])
def get_contacts():
    #Input validation and bound checking
    if 'pagesize' in request.args:
        pagesize = int(request.args['pagesize'])
        if pagesize < 1:
            return "Error: PageSize is less than 1 \n", 400
    else:
        pagesize = 20

    if 'page' in request.args:
        page = int(request.args['page'])
        if page < 1:
            return "Error: Page number less than 1 \n", 400
    else:
        page = 1

    if 'query' in request.args:
        query_string = request.args['query']
        print(query_string)
        query = {"query": {"query_string":{ "default_field" : "name",
            "query" : query_string}}}
    else:
        query = {"query": {"match_all": {} }}
    

    #Search and Collect all matches into resp list
    res = es.search(index=index, doc_type=doc_type, body=query)
    resp = []
    count = int(res ['hits']['total'])
    print(count)
    for doc in res['hits']['hits']:
        print("%s" % (doc['_source']))
        resp.append(doc)


    #Paging and pagesize logic
    if page > 1:
        if count > pagesize*(page-1):
            if count < pagesize*page:
                return jsonify(resp[pagesize*(page-1):count])
            else:
                return jsonify(resp[pagesize*(page-1):pagesize*page])
        else:
            return "Error: Page does not exist, since there are not enough results \n", 400
    else:
        if count > pagesize:
            return jsonify(resp[0:pagesize])
        else:
            return jsonify(resp[0:count])

#404 handler
@app.errorhandler(404)
def page_not_found(e):
    res = "Error: Requested function does not exist. Try a different route or method.\n"
    return res, 400

#Main
if __name__ == '__main__':
    app.run()

