#   Import MQTT and JSON library for handling MQTT messages, parsing and constructing JSON messages
import paho.mqtt.client as mqtt
import json

#   This function calculates the winter supplement amount based on input
def winterSupplementCalculator(data):
    baseAmount = 0.0
    additionalAmount = 0.0
    totalSupplementAmount = 0.0

    #   Checks if the familyUnitInPayForDecember is valid
    if data["familyUnitInPayForDecember"] == False:
        return {
            "id": data["id"], 
            "isEligible": False, 
            "baseAmount": baseAmount, 
            "childrenAmount": additionalAmount, 
            "supplementAmount": totalSupplementAmount
        }

    #   Calculate based amount based on family composition and children
    if data["familyComposition"] == "single" and data["numberOfChildren"] == 0:
        baseAmount+= 60.0
    elif data["familyComposition"] == "single" and data["numberOfChildren"] > 0:
        baseAmount+= 120.0
    elif data["familyComposition"] == "couple":
        baseAmount+= 120.0
    
    #   Calculate the additional amount based on the number of children
    additionalAmount+= data["numberOfChildren"] * 20

    #   Calculate total supplement
    totalSupplementAmount = baseAmount + additionalAmount

    return {
            "id": data["id"], 
            "isEligible": True, 
            "baseAmount": baseAmount, 
            "childrenAmount": additionalAmount, 
            "supplementAmount": totalSupplementAmount
        }
    
def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

    #   Decode message into dictionary
    input = json.loads(message.payload.decode("utf-8"))

    #   Process the input data using the winter supplement calculator
    output = winterSupplementCalculator(input)
    print(f"publishing output:{output}")

    #
    client.publish("BRE/calculateWinterSupplementOutput", json.dumps(output))

#   Defines MQTT broker and port
mqttBroker ="test.mosquitto.org" 
port = 1883

#   Creates MQTT instance
client = mqtt.Client("Rules Engine")

#   Assigne the callback function
client.on_message=on_message 

#   Connect to MQT broker
client.connect(mqttBroker, port) 

#   Subscribe to the input topic to listen for messages
client.subscribe("BRE/calculateWinterSupplementInput")

#   Start the loop to keep listening for messages
client.loop_forever()