#!/usr/bin/env python3 
import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib


Gst.init(None)

class Pipeline(object):
   def __init__(self):
       self.pipeline=Gst.parse_launch('rtspsrc location=rtsp://admin:artpark123@192.168.0.222/live/ch00_0 latency=0 ! rtph264depay ! h264parse ! decodebin ! autovideosink')
loop=GLib.MainLoop()
p=Pipeline()

try:
   p.pipeline.set_state(Gst.State.PLAYING)
   loop.run()
except KeyboardInterrupt:
   p.pipeline.set_state(Gst.State.NULL)
   loop.quit


'''from threading import Thread

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

pipeline = Gst.parse_launch("uridecodebin uri=rtsp://admin:artpark123@192.168.0.221/4 ! v4l2src ! decodebin ! videoconvert ! autovideosink")

pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()'''
