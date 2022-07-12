import time
from multiprocessing import Process


if __name__ == "__main__" :
    a = Process(target=scan_tag_capture)
    b = Process(target=reader_status)
    c = Process(target = check_aprrove_status)
    d = Process(target= insert_into_activity)
    e = Process(target = send_data_via_mqtt)

 # Lets start each process
    a.start()
    b.start()
    c.start()
    d.start()
    e.start()

    a.join()
    b.join()
    c.join()
    d.join()
    e.join()



#code for multi-processing
#Asset Management
