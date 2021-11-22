#!/usr/bin/env python

# Software License Agreement (BSD License)

#

# Copyright (c) 2008, Willow Garage, Inc.

# All rights reserved.

#

# Redistribution and use in source and binary forms, with or without

# modification, are permitted provided that the following conditions

# are met:

#

#  * Redistributions of source code must retain the above copyright

#    notice, this list of conditions and the following disclaimer.

#  * Redistributions in binary form must reproduce the above

#    copyright notice, this list of conditions and the following

#    disclaimer in the documentation and/or other materials provided

#    with the distribution.

#  * Neither the name of Willow Garage, Inc. nor the names of its

#    contributors may be used to endorse or promote products derived

#    from this software without specific prior written permission.

#

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS

# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT

# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS

# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE

# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,

# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,

# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;

# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER

# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT

# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN

# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE

# POSSIBILITY OF SUCH DAMAGE.

#

# Revision $Id$



## Simple talker demo that published std_msgs/Strings messages

## to the 'chatter' topic



import rospy

from std_msgs.msg import String



import boto3

from bottle import run, post, request, response, get, route

import simplejson as json

import thread

import time

import sys

import requests



def start_lambda(ip):

    lambda_client = boto3.client(

        'lambda',

        aws_access_key_id="KEY",

        aws_secret_access_key="KEY",

        region_name='us-east-2'

    )

    response = lambda_client.invoke(

      FunctionName='talker',

      Payload=json.dumps({"say":"szia lajos", "ip":str(ip)})

    )

    print(response)



def start_server(ip):

    run(host=str(ip), port=5000, debug=True)



@route('/', method = 'POST')

def process():

    global pub

    pub.publish('szia')



if __name__ == '__main__':

    try:

	pub = rospy.Publisher('chatter', String, queue_size=10)

        rospy.init_node('talker', anonymous=True)



        ip = str(requests.get('https://checkip.amazonaws.com').text.strip())

        thread.start_new_thread( start_server, (ip, ) )	

	time.sleep(5)

	print('lambda started on ip ', ip)

	start_lambda(ip)

    except rospy.ROSInterruptException:

        pass
