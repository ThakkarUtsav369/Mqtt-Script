from asyncio.log import logger
from datetime import datetime, timedelta
import time
import paho.mqtt.client as mqtt
import os
import json

mqtt_id = "mqtt.raychem.hikar.cloud"
mqtt_user = "raychem"
mqtt_pass = "Secure@098"
# def check_time(topic,time_dict):
#     print("Checking time")
#     if time_dict is not None:
#         print(time_dict)
#         keys = list(time_dict.keys())
#         print(keys)
#         print(topic)
        # if str(topic) in keys:
        #     print("Checking condition")
        #     value=time_dict[topic]
        #     print(value)
        #     diff = value - datetime.now()
            # if diff >timedelta(seconds=40):
            #     print("Time")

# time_dict={}
# last_mail_sent_dict={}

# def send_alerts(topic,subscribe_data):
    
#     topics=["Hikar/machineId/A8:74:1D:0E:D2:82:ST:02","Hikar/machineId/A8:74:1D:0E:D2:3B:ST:03","Hikar/machineId/A8:74:1D:0E:D2:F4:ST:04","Hikar/machineId/A8:74:1D:0C:68:DD:ST:05"]
#     if topic in topics:
#         print("hello from message send ")
        
        # if time_dict is not None:
        #     if topic in time_dict.keys():
        #         print("hello from")
        #         val=time_dict[topic][0]
        #         if val:
        #             print(val)
        #             diff = datetime.now() - val
        #             print("diff: " , diff)
        #             if diff >timedelta(seconds=40):
        #                     print("Mail sent")
        #                     print("sms sent")
        #                     print(topic)
        #                     last_mail_sent_dict[topic]=datetime.now()
        #                     print("Mail sent")
#         time_dict[topic] = [datetime.now()]
#         print(time_dict)
#         # check_time(time_dict,topic)
        


        
        


#     return time_dict


class MyMQTTClient:
    def __init__(self, mac_id_to_sud):
        self.mac_id_to_sud = mac_id_to_sud
        self.subscribe_data = None
        self.time_dict={}
        self.last_mail_sent_dict=None

        self.client = mqtt.Client()
        logger.error("Step 1 :: Main Function for MQTT")
        self.client.username_pw_set(username=mqtt_user, password=mqtt_pass)
        self.client.on_connect = self.on_connect_tag_device
        self.client.on_message = self.on_message_tag_device
        self.client.on_subscribe = self.on_subscribe_tag_device
        self.client.on_unsubscribe = self.on_unsubscribe_tag_device

        self.client.on_reconnect = self.on_reconnect_tag_device

        self.client.on_disconnect = self.on_disconnect_tag_device

        self.client.connect(mqtt_id, 1883, 60)
        # time.sleep(10)
        self.client.loop_forever()
        # time.sleep(5)

        self.client.on_connect = (
            lambda client, userdata, flags, rc: self.on_connect_tag_device(
                client, userdata, flags, rc
            )
        )
    def payload_formate(self,data):
        x = data.replace(":", ",")
        x = x.replace("{", "")
        x = x.replace("}", "")
        x = x.replace('"', "")
        x = x.replace("'", "")
        x = x.split()
        subscribe_data = list()
        for i in x:
            subscribe_data = i.split(",")
        return subscribe_data
    def send_alerts(self,topic,subscribe_data):
    
        topics=["Hikar/machineId/A8:74:1D:0E:D2:82:ST:02","Hikar/machineId/A8:74:1D:0E:D2:3B:ST:03","Hikar/machineId/A8:74:1D:0E:D2:F4:ST:04","Hikar/machineId/A8:74:1D:0C:68:DD:ST:05"]
        print("heelo from send message")
        json_file_path = 'time_dict.json'
        json_file_path_new="time_dict_new.json"

   
        try:
            with open(json_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
           
        except FileNotFoundError:
            existing_data = {} 
        if topic in topics:
            print(existing_data)
            
            with open(json_file_path_new,'w') as json_file_new:
                if existing_data:
                    json.dump(existing_data, json_file_new)
            self.time_dict[topic] = datetime.now().strftime("%H:%M:%S")
            existing_data.update(self.time_dict)
            # json_file_path = 'time_dict.json'


        with open(json_file_path, 'w') as json_file:
            json.dump(existing_data, json_file)

        print(f'Dictionary saved to {json_file_path}')
            # print(self.time_dict)

            # print("hello from message send ")
    def send_mail(self):  
        print("hello from send message new")  
    def on_connect_tag_device(self, client, userdata, flags, rc):
        logger.error("Step 2 :: Connected to MQTT broker")
        client.subscribe(self.mac_id_to_sud)

    def on_subscribe_tag_device(self, client, userdata, mid, granted_qos):
        logger.error(f"Step 3 :: Subscribed: {mid} with QoS {granted_qos}")

    def on_message_tag_device(self, client, userdata, msg):
        logger.error("Step 4 :: On Message Event Of Mqtt broker for bridge")
        data = msg.payload.decode()
        # logger.error(data)
        # logger.error(msg.topic)
        topic = msg.topic
        subscribe_data =self.payload_formate(data)
        # logger.error(subscribe_data)
        self.subscribe_data = subscribe_data
        self.send_alerts(topic,subscribe_data)
        self.send_mail()

    def on_unsubscribe_tag_device(self, client, userdata, mid):
        # logger.error("step 5")
        logger.error("Step 5 :: Unsubscribed from topic")

    def on_reconnect_tag_device(self, client, userdata, flags, rc):
        print("step 6 :: Reconnected with result code " + str(rc))
        logger.error("step 5")

        client.subscribe(self.mac_id_to_sud)
        # self.subscribe("mytopic")

    def on_disconnect_tag_device(self, client, userdata, rc):
        data = " Step 7 is Disconnected and Gone into disconnected method"
        # send_notification(data)
        if rc != 0:
            print("Station :: 3 Step 6  On Disconnect Method Unexpected disconnection.")
        else:
            print("Station :: 3 Step 6  On Disconnect Method Disconnected gracefully.")

    def get_subscribe_data(self):
        return self.subscribe_data
    def get_time_dict(self):
        return self.time_dict
    



# print(time_dict)




run_file=MyMQTTClient("Hikar/machineId/#")
data=run_file.get_time_dict()

# def send_alert(data):
#     print("heartbeat")
#     topics=["Hikar/machineId/A8:74:1D:0E:D2:82:ST:02","Hikar/machineId/A8:74:1D:0E:D2:3B:ST:03","Hikar/machineId/A8:74:1D:0E:D2:F4:ST:04","Hikar/machineId/A8:74:1D:0C:68:DD:ST:05"]
#     print(data)


# while True:
#     send_alert(data)