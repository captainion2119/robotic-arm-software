import tkinter as tk
from tkinter import ttk
import sv_ttk
import serial.tools.list_ports
import serial
import time
import threading
import json
# root = tk.Tk()
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
def send_coordinates(json_file,serial_port,master):
    progress_view = tk.Toplevel(master)
    progress_view.title("Progress")
    progress_view.resizable(False,False)
    progress_view.attributes("-topmost",1)
    progress_frame = tk.Frame(progress_view)
    progress_frame.grid()
    with open(json_file) as file:
        data = json.load(file)
    steps = data[0]['task data']
    total_steps = len(steps)
    ser = serial.Serial(serial_port, baudrate=115200, timeout=3)  # Adjust baudrate if necessary
    progress_variable = tk.DoubleVar()
    progress_bar = tk.Canvas(progress_frame, width=200, height=20)
    progress_bar.create_rectangle(0, 0, 200, 20, fill="grey")
    progress_bar.create_rectangle(0, 0, 0, 20, fill="green", tags="progress")
    progress_bar.grid(row=2, column=1)
    progressing = tk.Label(progress_frame,text="Task is running, please wait...")
    progressing.grid(row=3,column=1)
    sv_ttk.set_theme("dark")
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
            message = f"\n{arm_number}{coordinates['s1']:03d}{coordinates['s2']:03d}{coordinates['s3']:03d}{coordinates['s4']:03d}{coordinates['s5']:03d}\n"
            # print(message) #NOTE: USE TO DEBUG
            ser.write(message.encode())
              # Send the coordinates over serial
            print(message)
            while True:
                response = ser.readline().decode().strip() # Read response from serial
                print(response) #NOTE: USE TO DEBUG
                if response == "success":
                    time.sleep(3)
                    break  # Proceed to the next instruction
                elif response == "End":
                    return
        progress_variable.set((step_index / (total_steps - 1)) * 100)
        progress = progress_variable.get()
        progress_bar.coords("progress", (0, 0, progress * 2, 20))
        progress_bar.delete("text")
        progress_text = f"{int(progress)}%"
        progress_bar.create_text(100, 10, text=progress_text, tags="text")
        progress_view.update()
    progress_variable.set(100)
    progress = progress_variable.get()
    progress_bar.coords("progress", (0, 0, progress * 2, 20))
    progress_bar.delete("text")
    progress_text = f"{int(progress)}%"
    progress_bar.create_text(100, 10, text=progress_text, tags="text")
    progress_view.destroy()
    ser.close()
    progress_view.mainloop()
# send_coordinates("tasks/Task1.json","COM6",root)
def retrv_cur_pos(arm_no,com_port):
    ser = serial.Serial(com_port, baudrate=115200, timeout=3) # Adjust baudrate if necessary
    time.sleep(3)
    message = f"{arm_no}curpos\n"
    ser.write(message.encode())
    time.sleep(3)
    response = ser.readline().decode().strip() # Read response from serial
    ser.close()
    # response = f"data sent to {com_port} and recieved successfully"
    return response

def move_by_one(arm_ang,amt,com_port):
    ser = serial.Serial(com_port, baudrate=115200, timeout=3) # Adjust baudrate if necessary
    time.sleep(3)
    ang = int(amt)
    message = f"{arm_ang}{ang:03d}\n"
    ser.write(message.encode())
    # response = ser.readline().decode().strip() # Read response from serial
    ser.close()

# import tkinter as tk
# from tkinter import ttk
# import sv_ttk
# import serial.tools.list_ports
# import serial
# import time
# import threading
# import json

# # root = tk.Tk()

# def getPorts():

#     # Get a list of all available COM ports
#     com_ports = serial.tools.list_ports.comports()

#     # Extract the port names from the list
#     port_names = [port.device for port in com_ports]
#     return port_names

# def testConnection(com):

#     #on connection failure run timeout
#     def timeout_handler():
#         nonlocal connection_established
#         if not connection_established:
#             raise TimeoutError("Connection timed out")


#     connection_established = False

#     try:
#         ArdObj = serial.Serial(com,115200,timeout=3)
#         timer = threading.Timer(10,timeout_handler)
#         timer.start()

#         time.sleep(3)

#         ArdObj.write('Ping\n'.encode())

#         recieveMsg = ArdObj.readline().decode().strip()
#         if recieveMsg == "Pong":
#             connection_established = True
#             ArdObj.close()
#             return True
#         else:
#             ArdObj.close()
#             return False

#     except Exception as e:
#         return str(e)

#     finally:
#         if 'ArdObj' in locals():
#             ArdObj.close()
#             timer.cancel()


# def send_coordinates(json_file,serial_port,master):
#     progress_view = tk.Toplevel(master)
#     progress_view.title("Progress")
#     progress_view.resizable(False,False)
#     progress_view.attributes("-topmost",1)
#     progress_frame = tk.Frame(progress_view)
#     progress_frame.grid()

#     with open(json_file) as file:
#         data = json.load(file)

#     steps = data[0]['task data']
#     total_steps = len(steps)

#     ser = serial.Serial(serial_port, baudrate=115200, timeout=3)  # Adjust baudrate if necessary
#     progress_variable = tk.DoubleVar()
#     progress_bar = tk.Canvas(progress_frame, width=200, height=20)
#     progress_bar.create_rectangle(0, 0, 200, 20, fill="grey")
#     progress_bar.create_rectangle(0, 0, 0, 20, fill="green", tags="progress")
#     progress_bar.grid(row=2, column=1)
#     progressing = tk.Label(progress_frame,text="Task is running, please wait...")
#     progressing.grid(row=3,column=1)
#     sv_ttk.set_theme("dark")

#     time.sleep(3)

#     for step_index, step in enumerate(steps):
#         if 'end' in step:
#             time.sleep(3)
#             endmsg = "end"
#             ser.write(endmsg.encode())
#             break

#         arm_number = step['arm']

#         if 'wait' in step:
#             wait_time = step['wait']
#             # Wait for the specified time
#             time.sleep(wait_time)
#         else:
#             coordinates = step
#             if 'end' in coordinates:
#                 break  # End the loop if "end" instruction is encountered


#             message = f"{arm_number}{coordinates['x']:03d}{coordinates['y']:03d}{coordinates['z']:03d}\n"
#             # print(message) #NOTE: USE TO DEBUG


#             ser.write(message.encode())
#               # Send the coordinates over serial
#             while True:
#                 response = ser.readline().decode().strip() # Read response from serial
#                 # print(response) #NOTE: USE TO DEBUG
#                 if response == "success":
#                     break  # Proceed to the next instruction
#                 elif response == "End":
#                     return

#         progress_variable.set((step_index / (total_steps - 1)) * 100)
#         progress = progress_variable.get()
#         progress_bar.coords("progress", (0, 0, progress * 2, 20))
#         progress_bar.delete("text")
#         progress_text = f"{int(progress)}%"
#         progress_bar.create_text(100, 10, text=progress_text, tags="text")
#         progress_view.update()
#     progress_variable.set(100)
#     progress = progress_variable.get()
#     progress_bar.coords("progress", (0, 0, progress * 2, 20))
#     progress_bar.delete("text")
#     progress_text = f"{int(progress)}%"
#     progress_bar.create_text(100, 10, text=progress_text, tags="text")
#     progress_view.destroy()


#     ser.close()
#     progress_view.mainloop()



# # send_coordinates("tasks/Task1.json","COM6",root)

# def retrv_cur_pos(arm_no,com_port):
#     ser = serial.Serial(com_port, baudrate=115200, timeout=3) # Adjust baudrate if necessary
#     time.sleep(3)
#     message = f"{arm_no}curpos\n"
#     ser.write(message.encode())
#     time.sleep(3)
#     response = ser.readline().decode().strip() # Read response from serial
#     ser.close()
#     # response = f"data sent to {com_port} and recieved successfully"
#     return response