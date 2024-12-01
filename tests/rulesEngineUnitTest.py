#   Import libraries for handling MQTT messages, unit tests, asynchronos test events and JSON messages
import paho.mqtt.client as mqtt
import unittest
import json   
from threading import Event

#   Callback function for handling MQTT messages 
def on_message(client, userdata, message):
    #   Decode message and store in attribute
    TestRulesEngine.receivedMessage = json.loads(message.payload.decode())

    #   Notify event to proceed
    TestRulesEngine.event.set()

#   Rules engine unit test class
class TestRulesEngine(unittest.TestCase):  
    receivedMessage = None
    event = Event()
    
    #   Setup MQTT client,  connect to broker and subcribe to the output topic
    def setUp(self):
        self.client = mqtt.Client("Unit Test")
        self.broker = "test.mosquitto.org" 
        self.port = 1883
        self.client.on_message = on_message
        self.client.connect(self.broker, self.port)
        self.client.subscribe("BRE/calculateWinterSupplementOutput")
        self.client.loop_start()

    #   Stop loop after tests
    def tearDown(self):
        self.client.loop_stop()

    def testIneligible(self):
        data = {
            "id": "1",
            "numberOfChildren": 1,
            "familyComposition": "single",
            "familyUnitInPayForDecember": False
        }
        TestRulesEngine.event.clear()
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        TestRulesEngine.event.wait(timeout=10)
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
        TestRulesEngine.event.clear()
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        TestRulesEngine.event.wait(timeout=10)
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
        TestRulesEngine.event.clear()
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        TestRulesEngine.event.wait(timeout=10)
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
        TestRulesEngine.event.clear()
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        TestRulesEngine.event.wait(timeout=10)
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
        TestRulesEngine.event.clear()
        TestRulesEngine.receivedMessage = None
        self.client.publish("BRE/calculateWinterSupplementInput", json.dumps(data))
        TestRulesEngine.event.wait(timeout=10)
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