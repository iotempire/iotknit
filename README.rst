IoTknit is part of the IoTempower framework.
It allows to easily knit together devices reachable via 
MQTT (and hopefully later also for classic webrequests and websockets)
of a network into an actual IoT system.
It is therefore an IoT integration system (similar but much more
barebones than `Node-RED <https//nodered.org>`_).
It was called initially IntegrIoT since 2017, but that name was also adopted
by `BM Communications <https://www.bmit.cz>`_ in 2022 and therefor
had to be changed to forego any confusion or even potential legal conflicts
for this open source project here.

It is a Python module and can be installed to your local
Python environment the following way:

Without cloning:

.. code-block:: bash

   pip install --upgrade git+https://github.com/iotempire/iotknit

After cloning this repo (from the repo directory):

.. code-block:: bash

   pip install --upgrade .

For building, run:

.. code-block:: bash

   pip -m build

A simple example how to connect a button node with a switch is here:

.. code-block:: python
   
   from iotknit import *

   led1Status = False

   init("localhost")  # use a MQTT broker on localhost

   prefix("led")  # all actors below are prefixed with /led

   led1 = publisher("led1")  # create a Thingi interface that publishes to led/led1

   def button1Callback(msg):
      global led1Status

      print("received: [button]", msg)

      if (msg == "down"):
         led1Status = not led1Status  # toggle status of led

         if (led1Status):
               led1.publish("set", "on")  # publish updated state
               print("sending: [led1]", "on")
         else:
               led1.publish("set", "off")
               print("sending: [led1]", "of")


   prefix("button")  # all sensors below are prefixed with /button

   button1 = subscriber("button1")  # create a Thingi interface that can have 
                                    # subscribes only to button/button1
   button1.subscribe_change(callback=button1Callback)

   run()  # you can also do a while loop here call process() instead


More examples can be found at:
https://github.com/iotempire/iotempower/tree/master/examples/iotknit
