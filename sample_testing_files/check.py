import main
reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1")
data=reader1.reader_status()
reader1.send_data_via_mqtt(data)
