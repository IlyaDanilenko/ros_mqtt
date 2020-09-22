#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import paho.mqtt.client as mqtt
import importlib
from rospy import Publisher
from rospy_message_converter import json_message_converter
import json

class MqttSubscriber():
    def __import_type(self):
        tmp=self._ros_type_name.split("/")
        module_name=tmp[0]+".msg"
        libs=importlib.import_module(module_name)
        return getattr(libs,tmp[1])

    def __on_message(self,client,userdata,msg):
        msg_from_json=json.loads(msg.payload)
        ros_type=msg_from_json["type"]
        if(ros_type==self._ros_type_name):
            ros_msg=json_message_converter.convert_json_to_ros_message(ros_type, msg_from_json["value"])
            self.__topic_publisher.publish(ros_msg)

    def __init__(self,client,topic_name,ros_type,queue_size):
        self.__client=client
        self._topic_name=topic_name
        self._ros_type_name=ros_type
        self.__ros_type=self.__import_type()
        self.__client.on_message=self.__on_message
        self.__client.subscribe(self._topic_name)
        self.__topic_publisher=Publisher(self._topic_name,self.__ros_type,queue_size=queue_size)

topic_connect=[]

def on_connect(client,userdata,flags, rc):
    global topic_names
    global type_names
    for i in range(0,len(topic_names)):
        topic_connect.append(MqttSubscriber(client,topic_names[i],type_names[i],10))


rospy.init_node("mqtt2ros_topic")

topic_param_name=rospy.search_param("topic_names")
topic_names=rospy.get_param(topic_param_name)
type_param_name=rospy.search_param("type_names")
type_names=rospy.get_param(type_param_name)
address_name=rospy.search_param("address")
address=rospy.get_param(address_name)
port_name=rospy.search_param("port")
port=rospy.get_param(port_name)

if(type(address)!=str):
    rospy.logerr("Server address not set")
    exit()

if(type(port)!=int):
    rospy.logerr("Port not set")
    exit()

if(len(type_names)!=len(topic_names)):
    rospy.logerr("The number of topic does not match the number of topic types")
    exit()

client= mqtt.Client()
client.on_connect=on_connect
client.connect(address,port,60)
client.loop_start()
while not rospy.is_shutdown():
    pass
client.loop_stop()
