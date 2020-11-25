import requests

tests = [
    ('CREATE /devices content-type : application/json {"type" : "COMPUTER", "name" : "A1"}' ,200 , {"msg": "Successfully added A1"} ),
    ('CREATE /devices content-type : application/json {"type" : "COMPUTER", "name" : "A2"}' ,200 , {"msg": "Successfully added A2"} ),
    ('CREATE /devices content-type : application/json {"type" : "COMPUTER", "name" : "A3"}' ,200 , {"msg": "Successfully added A3"} ),
    ('CREATE /devices' ,400 , {"msg": "Invalid Command."} ),
    ('CREATE /devices content-type : application/json {"type" : "PHONE", "name" : "A3"}' ,400 , {"msg": "type 'PHONE' is not supported"} ),
    ('CREATE /devices content-type : application/json {"type" : "COMPUTER", "name" : "A1"}' ,400 , {"msg": "Device 'A1' already exists"} ),
    ('CREATE /devices content-type : application/json {"type" : "COMPUTER", "name" : "A4"}' ,200 , {"msg": "Successfully added A4"} ),
    ('CREATE /devices content-type : application/json {"type" : "COMPUTER", "name" : "A5"}' ,200 , {"msg": "Successfully added A5"} ),
    ('CREATE /devices content-type : application/json {"type" : "COMPUTER", "name" : "A6"}' ,200 , {"msg": "Successfully added A6"} ),
    ('CREATE /devices content-type : application/json {"type" : "REPEATER", "name" : "R1"}' ,200 , {"msg": "Successfully added R1"} ),
    ('MODIFY /devices/A1/strength content-type : application/json {"value": "Helloworld"}' ,400 , {"msg": "value should be an integer"} ),
    ('MODIFY /devices/A10/strength content-type : application/json {"value": "Helloworld"}' ,404 , {"msg": "Device Not Found"} ),
    ('MODIFY /devices/A1/strength content-type : application/json {"value": 2}' ,200 , {"msg": "Successfully defined strength"} ),
    ('CREATE /connections content-type : application/json {"source" : "A1", "targets" : ["A2", "A3"]}' ,200 , {"msg": "Successfully connected"}  ),
    ('CREATE /connections content-type : application/json {"source" : "A1", "targets" : ["A1"]}' ,400 , {"msg": "Cannot connect device to itself"} ),
    ('CREATE /connections content-type : application/json {"source" : "A1", "targets" : ["A2"]}' ,400 , {"msg": "Devices are already connected"} ),
    ('CREATE /connections content-type : application/json {"source" : "A5", "targets" : ["A4"]}' ,200 , {"msg": "Successfully connected"} ),
    ('CREATE /connections content-type : application/json {"source" : "R1", "targets" : ["A2"]}' ,200 , {"msg": "Successfully connected"} ),
    ('CREATE /connections content-type : application/json {"source" : "R1", "targets" : ["A5"]}' ,200 , {"msg": "Successfully connected"} ),
    ('CREATE /connections content-type : application/json {"source" : "R1"}' ,400 , {"msg": "Invalid command syntax"} ),
    ('CREATE /connections' ,400 , {"msg": "Invalid command syntax"} ),
    ('CREATE /connections content-type : application/json {"source" : "A8", "targets" : ["A1"]}'  ,400 , {"msg": "Node 'A8' not found"} ),
    ('CREATE /connections content-type : application/json {"source" : "A2", "targets" : ["A4"]}' ,200 , {"msg": "Successfully connected"} ),
    ('FETCH /info-routes?from=A1&to=A4' ,200 , {"msg": "Route is A1->A2->A4"} ),
    ('FETCH /info-routes?from=A1&to=A5' ,200 , {"msg": "Route is A1->A2->R1->A5"} ),
    ('FETCH /info-routes?from=A4&to=A3' ,200 , {"msg": "Route is A4->A2->A1->A3"} ),
    ('FETCH /info-routes?from=A1&to=A1' ,200 , {"msg": "Route is A1->A1"}),
    ('FETCH /info-routes?from=A1&to=A6' ,404 , {"msg": "Route not found"} ),
    ('FETCH /info-routes?from=A2&to=R1' ,400 , {"msg": "Route cannot be calculated with repeater"} ),
    ('FETCH /info-routes?from=A3' ,400 , {"msg": "Invalid Request"} ),
    ('FETCH /info-routes' ,400 , {"msg": "Invalid Request"} ),
    ('FETCH /info-routes?from=A1&to=A10' ,400 , {"msg": "Node 'A10' not found"} ),
    ('FETCH /devices' ,200 , { "devices": [ { 'type': 'COMPUTER', 'name': 'A1' }, { 'type': 'COMPUTER', 'name': 'A2' }, { 'type': 'COMPUTER', 'name': 'A3' }, { 'type': 'COMPUTER', 'name': 'A4' }, { 'type': 'COMPUTER', 'name': 'A5' }, { 'type': 'COMPUTER', 'name': 'A6' }, { 'type': 'REPEATER', 'name': 'R1' } ] })]

for data in tests:
    response = requests.post("http://localhost:8080/ajiranet/process",data=data[0])
    print("Testing.. {}".format(data[0]) ,response.json())
    assert response.status_code == data[1]
    assert response.json() == data[2]