import sys, threading, time, io
from queue import Queue, Empty
import picamera

# Output stream
class OutputStream:
   def next_str(self, string):
      char = string[-1]
      if char == 'z':
         return string + 'a'
      else:
         if len(string) == 1:
            return chr(ord(string[0]) + 1)
         return string[:-1] + chr(ord(string[-1]) + 1)
   
   def new_file(self):
      self.file_name = self.next_str(self.file_name)
      return open(self.file_name + '.vblock', 'wb')

   def __init__(self):
      self.count = 0
      self.buf = b''
      self.output_stream = Queue()
      self.file_name = 'a'
      self.output_file = self.new_file()#open('file.h264', 'wb')

   def send_file(self):
      self.output_file.close()
      #call function to send file
      self.output_file = self.new_file()

   def write(self, buf):
      print('writing to queue')
      self.count += 1
      self.buf += buf
      #self.output_stream.put(buf)
      if self.count % 100 == 0:
         self.output_file.write(self.buf)
         self.send_file()
         self.buf = b''

   def flush(self):
      print('flush')
      #self.output_file.flush()
      if len(self.buf) != 0:
         self.output_file.write(self.buf)
      self.send_file()

stream = OutputStream()
#t2 = BlockThread()

# Start recording video with the picamera
def record_video():
   #global t2, t3
   with picamera.PiCamera() as camera:
      camera.resolution = (640, 480)
      #camera.framerate = 30
      try:
         camera.start_recording(stream, format='h264')#, quantization=23)
         print('recording video...')
         #_thread.start_new_thread(process_block_stream, ()) # Spawn a thread to process the block stream
         for _ in range(20):
            camera.wait_recording(1)
         camera.stop_recording()
      except KeyboardInterrupt:
         camera.stop_recording()
         print("Exiting")
         sys.exit(0)
   #t2.kill()
   print('killed threads')
   #print('t2 killed', t2.killed())
   return

t1 = threading.Thread(target=record_video)

t1.start()
#t2.start()

t1.join()
#t2.join()

