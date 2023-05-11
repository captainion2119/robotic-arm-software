import serial.tools.list_ports
import serial
import time
import threading


def getPorts():

    # Get a list of all available COM ports
    com_ports = serial.tools.list_ports.comports()

    # Extract the port names from the list
    port_names = [port.device for port in com_ports]
    return port_names

def testConnection(com):

    #on connection failure run timeout
    def timeout_handler():
        nonlocal connection_established
        if not connection_established:
            raise TimeoutError("Connection timed out")
            

    connection_established = False

    try:
        ArdObj = serial.Serial(com,115200,timeout=3)
        timer = threading.Timer(10,timeout_handler)
        timer.start()

        time.sleep(3)

        ArdObj.write('Ping\n'.encode())

        recieveMsg = ArdObj.readline().decode().strip()
        if recieveMsg == "Pong":
            connection_established = True
            ArdObj.close()
            return True
        else:
            ArdObj.close()
            return False
    
    except Exception as e:
        return str(e)

    finally:
        if 'ArdObj' in locals():
            ArdObj.close()
            timer.cancel()


