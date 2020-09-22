#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import paho.mqtt.client as mqtt
import importlib
from rospy import Subscriber
from rospy_message_converter import json_message_converter
import json

class MqttPublisher():
    def __import_type(self):
        tmp=self._ros_type_name.split("/")
        module_name=tmp[0]+".msg"
        libs=importlib.import_module(module_name)
        return getattr(libs,tmp[1])

    def __json_convert(self,value):
        return json.dumps({"type":self._ros_type_name,"value":value})

    def __callback(self,msg):
        self.__client.publish(self._topic_name,self.__json_convert(json_message_converter.convert_ros_message_to_json(msg)))

    def __init__(self,client,topic_name,ros_type):
        self._topic_name=topic_name
        self._ros_type_name=ros_type
        self.__ros_type=self.__import_type()
        self.__client=client
        self.__topic_subscriber=Subscriber(self._topic_name,self.__ros_type,self.__callback)

topic_connect=[]

def on_connect(client,userdata,flags, rc):
    global topic_names
    global type_names
    for i in range(0,len(topic_names)):
        topic_connect.append(MqttPublisher(client,topic_names[i],type_names[i]))


rospy.init_node("ros_topic2mqtt")

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
