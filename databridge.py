import serial.tools.list_ports
import serial


def getPorts():

    # Get a list of all available COM ports
    com_ports = serial.tools.list_ports.comports()

    # Extract the port names from the list
    port_names = [port.device for port in com_ports]

    return port_names

def serial_begin(com):
    ser = serial.Serial(com,9600)
    ser.write(b'hi')

    response = ser.readline().decode().strip()
    print(response)

    ser.close()

# need to begin testing of serial_begin()