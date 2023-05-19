import serial.tools.list_ports
import serial
import time
import threading
import json



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


def send_coordinates(json_file,serial_port):
    with open(json_file) as file:
        data = json.load(file)

    progress_variable = 0

    steps = data[0]['task data']
    total_steps = len(steps)

    ser = serial.Serial(serial_port, baudrate=115200, timeout=3)  # Adjust baudrate if necessary
    
    time.sleep(3)

    for step_index, step in enumerate(steps):
        if 'end' in step:
            time.sleep(3)
            endmsg = "end"
            ser.write(endmsg.encode())
            break
        
        arm_number = step['arm']
        
        if 'wait' in step:
            wait_time = step['wait']
            # Wait for the specified time
            time.sleep(wait_time)
        else:
            coordinates = step
            if 'end' in coordinates:
                break  # End the loop if "end" instruction is encountered


            message = f"{arm_number}{coordinates['x']:03d}{coordinates['y']:03d}{coordinates['z']:03d}\n"
            # print(message) #NOTE: USE TO DEBUG


            ser.write(message.encode())
              # Send the coordinates over serial
            while True:
                response = ser.readline().decode().strip() # Read response from serial
                # print(response) #NOTE: USE TO DEBUG
                if response == "success":
                    break  # Proceed to the next instruction
                elif response == "End":
                    return
                

        progress_variable = int((step_index / (total_steps - 1)) * 100)
    progress_variable = 100


    ser.close()
