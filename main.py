#==================================== Imports ====================================
import tkinter
from tkinter import ttk
import datetime
import sv_ttk
from PIL import ImageTk, Image
import taskcreator


#==================================== INIT Tkinter ====================================

# Initializing all require Tkinter functions
root = tkinter.Tk()
root.attributes('-fullscreen', True)
root.geometry("1920x1080")
root.title("Robotic Arm Software")
frame = tkinter.Frame(root)
frame.pack()


#==================================== INIT ASSETS ====================================

#Loading assets, initializing variables
play_image = ImageTk.PhotoImage(Image.open("assets/play.png").resize((30,30)))
pause_image = ImageTk.PhotoImage(Image.open("assets/pause.png").resize((30,30)))
stop_image = ImageTk.PhotoImage(Image.open("assets/stop.png").resize((30,30)))
close_image = ImageTk.PhotoImage(Image.open("assets/close.png").resize((30,30)))
minim_image = ImageTk.PhotoImage(Image.open("assets/minimize.png").resize((30,30)))
progress = 0
state = "stopped"
last_update = datetime.datetime.now()


#==================================== Define Panes ====================================

#essential ops
button_frame = tkinter.Frame(root)
button_frame.pack(side="top")

#Left pane
left_pane = tkinter.LabelFrame(frame, text="Options", padx=100)
left_pane.grid(row=0,column=0,padx=20,pady=20)

#Left bottom pane
left_bottom_pane = tkinter.LabelFrame(frame, text="Task List", padx=50)
left_bottom_pane.grid(row=1,column=0,padx=20,pady=20)

#Right pane
right_pane = tkinter.LabelFrame(frame, text="Arm Operations", pady=100)
right_pane.grid(row=0,column=2,padx=20,pady=20,rowspan=2)

#Middle pane
middle_pane = tkinter.LabelFrame(frame, text="Arm Statistics", padx=100)
middle_pane.grid(row=0,column=1,padx=20,pady=20)

#Middle bottom pane
middle_bottom_pane = tkinter.LabelFrame(frame, text="Movement Control", padx=100)
middle_bottom_pane.grid(row=1,column=1,padx=20,pady=20)


#==================================== Essential Functions ====================================

#Task Handler Loader
def callhandler():
    taskcreator.create_interface(root)

#==================================== Begin Widgets ====================================

#Top functions
close_app = ttk.Button(button_frame, image=close_image, command=root.destroy)
close_app.pack(side="right")
minimize_app = ttk.Button(button_frame, image=minim_image, command=root.iconify)
minimize_app.pack(side="right")

#Left pane widgets
style = ttk.Style()
style.configure('Custom.TButton', borderwidth=0, relief=0)
Task_opt = ttk.Label(left_pane, text="Task Options", padding=(20,20,20,20))
Task_opt.grid(row=0,column=0,padx=20,pady=20)
Task_opt.pack()
Load_task = ttk.Button(left_pane, text="Load Tasks", padding=(45,5), style="Custom.TButton")
Load_task.pack(pady=(10,0))
Save_task = ttk.Button(left_pane, text="Save Tasks", padding=(45,5))
Save_task.pack(pady=(10,0))
Add_task = ttk.Button(left_pane, text="Add Task", padding=(52,5),command=callhandler)
Add_task.pack(pady=(10,0))
Remove_task = ttk.Button(left_pane, text="Remove Task", padding=(39,5))
Remove_task.pack(pady=(10,10))

#Left bottom pane widgets
Task_list = ttk.Label(left_bottom_pane, text="Task List", padding=(20,20,20,20))
Task_list.grid(row=0,column=0,padx=20,pady=20)
Task_list.pack()
Task_list_box = tkinter.Listbox(left_bottom_pane, justify="center", font=("Helvetica", 12))
Task_list_box.pack(fill='x',expand='False')
for item in ['Task1','Task2','Task3']:
    Task_list_box.insert('end', item)
Select_task = ttk.Button(left_bottom_pane, text="Select Task", padding=(20,10,20,10),width=10)
Select_task.pack(side=tkinter.LEFT, padx=(10, 10), pady=10)
Run_task = ttk.Button(left_bottom_pane, text="Run Task", padding=(20,10,20,10),width=10)
Run_task.pack(side=tkinter.LEFT, padx=(10, 10), pady=10)
Task_list.pack_propagate(0)
Select_task.pack_propagate(0)
Run_task.pack_propagate(0)

#Middle pane widgets
arm1_label = tkinter.Label(middle_pane, text="Robotic Arm 1")
arm1_label.grid(row=0,column=0,padx=20,pady=20)
arm2_label = tkinter.Label(middle_pane, text="Robotic Arm 2")
arm2_label.grid(row=0,column=1,padx=20,pady=20)
arm1_button = tkinter.Button(middle_pane, text="Running", bg="green", width=10, command=lambda: switch_state(arm1_button))
arm1_button.grid(row=1, column=0, padx=10, pady=10)
arm2_button = tkinter.Button(middle_pane, text="Running", bg="green", width=10, command=lambda: switch_state(arm2_button))
arm2_button.grid(row=1, column=1, padx=10, pady=10)
progress_frame = tkinter.LabelFrame(middle_pane, text="Task Progress", padx=50)
progress_frame.grid(row=2,column=0,columnspan=2,padx=20,pady=20)
progress_bar = tkinter.Canvas(progress_frame, width=200,height=20)
progress_bar.create_rectangle(0, 0, 200, 20, fill="grey")
progress_bar.create_rectangle(0, 0, 0, 20, fill="green", tags="progress")
progress_bar.grid(row=2,column=1)

#Middle bottom pane widgets
Retrv_curr_pos = ttk.Button(middle_bottom_pane, text="Retrieve\nCurrent\nPosition", padding=(10,40))
Retrv_curr_pos.grid(row=0,column=0,rowspan=4,pady=(10,0),padx=(10,0),sticky='EW')
joint_label = ttk.Label(middle_bottom_pane, text="Joint Values")
joint_label.grid(row=0,column=1,pady=(10,0),padx=(10,0),sticky='W')
mv_to_joints = ttk.Button(middle_bottom_pane, text="Move to Joints", padding=(25,5))
mv_to_joints.grid(row=0,column=2,pady=(10,0),padx=(10,10),sticky='E')
mv_text_entry = ttk.Entry(middle_bottom_pane, width=45)
mv_text_entry.insert(0, "Enter the joint values")
mv_text_entry.grid(row=1,column=1,pady=(5,0),padx=(10,10),columnspan=2,sticky='W')
cart_pos = ttk.Label(middle_bottom_pane, text="Cartesian Position")
cart_pos.grid(row=2,column=1,pady=(10,0),padx=(10,0),sticky='W')
mv_to_cart = ttk.Button(middle_bottom_pane, text="Move to Position", padding=(12,5))
mv_to_cart.grid(row=2,column=2,pady=(10,0),padx=(10,10),sticky='E')
mv_text_entry2 = ttk.Entry(middle_bottom_pane, width=45)
mv_text_entry2.insert(0, "Enter the cartesian values")
mv_text_entry2.grid(row=3,column=1,pady=(5,10),padx=(10,10),columnspan=2,sticky='W')
time_label = ttk.Label(middle_bottom_pane, text="", padding=(20,20,20,20))
time_label.grid(row=4,column=0,padx=12,pady=12,columnspan=3)


#==================================== UI Update Functions ====================================

#Arm Selections UI Updates
def select_arm1():
    arm1_selector.configure(bg="green")
    arm2_selector.configure(bg="gray")
    arm2_button.configure(bg="Purple",text="Idle")
    arm1_button.configure(bg="Green",text="Running")

def select_arm2():
    arm1_selector.configure(bg="gray")
    arm2_selector.configure(bg="green")
    arm1_button.configure(bg="Purple",text="Idle")
    arm2_button.configure(bg="Green",text="Running")

def show_servo_spinbox():
    spinbox_distance.grid_forget()
    distance_label.grid_forget()
    label_null.grid_forget()
    degree_label.grid(row=5,column=0,padx=20,pady=20)
    spinbox_degree.grid(row=5,column=1,padx=20,pady=20)

def show_arm_spinbox():
    spinbox_degree.grid_forget()
    degree_label.grid_forget()
    label_null.grid_forget()
    distance_label.grid(row=5,column=0,padx=20,pady=20)
    spinbox_distance.grid(row=5,column=1,padx=20,pady=20)


#==================================== Widgets Contd. ====================================

#Right pane widgets
arm_selector = tkinter.LabelFrame(right_pane,text="Arm Selection",padx=50)
arm_selector.grid(row=0,column=0,padx=20,pady=20,columnspan=2)
com_selector = tkinter.Label(arm_selector,text="COM Port Selection")
com_selector.grid(row=1,column=0,padx=20,pady=20)
arm_combobox = ttk.Combobox(arm_selector,values=["","COM3","COM4","COM6","COM8"])
arm_combobox.grid(row=1,column=1,padx=20,pady=20)
arm1_selector = tkinter.Button(arm_selector,text="Select Arm1", command=select_arm1, bg="gray")
arm1_selector.grid(row=2,column=0,padx=20,pady=20)
arm2_selector = tkinter.Button(arm_selector,text="Select Arm2", command=select_arm2, bg="gray")
arm2_selector.grid(row=2,column=1,padx=20,pady=20)
arm_type_selector = tkinter.LabelFrame(right_pane,text="Select Movement Type",padx=110)
arm_type_selector.grid(row=3,column=0,padx=20,pady=20,columnspan=2)
servo_button = tkinter.Button(arm_type_selector, text="Move Servo", command=show_servo_spinbox)
arm_move_button = tkinter.Button(arm_type_selector, text="Move Arm", command=show_arm_spinbox)
servo_button.grid(row=4,column=0,padx=20,pady=20)
arm_move_button.grid(row=4,column=1,padx=20,pady=20)
label_null = tkinter.Label(arm_type_selector,text="Select Type of Movement")
label_null.grid(row=5,column=0,padx=20,pady=20,columnspan=2)
spinbox_degree = tkinter.Spinbox(arm_type_selector, from_=0, to=360, width=10)
degree_label = tkinter.Label(arm_type_selector,text="Step Degrees (°): ")
spinbox_distance = tkinter.Spinbox(arm_type_selector, from_=0, to=100, width=10)
distance_label = tkinter.Label(arm_type_selector,text="Step Distance (mm): ")

#6 buttons -Tx -Ty -Tz -Rx -Ry -Rz +Tx +Ty +Tz +Rx +Ry +Rz
tx_button = ttk.Button(right_pane,text="-Tx",padding=(40,10))
ty_button = ttk.Button(right_pane,text="-Ty",padding=(40,10))
tz_button = ttk.Button(right_pane,text="-Tz",padding=(40,10))
rx_button = ttk.Button(right_pane,text="-Rx",padding=(40,10))
ry_button = ttk.Button(right_pane,text="-Ry",padding=(40,10))
rz_button = ttk.Button(right_pane,text="-Rz",padding=(40,10))
tx_button.grid(row=6,column=0,padx=5,pady=5)
ty_button.grid(row=7,column=0,padx=5,pady=5)
tz_button.grid(row=8,column=0,padx=5,pady=5)
rx_button.grid(row=9,column=0,padx=5,pady=5)
ry_button.grid(row=10,column=0,padx=5,pady=5)
rz_button.grid(row=11,column=0,padx=5,pady=5)

tx_button = ttk.Button(right_pane,text="+Tx",padding=(40,10))
ty_button = ttk.Button(right_pane,text="+Ty",padding=(40,10))
tz_button = ttk.Button(right_pane,text="+Tz",padding=(40,10))
rx_button = ttk.Button(right_pane,text="+Rx",padding=(40,10))
ry_button = ttk.Button(right_pane,text="+Ry",padding=(40,10))
rz_button = ttk.Button(right_pane,text="+Rz",padding=(40,10))
tx_button.grid(row=6,column=1,padx=5,pady=5)
ty_button.grid(row=7,column=1,padx=5,pady=5)
tz_button.grid(row=8,column=1,padx=5,pady=5)
rx_button.grid(row=9,column=1,padx=5,pady=5)
ry_button.grid(row=10,column=1,padx=5,pady=5)
rz_button.grid(row=11,column=1,padx=5,pady=5)


#==================================== Begin Functions ====================================

#Button python code (Status Lambda function)
def switch_state(button):
    current_state = button['text']
    if current_state == 'Running':
        button['text'] = 'Error'
        button['bg'] = 'red'
    elif current_state == 'Error':
        button['text'] = 'Idle'
        button['bg'] = 'purple'
    else:
        button['text'] = 'Running'
        button['bg'] = 'green'

#Live time function
def update_time():
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    date_str = current_time.strftime("%Y-%m-%d")
    time_label.config(text="Current Time: " + time_str + "\nToday's Date: " + date_str)
    root.after(1000, update_time)


#==================================== Progress Bar Functions ====================================

# Progress Bar Code From Here
def start():
    global state
    global last_update
    global progress
    global progress_bar
    global time_delta
    if state == "stopped":
        # Set the state to "playing"
        state = "playing"

        # Enable the pause and stop buttons
        pause_button.config(state="normal")
        stop_button.config(state="normal")

        # Disable the play button
        play_button.config(state="disabled")

        # Set the time of the last update to the current time
        last_update = datetime.datetime.now()

    elif state == "paused":
        # Set the state to "playing"
        state = "playing"

        # Enable the pause and stop buttons
        pause_button.config(state="normal")
        stop_button.config(state="normal")

        # Disable the play button
        play_button.config(state="disabled")

        if last_update is None:
            last_update = datetime.datetime.now()

        # Calculate the time since the last update and add it to the last update time
        now = datetime.datetime.now()
        time_delta = (now - last_update).total_seconds()
        last_update += datetime.timedelta(seconds=time_delta)
        
def pause():
    global state
    global last_update
    global progress
    global progress_bar
    global time_delta
    if state == "playing":
        # Set the state to "paused"
        state = "paused"
        
        # Disable the pause button
        pause_button.config(state="disabled")
        
        # Enable the play button
        play_button.config(state="normal")
        
        # Set the time of the last update to None
        last_update = None
        
    elif state == "paused":
        # Set the state to "playing"
        state = "playing"
        
        # Enable the pause and stop buttons
        pause_button.config(state="normal")
        stop_button.config(state="normal")
        
        # Disable the play button
        play_button.config(state="disabled")
        
        # Set the time of the last update to the current time
        last_update = datetime.datetime.now()

def stop():
    global state
    global last_update
    global progress
    global progress_bar
    global time_delta
    if state != "stopped":
        # Set the state to "stopped"
        state = "stopped"
        
        # Disable the pause and stop buttons
        pause_button.config(state="disabled")
        stop_button.config(state="disabled")
        
        # Enable the play button
        play_button.config(state="normal")
        
        # Reset the progress to 0
        progress = 0
        progress_bar.coords("progress", (0, 0, 0, 20))
    
def update_progress():
    global state
    global last_update
    global progress
    global progress_bar
    global time_delta
    # Calculate the time since the last update
    now = datetime.datetime.now()
    time_delta = (now - last_update).total_seconds() if last_update is not None else 0
    if state == "playing" or state == "paused":
        # Update the progress based on the time delta
        if state == "playing":
            progress += time_delta * 10
        if state == "stopped":
            progress = 0
        
        progress = min(progress, 100)
        # Update the progress bar
        progress_bar.coords("progress", (0, 0, progress * 2, 20))
        # Remove the previous progress text
        progress_bar.delete("text")
        # Add the new progress text
        progress_text = f"{int(progress)}%"
        progress_bar.create_text(100, 10, text=progress_text, tags="text")
        # Check if the progress has reached 100%
        
        if progress >= 100:
            stop()
    # Set the time of the last update to the current time
    last_update = now
    # Call this function again after a short delay
    root.after(100, update_progress)

play_button = tkinter.Button(progress_frame, image=play_image, command=start)
pause_button = tkinter.Button(progress_frame, image=pause_image, state="disabled", command=pause)
stop_button = tkinter.Button(progress_frame, image=stop_image, state="disabled", command=stop)
play_button.grid(row=3,column=0, padx=20, pady=10)
pause_button.grid(row=3,column=1, padx=20, pady=10)
stop_button.grid(row=3,column=2, padx=20, pady=10)

update_progress()


#==================================== End Functions (Tkinter) ====================================

# This is where the magic happens
sv_ttk.set_theme("dark")
update_time()

root.mainloop()