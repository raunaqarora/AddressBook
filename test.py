import requests
import json
import time
import random

payload1 = {'name':'abc', 'number':'1234'}
payload2 = {'name':'xyz', 'number':'4321'}

def setup():
    res = requests.post('http://localhost:5000/contact', json = payload1)
    res = requests.post('http://localhost:5000/contact', json = payload2)

def test_get_contact():
    res = requests.get('http://localhost:5000/contact/abc')
    if res.status_code == 200:
        a, b = json.loads(res.text), payload1
        a = a[0]['_source']
        if a == b:
            print ("Test 1: GET /contact/abc Passed \n")
        else:
            print(json.dumps(a))
            print(json.dumps(b))


def test_delete():
    res = requests.delete('http://localhost:5000/contact/abc')
    if res.status_code == 200:
        a = json.loads(res.text)
        a = a[0]['_shards']['successful']
        if a <= 1:
            print ("Test 2: DELETE /contact/abc Passed \n")

def test_put():
    rand_number = random.randint(1,4320)
    payload3 = {'number': rand_number}
    res = requests.put('http://localhost:5000/contact/xyz', json = payload3)
    if res.status_code == 200:
        a = json.loads(res.text)
        a = a[0]['_shards']['successful']
        if a <= 1:
            print ("Test 3: PUT /contact/xyz Passed \n")


def tearDown():
    res = requests.delete('http://localhost:5000/contact/abc')
    res = requests.delete('http://localhost:5000/contact/xyz')

if __name__ == '__main__':
    setup()
    time.sleep(1)
    test_get_contact()
    time.sleep(1)
    test_put()
    time.sleep(1)
    test_delete()
    time.sleep(1)
    tearDown()
