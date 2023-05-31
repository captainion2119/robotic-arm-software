#==================================== Imports ====================================
import tkinter
from tkinter import ttk, messagebox
import datetime
import sv_ttk
import os
import json
from PIL import ImageTk, Image

#==================================== Importing Custom Modules ====================================
import taskcreator
import databridge

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
robo_arm_image = ImageTk.PhotoImage(Image.open("assets/arm.png").resize((256,256)))
path = "./tasks"
progress = 0
state = "stopped"
last_update = datetime.datetime.now()
com_ports = databridge.getPorts()
run_selection_file = None
run_selection_item = None
select_arm = None

#==================================== Define Panes ====================================

#essential opsD
button_frame = tkinter.Frame(root)
button_frame.pack(side="top")

#Left pane
left_pane = tkinter.LabelFrame(frame, text="Options", padx=100)
left_pane.grid(row=0,column=0,padx=20,pady=20)

#Left bottom pane
left_bottom_pane = tkinter.LabelFrame(frame, text="Task List", padx=50)
left_bottom_pane.grid(row=1,column=0,padx=20,pady=20)

#Right pane
right_pane = tkinter.LabelFrame(frame, text="Arm Operations", pady=50)
right_pane.grid(row=0,column=2,padx=20,pady=20,rowspan=2)

#Middle pane
middle_pane = tkinter.LabelFrame(frame, padx=50, bg="gray")
middle_pane.grid(row=0,column=1,padx=20,pady=20)

#Middle bottom pane
middle_bottom_pane = tkinter.LabelFrame(frame, text="Movement Control", padx=50)
middle_bottom_pane.grid(row=1,column=1,padx=20,pady=20)


#==================================== Essential Functions ====================================

#Task Handler Loader
def callhandler():
    taskcreator.create_interface_angles(root)

def load_tasks():
    files = [f for f in os.listdir(path) if f.endswith('.json')]
    if Task_list_box.size()>0:
        Task_list_box.delete(0,tkinter.END)
        load_tasks()
    else:
        for filename in files:
            with open(os.path.join(path, filename), 'r') as f:
                task = json.load(f)
                task_name = task[0]["task name"]
                Task_list_box.insert(tkinter.END, task_name)
    
def remove_task():
    selected_file = Task_list_box.curselection()
    if selected_file:
        selected_item = [Task_list_box.get(index) for index in selected_file]
        response = messagebox.askquestion("Confirmation",f"Are you sure you want to delete {selected_item[0]}",icon="warning",parent=root)
        if response == "yes":
            os.remove(os.path.join(path, selected_item[0]+".json"))
            load_tasks()
        else:
            return
    else:
        messagebox.showwarning("Warning","No Item selected!")

def callviewer():
    selected_file = Task_list_box.curselection()
    if selected_file:
        selected_item = [Task_list_box.get(index) for index in selected_file]
        taskcreator.list_interface(root,selected_item[0])
    else:
        messagebox.showerror("Error","No task selected",parent=root)

def get_ports():
    global com_ports
    com_ports = databridge.getPorts()
    arm_combobox['values'] = com_ports
    root.after(10000,get_ports)

def on_select_com(event):
    selected_port = arm_combobox.get()
    messagebox.showinfo("Info",f"{selected_port} selected!")
    response = databridge.testConnection(selected_port)
    if response == True:
        messagebox.showinfo("Info","Connection Successful!")
    elif response != True or False:
        messagebox.showerror("Error", response)
    else:
        messagebox.showerror("Error","Connection Failed!")

def select_task():
    global run_selection_file
    global run_selection_item
    run_selection_file = Task_list_box.curselection()
    run_selection_item = [Task_list_box.get(index) for index in run_selection_file]
    run_selection_item = run_selection_item[0]
    run_selection_item = str(run_selection_item)
    if run_selection_item:
        messagebox.showinfo("Selected","file has been selected, you may run the task now",parent=root)
    else:
        messagebox.showerror("Error","No task selected",parent=root)

def run_task():
    run_port = arm_combobox.get()
    if run_port:
        if run_selection_item is not None:
            run_file = f"tasks\{run_selection_item}.json"
            # play_button.invoke()
            databridge.send_coordinates(run_file,run_port,root)
        else:
            messagebox.showerror("Error","No file selected",parent=root)
    else:
        messagebox.showerror("Error","No port selected")

def getcurpos():
    arm_no = select_arm
    run_port = arm_combobox.get()
    if arm_no is not None:
        if run_port:
            resp = databridge.retrv_cur_pos(arm_no,run_port)
            resp_x = int(resp[:3])
            resp_y = int(resp[3:6])
            resp_z = int(resp[6:9])
            mv_text_entry2.delete(0, "end")
            mv_text_entry2.insert(0, "")
            mv_text_entry2.insert(0, f"X: {resp_x}, Y: {resp_y}, Z: {resp_z}")
        else:
            messagebox.showerror("Error","No port selected!")
    else:
        messagebox.showerror("Error","No arm selected")

def on_entry_click(event, entry):
        if entry.cget("fg") == "grey":
            entry.delete(0, "end")
            entry.insert(0, "")
            entry.config(fg="white")

def on_focusout(event, entry, text):
    if entry.get() == "":
        entry.insert(0, text)
        entry.config(fg="grey")


#==================================== Begin Widgets ====================================

#Close minimize util functions
button_frame = tkinter.LabelFrame(middle_pane)
button_frame.grid(row=1,column=1,columnspan=2)
close_app = ttk.Button(button_frame, image=close_image, command=root.destroy)
close_app.grid(row=0,column=0)
minimize_app = ttk.Button(button_frame, image=minim_image, command=root.iconify)
minimize_app.grid(row=0,column=1)

#Left pane widgets
style = ttk.Style()
style.configure('Custom.TButton', borderwidth=0, relief=0)
Task_opt = ttk.Label(left_pane, text="Task Options", padding=(20,20,20,20))
Task_opt.grid(row=0,column=0,padx=20,pady=20)
Task_opt.pack()
Load_task = ttk.Button(left_pane, text="Load Tasks", padding=(45,5), style="Custom.TButton",command=load_tasks)
Load_task.pack(pady=(10,0))
View_task = ttk.Button(left_pane, text="View Task", padding=(45,5),command=callviewer)
View_task.pack(pady=(10,0))
Add_task = ttk.Button(left_pane, text="Add Task", padding=(52,5),command=callhandler)
Add_task.pack(pady=(10,0))
Remove_task = ttk.Button(left_pane, text="Remove Task", padding=(39,5),command=remove_task)
Remove_task.pack(pady=(10,10))

#Left bottom pane widgets
Task_list = ttk.Label(left_bottom_pane, text="Task List", padding=(20,20,20,20))
Task_list.grid(row=0,column=0,padx=20,pady=20)
Task_list.pack()
Task_list_box = tkinter.Listbox(left_bottom_pane, justify="center", font=("Helvetica", 12))
Task_list_box.pack(fill='x',expand='False')
Select_task = ttk.Button(left_bottom_pane, text="Select Task", padding=(20,10,20,10),width=10,command=select_task)
Select_task.pack(side=tkinter.LEFT, padx=(10, 10), pady=10)
Run_task = ttk.Button(left_bottom_pane, text="Run Task", padding=(20,10,20,10),width=10,command=run_task)
Run_task.pack(side=tkinter.LEFT, padx=(10, 10), pady=10)
Task_list.pack_propagate(0)
Select_task.pack_propagate(0)
Run_task.pack_propagate(0)

#Middle pane widgets
arm_images = tkinter.Label(middle_pane,image=robo_arm_image,bg="gray")
arm_images.grid(row=0,column=0)
arm_text = tkinter.Label(middle_pane,text="ROBOTIC \nARM \nSOFTWARE", font=("Helvetica", 24),bg="gray")
arm_text.grid(row=0,column=1)

#Middle bottom pane widgets
Retrv_curr_pos = ttk.Button(middle_bottom_pane, text="Retrieve\nCurrent\nPosition", padding=(10,40),command=getcurpos)
Retrv_curr_pos.grid(row=0,column=0,rowspan=4,pady=(10,0),padx=(10,0),sticky='EW')
joint_label = ttk.Label(middle_bottom_pane, text="Joint Values")
joint_label.grid(row=0,column=1,pady=(10,0),padx=(10,0),sticky='W')
mv_to_joints = ttk.Button(middle_bottom_pane, text="Move to Joints", padding=(25,5))
mv_to_joints.grid(row=0,column=2,pady=(10,0),padx=(10,10),sticky='E')
mv_text_entry = tkinter.Entry(middle_bottom_pane, width=45,fg="grey")
mv_text_entry.insert(0, "Enter the joint values")
mv_text_entry.grid(row=1,column=1,pady=(5,0),padx=(10,10),columnspan=2,sticky='W')
cart_pos = ttk.Label(middle_bottom_pane, text="Cartesian Position")
cart_pos.grid(row=2,column=1,pady=(10,0),padx=(10,0),sticky='W')
mv_to_cart = ttk.Button(middle_bottom_pane, text="Move to Position", padding=(12,5))
mv_to_cart.grid(row=2,column=2,pady=(10,0),padx=(10,10),sticky='E')
mv_text_entry2 = tkinter.Entry(middle_bottom_pane, width=45,fg="grey")
mv_text_entry2.insert(0, "Enter the cartesian values")
mv_text_entry2.grid(row=3,column=1,pady=(5,10),padx=(10,10),columnspan=2,sticky='W')
time_label = ttk.Label(middle_bottom_pane, text="", padding=(20,20,20,20))
time_label.grid(row=4,column=0,padx=12,pady=12,columnspan=3)

mv_text_entry.bind("<FocusIn>",lambda event: on_entry_click(event,mv_text_entry))
mv_text_entry.bind("<FocusOut>",lambda event: on_focusout(event,mv_text_entry,"Enter the joint values"))
mv_text_entry2.bind("<FocusIn>",lambda event: on_entry_click(event,mv_text_entry2))
mv_text_entry2.bind("<FocusOut>",lambda event: on_focusout(event,mv_text_entry2,"Enter the cartesian values"))


#==================================== UI Update Functions ====================================

#Arm Selections UI Updates
def select_arm1():
    global select_arm
    arm1_selector.configure(bg="green")
    arm2_selector.configure(bg="gray")
    select_arm = 1


def select_arm2():
    global select_arm
    arm1_selector.configure(bg="gray")
    arm2_selector.configure(bg="green")
    select_arm = 2


def send_one_move(run_ang):
    run_port = arm_combobox.get()
    amt = spinbox_degree.get()
    print(amt)
    if run_port:
        # play_button.invoke()
        databridge.move_by_one(run_ang,amt,run_port)
    else:
        messagebox.showerror("Error","No port selected")


#==================================== Widgets Contd. ====================================

#Right pane widgets
arm_selector = tkinter.LabelFrame(right_pane,text="Arm Selection")
arm_selector.grid(row=0,column=0,padx=20,pady=20,columnspan=2)
com_selector = tkinter.Label(arm_selector,text="COM Port Selection")
com_selector.grid(row=1,column=0,padx=20,pady=20)
arm_combobox = ttk.Combobox(arm_selector,values=com_ports,state="readonly")
arm_combobox.grid(row=1,column=1,padx=20,pady=20)
arm1_selector = tkinter.Button(arm_selector,text="Select Arm1", command=select_arm1, bg="gray")
arm1_selector.grid(row=2,column=0,padx=20,pady=20)
arm2_selector = tkinter.Button(arm_selector,text="Select Arm2", command=select_arm2, bg="gray")
arm2_selector.grid(row=2,column=1,padx=20,pady=20)
arm_type_selector = tkinter.LabelFrame(right_pane,text="Select Movement Type",padx=80)
arm_type_selector.grid(row=3,column=0,padx=20,pady=20,columnspan=2)
spinbox_degree = tkinter.Spinbox(arm_type_selector, from_=10, to=90, width=10)
degree_label = tkinter.Label(arm_type_selector,text="Step Degrees (°): ")
degree_label.grid(row=5,column=0,padx=20,pady=20)
spinbox_degree.grid(row=5,column=1,padx=20,pady=20)


#6 buttons -Tx -Ty -Tz -Rx -Ry -Rz +Tx +Ty +Tz +Rx +Ry +Rz
tx_button = ttk.Button(right_pane,text="-Tx",padding=(40,10),command=lambda: send_one_move("rs1"))
ty_button = ttk.Button(right_pane,text="-Ty",padding=(40,10),command=lambda: send_one_move("rs2"))
tz_button = ttk.Button(right_pane,text="-Tz",padding=(40,10),command=lambda: send_one_move("rs3"))
rx_button = ttk.Button(right_pane,text="-Rx",padding=(40,10),command=lambda: send_one_move("rs4"))
ry_button = ttk.Button(right_pane,text="-Ry",padding=(40,10),command=lambda: send_one_move("rs5"))
rz_button = ttk.Button(right_pane,text="-Rz",padding=(40,10),command=lambda: send_one_move("rs6"))
tx_button.grid(row=6,column=0,padx=5,pady=5)
ty_button.grid(row=7,column=0,padx=5,pady=5)
tz_button.grid(row=8,column=0,padx=5,pady=5)
rx_button.grid(row=9,column=0,padx=5,pady=5)
ry_button.grid(row=10,column=0,padx=5,pady=5)
rz_button.grid(row=11,column=0,padx=5,pady=5)

tx_button = ttk.Button(right_pane,text="+Tx",padding=(40,10),command=lambda: send_one_move("s1"))
ty_button = ttk.Button(right_pane,text="+Ty",padding=(40,10),command=lambda: send_one_move("s2"))
tz_button = ttk.Button(right_pane,text="+Tz",padding=(40,10),command=lambda: send_one_move("s3"))
rx_button = ttk.Button(right_pane,text="+Rx",padding=(40,10),command=lambda: send_one_move("s4"))
ry_button = ttk.Button(right_pane,text="+Ry",padding=(40,10),command=lambda: send_one_move("s5"))
rz_button = ttk.Button(right_pane,text="+Rz",padding=(40,10),command=lambda: send_one_move("s6"))
tx_button.grid(row=6,column=1,padx=5,pady=5)
ty_button.grid(row=7,column=1,padx=5,pady=5)
tz_button.grid(row=8,column=1,padx=5,pady=5)
rx_button.grid(row=9,column=1,padx=5,pady=5)
ry_button.grid(row=10,column=1,padx=5,pady=5)
rz_button.grid(row=11,column=1,padx=5,pady=5)

arm_combobox.bind("<<ComboboxSelected>>",on_select_com)

#==================================== Begin Functions ====================================

#Live time function
def update_time():
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    date_str = current_time.strftime("%Y-%m-%d")
    time_label.config(text="Current Time: " + time_str + "\nToday's Date: " + date_str)
    root.after(1000, update_time)


#==================================== Closing Functions (Util) ====================================

get_ports()

#==================================== End Functions (Tkinter) ====================================

# This is where the magic happens
sv_ttk.set_theme("dark")
update_time()

root.mainloop()