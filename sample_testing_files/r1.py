import main
from multiprocessing import Process

reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1","reader1_log")
def f1() :

    while True :
        try :
            redr_sts = reader1.reader_status()
            print(redr_sts)
            reader1.reader_status_mqtt(redr_sts)
            print("this is working")
        except :
            print("error in connecting")

        finally:
            if redr_sts == "Connected" :
                tag = reader1.scan_tag_capture()  # scan the tags
                tag1 = map(reader1.hex_to_string, tag) #convert to string
                print(tag1)
                approve = reader1.check_approve_status(tag1)       #check the approval status for the tag and return a string
                reader1.approval_status_mqtt(approve)
            else :
                reader1.reader_status_mqtt("Reader is disconnected")



if __name__ == "__main__" :
    a = Process(target = f1)
    
    a.start()
    a.join()
