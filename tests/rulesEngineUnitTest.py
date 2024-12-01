import paho.mqtt.client as mqtt
import unittest
import json   
import time

def on_message(client, userdata, message):
    TestRulesEngine.receivedMessage = json.loads(message.payload.decode())

class TestRulesEngine(unittest.TestCase):  
    receivedMessage = None
    
    def setUp(self):
        self.client = mqtt.Client("Unit Test")
        self.client.on_message = on_message
        self.client.connect("test.mosquitto.org" , 1883)
        self.client.subscribe("BRE/calculateWinterSupplementOutput")
        self.client.loop_start()

    def tearDown(self):
        self.client.loop_stop()

    def testIneligible(self):
        data = {
            "id": "1",
            "numberOfChildren": 1,
            "familyComposition": "single",
            "familyUnitInPayForDecember": False
        }
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        time.sleep(10)
        expectedOutput = {
            "id": data["id"], 
            "isEligible": False, 
            "baseAmount": 0.0, 
            "childrenAmount": 0.0, 
            "supplementAmount": 0.0
        }
        self.assertEqual(TestRulesEngine.receivedMessage, expectedOutput)
        
    def testSingleNoChildren(self):
        data = {
            "id": "2",
            "numberOfChildren": 0,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        time.sleep(10)
        expectedOutput = {
            "id": data["id"], 
            "isEligible": True, 
            "baseAmount": 60, 
            "childrenAmount": 0, 
            "supplementAmount": 60
        }
        self.assertEqual(TestRulesEngine.receivedMessage, expectedOutput)
        
    def testSingleWithChildren(self):
        data = {
            "id": "3",
            "numberOfChildren": 6,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        time.sleep(10)
        expectedOutput = {
            "id": data["id"], 
            "isEligible": True, 
            "baseAmount": 120, 
            "childrenAmount": 120, 
            "supplementAmount": 240
        }
        self.assertEqual(TestRulesEngine.receivedMessage, expectedOutput)
   
    def testCoupleWithChildren(self):
        data = {
            "id": "4",
            "numberOfChildren": 5,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        time.sleep(10)
        expectedOutput = {
            "id": data["id"], 
            "isEligible": True, 
            "baseAmount": 120, 
            "childrenAmount": 100, 
            "supplementAmount": 220
        }
        self.assertEqual(TestRulesEngine.receivedMessage, expectedOutput)
    
    def testcoupleNoChildren(self):
        data = {
            "id": "5",
            "numberOfChildren": 8,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        time.sleep(10)
        expectedOutput = {
            "id": data["id"], 
            "isEligible": True, 
            "baseAmount": 120, 
            "childrenAmount": 160, 
            "supplementAmount": 280
        }
        self.assertEqual(TestRulesEngine.receivedMessage, expectedOutput)
   
   
if __name__ == '__main__':
    unittest.main()