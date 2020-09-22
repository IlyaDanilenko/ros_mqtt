# ros_mqtt
Integration MQTT to Robot Operating System

This package allows you to broadcast ROS topics using the MQTT protocol.

You must install the python library [paho-mqtt](https://pypi.org/project/paho-mqtt/) before use

# Nodes

## ros_topic2mqtt
This node broadcasts ROS topics to the deployed MQTT server

### Parameters
* ```~topic_names``` (strings list: default:null) names of broadcast topics
* ```~type_names``` (string list: default:null) types of messages broadcast topic
* ```~address``` (string: default:null) ip address of a mqtt server 
* ```~port``` (integer: default:null) port number of a mqtt server

### Subscribe
The node subscribes to topics specified in the ```~topic_names``` parameter

## mqtt2ros_topic
This node broadcast MQTT topics to ROS topics

### Parameters
* ```~topic_names``` (strings list: default:null) names of broadcast topics
* ```~type_names``` (string list: default:null) types of messages broadcast topic
* ```~address``` (string: default:null) ip address of a mqtt server 
* ```~port``` (integer: default:null) port number of a mqtt server

### Publish
The node publishes to the topics specified in the ```~topics_name``` parameter
