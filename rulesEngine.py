import paho.mqtt.client as mqtt
import json

#   This function calculates the winter supplement amount based on input
def winterSupplementCalculator(data):
    baseAmount = 0.0
    additionalAmount = 0.0
    totalSupplementAmount = 0.0

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
    
    additionalAmount+= data["numberOfChildren"] * 20

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
    input = json.loads(message.payload.decode("utf-8"))
    output = winterSupplementCalculator(input)
    print(f"publishing output:{output}")

    
    client.publish("BRE/calculateWinterSupplementOutput", json.dumps(output))

client = mqtt.Client("Rules Engine")

client.on_message=on_message 
client.connect("test.mosquitto.org" , 1883) 
client.subscribe("BRE/calculateWinterSupplementInput")

client.loop_forever()