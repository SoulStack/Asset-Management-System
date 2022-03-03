from multiprocessing import Process
import main
import time

reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1","reader1_log")

def f1():
        while True :
                try :
                        data1 = reader1.reader_status()
                        time.sleep(10)                            #check the reader status and send>
                        reader1.reader_status_mqtt(data1)
                except :
                        print("error on connecting reader")       

def f2() :
        while True :
                try :
                        tag = reader1.scan_tag_capture()                 #scan the tags
                        tag1 = map(reader1.hex_to_string,tag)            #covert to string
                        approval = reader1.check_approve_status(tag1)    #check the approval status >
                        reader1.approval_status_mqtt(approval)   #send mqtt to broker
                except :
                        pass
def f3() :
        while True :
                try :
                        reader1.insert_into_activity()             #records will be inserted into ac>
                except :
                        pass


if __name__ == "__main__" :
        a = Process(target = f1) 
        b = Process(target = f2)
        c = Process(target = f3)


        a.start()               #To start the process
        b.start()
        c.start()


        a.join()              #In order to stop execution of current program until a process is comp>
        b.join()
        c.join()
