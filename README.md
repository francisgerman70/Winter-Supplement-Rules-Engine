# Winter Supplement Rules Engine

## Description
This repository contains a rules engine for determining client eligibility for the winter supplement, calculating the eligibilty amout and integrating an MQTT based event driven architecture. 
The unit test simulates publishing input to a topic and receiving responses from the rules engine being tested.

## Features
---
>* Determines a client eligibility for the sinter supplement based on json input.
>* Calculate the supplement amount based on specific rules.
>* Intergrates with an MQTT broker to receive input and publish results.

## Contributors
---
 [Francis German](francisgerman70)


### Resources:
>* https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4
>* https://stackoverflow.com/questions/63349301/python-unittest-for-paho-mqtt-not-working-simple-syntax-issue
>* https://github.com/phyunsj/mqtt-rule-engine/blob/master/unittest/mqtt_rule_test.py
>* https://stackoverflow.com/questions/54568782/how-to-implement-multithreading-for-a-mqtt-client-that-can-send-and-receive-mess

### Programming Language: Python

### Prerequisites
* install python 3
* install paho-mqtt==1.6.1 (pip install paho-mqtt==1.6.1)

### Setup
* Clone the repository
* cd winter supplement rules engine

## How To Run
```
In the winter supplement rules engine folder run "python3 rulesEngine.py" in terminal to run the rules engine, while rulesEngine.py is running go into the tests folder and run "python3 rulesEngineUnitTest.py" in a new terminal to run the unit test that tests the rules engine.
```
### Below is the output after performing the above properly.
* received message:  {"id": "4", "numberOfChildren": 5, "familyComposition": "couple", "familyUnitInPayForDecember": true}

publishing output:{'id': '4', 'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 100.0, 'supplementAmount': 220.0}

* received message:  {"id": "1", "numberOfChildren": 1, "familyComposition": "single", "familyUnitInPayForDecember": false}

publishing output:{'id': '1', 'isEligible': False, 'baseAmount': 0.0, 'childrenAmount': 0.0, 'supplementAmount': 0.0}

* received message:  {"id": "2", "numberOfChildren": 0, "familyComposition": "single", "familyUnitInPayForDecember": true}

publishing output:{'id': '2', 'isEligible': True, 'baseAmount': 60.0, 'childrenAmount': 0.0, 'supplementAmount': 60.0}

* received message:  {"id": "3", "numberOfChildren": 6, "familyComposition": "single", "familyUnitInPayForDecember": true}
  
publishing output:{'id': '3', 'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 120.0, 'supplementAmount': 240.0}

* received message:  {"id": "5", "numberOfChildren": 8, "familyComposition": "couple", "familyUnitInPayForDecember": true}
  
publishing output:{'id': '5', 'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 160.0, 'supplementAmount': 280.0}

## Note
* After running unit test multiple times, some test cases might start to fail due to flakiness. A solution will be to restart your local machine and try again.
