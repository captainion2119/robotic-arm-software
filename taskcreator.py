import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import json
import os

def create_interface(master):
    #====================== Tkinter window creation ======================

    data_entry_window = tk.Toplevel(master)
    data_entry_window.title("Task Creator")
    data_entry_window.resizable(False,False)
    data_entry_window.attributes("-topmost",1)
    data_entry_frame = tk.Frame(data_entry_window)
    data_entry_frame.grid()


    #====================== Variable Init ======================

    tasks = []
    wait_time_append = []
    arm_var = tk.IntVar()
    check1_var = tk.BooleanVar()
    check2_var = tk.BooleanVar()
    def set_arm1():
        arm_var.set(1)
        check2_var.set(False)
    def set_arm2():
        arm_var.set(2)
        check1_var.set(False)
    directory = "tasks/"


    #====================== Begin UI ======================

    data_label_master = tk.LabelFrame(data_entry_frame, text="")
    label_main = tk.Label(data_label_master,text="Task Creator",font=("Helvetica",18))
    separator_0 = ttk.Separator(data_label_master, orient="horizontal")
    task_name = tk.Label(data_label_master,text="Task name")
    separator_1 = ttk.Separator(data_label_master, orient="horizontal")
    arm_label = tk.Label(data_label_master,text="Select arm")
    arm1_button = tk.Checkbutton(data_label_master,text="Arm 1", command=set_arm1,selectcolor="black",variable=check1_var)
    arm2_button = tk.Checkbutton(data_label_master,text="Arm 2", command=set_arm2,selectcolor="black",variable=check2_var)
    separator_4 = ttk.Separator(data_label_master,orient="horizontal")
    coord_x = tk.Label(data_label_master, text="X coordinate")
    coord_y = tk.Label(data_label_master, text="Y coordinate")
    coord_z = tk.Label(data_label_master, text="Z coordinate")
    wait_time = tk.Label(data_label_master, text="Wait time (seconds)")


    #====================== Begin Formatting ======================
    
    data_label_master.grid(row=0, column=0)
    label_main.grid(row=0,column=1)
    separator_0.grid(row=1,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    task_name.grid(row=2,column=0,padx=20,pady=20)
    separator_1.grid(row=3,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    arm_label.grid(row=4,column=0)
    arm1_button.grid(row=4,column=1,padx=20,pady=20)
    arm2_button.grid(row=4,column=2,padx=20,pady=20)
    separator_4.grid(row=5,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    coord_x.grid(row=6, column=0, padx=20, pady=20)
    coord_y.grid(row=6, column=1, padx=20, pady=20)
    coord_z.grid(row=6, column=2, padx=20, pady=20)
    wait_time.grid(row=9, column=0, padx=20, pady=20)


    #====================== Lambda Functions ======================

    def on_entry_click(event, entry):
        if entry.cget("fg") == "grey":
            entry.delete(0, "end")
            entry.insert(0, "")
            entry.config(fg="white")

    def on_focusout(event, entry, text):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")

    
    #====================== Entry Fields Definition ======================

    task_name_entry = tk.Entry(data_label_master,fg="grey")
    coord_x_entry = tk.Entry(data_label_master, fg="grey")
    coord_y_entry = tk.Entry(data_label_master, fg="grey")
    coord_z_entry = tk.Entry(data_label_master, fg="grey")
    separator_2 = ttk.Separator(data_label_master, orient="horizontal")
    wait_text = tk.Entry(data_label_master, fg="grey")
    separator_3 = ttk.Separator(data_label_master, orient="horizontal")


    #====================== Entry Fields Formatting ======================

    task_name_entry.insert(0,"Enter Task name")
    task_name_entry.bind("<FocusIn>",lambda event: on_entry_click(event,task_name_entry))
    task_name_entry.bind("<FocusOut>",lambda event: on_focusout(event,task_name_entry,"Enter Task Name"))
    task_name_entry.grid(row=2,column=1,padx=20,pady=20)
    coord_x_entry.insert(0, "Enter X coord")
    coord_x_entry.bind("<FocusIn>", lambda event: on_entry_click(event, coord_x_entry))
    coord_x_entry.bind("<FocusOut>", lambda event: on_focusout(event,coord_x_entry, "Enter X coord"))
    coord_x_entry.grid(row=7, column=0, padx=20, pady=20)
    coord_y_entry.insert(0, "Enter Y coord")
    coord_y_entry.bind("<FocusIn>", lambda event: on_entry_click(event, coord_y_entry))
    coord_y_entry.bind("<FocusOut>", lambda event: on_focusout(event,coord_y_entry, "Enter Y coord"))
    coord_y_entry.grid(row=7, column=1, padx=20, pady=20)
    coord_z_entry.insert(0, "Enter Z coord")
    coord_z_entry.bind("<FocusIn>", lambda event: on_entry_click(event, coord_z_entry))
    coord_z_entry.bind("<FocusOut>", lambda event: on_focusout(event,coord_z_entry, "Enter Z coord"))
    coord_z_entry.grid(row=7, column=2, padx=20, pady=20)
    separator_2.grid(row=8,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    wait_text.insert(0, "Enter wait time")
    wait_text.bind("<FocusIn>", lambda event: on_entry_click(event, wait_text))
    wait_text.bind("<FocusOut>", lambda event: on_focusout(event,wait_text, "Enter wait time"))
    wait_text.grid(row=9, column=1, padx=20, pady=20)
    separator_3.grid(row=10,columnspan=4,sticky="ew",pady=(5,5),ipady=2)


    #====================== Button Functions ======================

    def add_task():
        task_name = task_name_entry.get()
        coord_x = coord_x_entry.get()
        coord_y = coord_y_entry.get()
        coord_z = coord_z_entry.get()
        wait_time = wait_text.get()
        arm = arm_var.get()
        check1 = check1_var.get()
        check2 = check2_var.get()


        if task_name == "" or task_name == "Enter Task name":
            messagebox.showerror("Error", "Please enter a Task name",parent=data_entry_window)
            return
        else:

            task_name_entry.config(state=tk.DISABLED)
            if check1 == False and check2 == False:
                messagebox.showerror("Error", "Please select an arm",parent=data_entry_window)
                return
            else:
                if coord_x == "" or coord_y == "" or coord_z == "" or coord_x == "Enter X coord" or coord_y == "Enter Y coord" or coord_z == "Enter Z coord":
                    if wait_time == "" or wait_time == "Enter wait time":
                        messagebox.showerror("Error", "Please enter all coordinates",parent=data_entry_window)
                        return
                    else:
                        coord_x = coord_y = coord_z = -1

                task_data = [{"arm":int(arm),"x": int(coord_x), "y": int(coord_y), "z": int(coord_z)}]

                if wait_time != "Enter wait time":
                    if coord_x != -1 and coord_y != -1 and coord_z != -1:
                        messagebox.showerror("Error","Coordinates have to be empty to enter wait command",parent=data_entry_window)
                        return
                    else:
                        wait_time_append.append({"arm":int(arm),"wait": int(wait_time)})

                for task in tasks:
                    if task["task name"] == task_name:
                        if coord_x == -1 and coord_y == -1 and coord_z == -1:
                            task["task data"].extend(wait_time_append)
                            wait_time_append.clear()
                            break
                        else:
                            task["task data"].extend(task_data)
                            break
                else:
                    task = {"task name": task_name, "task data": task_data}
                    tasks.append(task)

                update_list_view(list_view,tasks)

    def update_list_view(list_view, tasks):
        # Clear existing items in the list view
        list_view.delete(0, tk.END)

        # Loop over tasks and their steps, and add formatted strings to the list view
        for task in tasks:
            task_name = task["task name"]
            task_data = task["task data"]

            # Add task name as a heading
            list_view.insert(tk.END, f"Task: {task_name}")

            # Loop over task steps and add formatted strings to the list view
            for step in task_data:
                if "wait" in step:
                    list_view.insert(tk.END, f"Wait arm{step['arm']} for {step['wait']} seconds")
                elif "end" in step:
                    list_view.insert(tk.END, "End of task")
                else:
                    arm = step["arm"]
                    x = step["x"]
                    y = step["y"]
                    z = step["z"]
                    list_view.insert(tk.END, f"Move arm{arm} to x={x}, y={y}, z={z}")

            # Add an empty line after each task
            list_view.insert(tk.END, "")

    def clear_task():
        response = messagebox.askquestion("Confirmation","Are you sure you want to clear all data?",icon="warning",parent=data_entry_window)

        if response == "yes":
            tasks.clear()
            update_list_view(list_view,tasks)
            task_name_entry.config(state=tk.NORMAL)
            task_name_entry.delete(0,tk.END)
            coord_x_entry.delete(0,tk.END)
            coord_y_entry.delete(0,tk.END)
            coord_z_entry.delete(0,tk.END)
            wait_text.delete(0,tk.END)

            on_focusout(None,task_name_entry,"Enter Task name")
            on_focusout(None,coord_x_entry,"Enter X coord")
            on_focusout(None,coord_y_entry,"Enter Y coord")
            on_focusout(None,coord_z_entry,"Enter Z coord")
            on_focusout(None,wait_text,"Enter wait time")
            check1_var.set(False)
            check2_var.set(False)
        
        if response == "no":
            return
        
    def clear_task_force():
        tasks.clear()
        update_list_view(list_view,tasks)
        task_name_entry.config(state=tk.NORMAL)
        task_name_entry.delete(0,tk.END)
        coord_x_entry.delete(0,tk.END)
        coord_y_entry.delete(0,tk.END)
        coord_z_entry.delete(0,tk.END)
        wait_text.delete(0,tk.END)
        on_focusout(None,task_name_entry,"Enter Task name")
        on_focusout(None,coord_x_entry,"Enter X coord")
        on_focusout(None,coord_y_entry,"Enter Y coord")
        on_focusout(None,coord_z_entry,"Enter Z coord")
        on_focusout(None,wait_text,"Enter wait time")
        check1_var.set(False)
        check2_var.set(False)
        
    def save_task():
        task_name = task_name_entry.get()
        if os.path.isfile(directory + task_name + ".json"):
            messagebox.showerror("Error","A task with the same name exists already!",parent=data_entry_window)

        else:
            if len(tasks) == 0:
                messagebox.showerror("Error","Please enter a task",parent=data_entry_window)
                return
            else:
                #add {"end":True} to the end of tasks
                tasks[-1]["task data"].append({"end":True})
                with open(f"{directory}{task_name}"+".json", "w") as f:
                    json.dump(tasks, f, indent=4)
                messagebox.showinfo("Success","Tasks saved successfully",parent=data_entry_window)
                clear_task_force()
                return
            

    #====================== Buttons ======================

    button_add = tk.Button(data_label_master,text="Add",width=10,command=add_task)
    button_clear = tk.Button(data_label_master,text="Clear",width=10,command=clear_task)
    button_save = tk.Button(data_label_master,text="Save",width=10,command=save_task)
    list_view_frame = tk.LabelFrame(data_label_master,text="Entered Tasks",font=("Helvetica",12))
    list_view = tk.Listbox(list_view_frame, justify="center", font=("Helvetica", 12))

    #====================== Buttons Formatting ======================

    button_add.grid(row=11,column=0,padx=20,pady=20)
    button_clear.grid(row=11,column=1,padx=20,pady=20)
    button_save.grid(row=11,column=2,padx=20,pady=20)
    list_view_frame.grid(row=0,column=4,rowspan=12,sticky="NS")
    list_view.grid(row=0,column=1,ipady=130,ipadx=40)

    #====================== Tkinter End Statements ======================
    sv_ttk.set_theme("dark")
    data_entry_window.mainloop()


#create_interface(root)

def list_interface(master,file):
    list_view_window = tk.Toplevel(master)
    list_view_window.title("Task Creator")
    list_view_window.resizable(False,False)
    list_view_window.attributes("-topmost",1)
    list_view_frame = tk.Frame(list_view_window)
    list_view_frame.grid()

    list_view = tk.LabelFrame(list_view_frame, text="Task Data")
    list_view.grid(row=0,column=1,columnspan=2)

    list = tk.Listbox(list_view,justify="left",font=("Helvetica",12))
    list.grid(row=0,column=2,columnspan=3,padx=20,pady=20,ipadx=40,ipady=60)

    path = "tasks/" + file + ".json"
    with open(path,"r") as f:
        data = json.load(f)
    
    list.delete(0,tk.END)
    for task in data:
        task_name = task["task name"]
        task_data = task["task data"]
        # Add task name as a heading
        list.insert(tk.END, f"Task Name: {task_name}")
        # Loop over task steps and add formatted strings to the list view
        for step in task_data:
            if "wait" in step:
                list.insert(tk.END, f"Arm{step['arm']} wait for {step['wait']} seconds")
            elif "end" in step:
                list.insert(tk.END, f"End task")
            else:
                arm = step["arm"]
                x = step["x"]
                y = step["y"]
                z = step["z"]
                list.insert(tk.END, f"Move arm{arm} to x:{x}, y:{y}, z:{z}")
        list.insert(tk.END, "")


def create_interface_angles(master):
    #====================== Tkinter window creation ======================

    data_entry_window = tk.Toplevel(master)
    data_entry_window.title("Task Creator")
    # data_entry_window.resizable(False,False)
    data_entry_window.attributes("-topmost",1)
    data_entry_frame = tk.Frame(data_entry_window)
    data_entry_frame.grid()


    #====================== Variable Init ======================

    tasks = []
    wait_time_append = []
    arm_var = tk.IntVar()
    check1_var = tk.BooleanVar()
    check2_var = tk.BooleanVar()
    def set_arm1():
        arm_var.set(1)
        check2_var.set(False)
    def set_arm2():
        arm_var.set(2)
        check1_var.set(False)
    directory = "tasks/"


    #====================== Begin UI ======================

    data_label_master = tk.LabelFrame(data_entry_frame, text="")
    label_main = tk.Label(data_label_master,text="Task Creator",font=("Helvetica",18))
    separator_0 = ttk.Separator(data_label_master, orient="horizontal")
    task_name = tk.Label(data_label_master,text="Task name")
    separator_1 = ttk.Separator(data_label_master, orient="horizontal")
    arm_label = tk.Label(data_label_master,text="Select arm")
    arm1_button = tk.Checkbutton(data_label_master,text="Arm 1", command=set_arm1,selectcolor="black",variable=check1_var)
    arm2_button = tk.Checkbutton(data_label_master,text="Arm 2", command=set_arm2,selectcolor="black",variable=check2_var)
    separator_4 = ttk.Separator(data_label_master,orient="horizontal")
    servo_1 = tk.Label(data_label_master, text="servo 1")
    servo_2 = tk.Label(data_label_master, text="servo 2")
    servo_3 = tk.Label(data_label_master, text="servo 3")
    servo_4 = tk.Label(data_label_master, text="servo 4")
    servo_5 = tk.Label(data_label_master, text="servo 5")
    wait_time = tk.Label(data_label_master, text="Wait time (seconds)")


    #====================== Begin Formatting ======================
    
    data_label_master.grid(row=0, column=0)
    label_main.grid(row=0,column=1)
    separator_0.grid(row=1,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    task_name.grid(row=2,column=0,padx=20,pady=20)
    separator_1.grid(row=3,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    arm_label.grid(row=4,column=0)
    arm1_button.grid(row=4,column=1,padx=20,pady=20)
    arm2_button.grid(row=4,column=2,padx=20,pady=20)
    separator_4.grid(row=5,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    servo_1.grid(row=6, column=0, padx=20, pady=20)
    servo_2.grid(row=6, column=1, padx=20, pady=20)
    servo_3.grid(row=6, column=2, padx=20, pady=20)
    servo_4.grid(row=6, column=3, padx=20, pady=20)
    servo_5.grid(row=6, column=4, padx=20, pady=20)
    wait_time.grid(row=9, column=0, padx=20, pady=20)


    #====================== Lambda Functions ======================

    def on_entry_click(event, entry):
        if entry.cget("fg") == "grey":
            entry.delete(0, "end")
            entry.insert(0, "")
            entry.config(fg="white")

    def on_focusout(event, entry, text):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")

    
    #====================== Entry Fields Definition ======================

    task_name_entry = tk.Entry(data_label_master,fg="grey")
    servo_1_entry = tk.Entry(data_label_master, fg="grey")
    servo_2_entry = tk.Entry(data_label_master, fg="grey")
    servo_3_entry = tk.Entry(data_label_master, fg="grey")
    servo_4_entry = tk.Entry(data_label_master, fg="grey")
    servo_5_entry = tk.Entry(data_label_master, fg="grey")
    separator_2 = ttk.Separator(data_label_master, orient="horizontal")
    wait_text = tk.Entry(data_label_master, fg="grey")
    separator_3 = ttk.Separator(data_label_master, orient="horizontal")


    #====================== Entry Fields Formatting ======================

    task_name_entry.insert(0,"Enter Task name")
    task_name_entry.bind("<FocusIn>",lambda event: on_entry_click(event,task_name_entry))
    task_name_entry.bind("<FocusOut>",lambda event: on_focusout(event,task_name_entry,"Enter Task Name"))
    task_name_entry.grid(row=2,column=1,padx=20,pady=20)
    servo_1_entry.insert(0, "Enter servo 1 angle")
    servo_1_entry.bind("<FocusIn>", lambda event: on_entry_click(event, servo_1_entry))
    servo_1_entry.bind("<FocusOut>", lambda event: on_focusout(event,servo_1_entry, "Enter servo 1 angle"))
    servo_1_entry.grid(row=7, column=0, padx=20, pady=20)
    servo_2_entry.insert(0, "Enter servo 2 angle")
    servo_2_entry.bind("<FocusIn>", lambda event: on_entry_click(event, servo_2_entry))
    servo_2_entry.bind("<FocusOut>", lambda event: on_focusout(event,servo_2_entry, "Enter servo 2 angle"))
    servo_2_entry.grid(row=7, column=1, padx=20, pady=20)
    servo_3_entry.insert(0, "Enter servo 3 angle")
    servo_3_entry.bind("<FocusIn>", lambda event: on_entry_click(event,  servo_3_entry))
    servo_3_entry.bind("<FocusOut>", lambda event: on_focusout(event, servo_3_entry, "Enter servo 3 angle"))
    servo_3_entry.grid(row=7, column=2, padx=20, pady=20)
    servo_4_entry.insert(0, "Enter servo 4 angle")
    servo_4_entry.bind("<FocusIn>", lambda event: on_entry_click(event,  servo_4_entry))
    servo_4_entry.bind("<FocusOut>", lambda event: on_focusout(event, servo_4_entry, "Enter servo 4 angle"))
    servo_4_entry.grid(row=7, column=3, padx=20, pady=20)
    servo_5_entry.insert(0, "Enter servo  angle")
    servo_5_entry.bind("<FocusIn>", lambda event: on_entry_click(event,  servo_5_entry))
    servo_5_entry.bind("<FocusOut>", lambda event: on_focusout(event, servo_5_entry, "Enter servo 5 angle"))
    servo_5_entry.grid(row=9, column=3, padx=20, pady=20)
    separator_2.grid(row=8,columnspan=6,sticky="ew",pady=(5,5),ipady=2)
    wait_text.insert(0, "Enter wait time")
    wait_text.bind("<FocusIn>", lambda event: on_entry_click(event, wait_text))
    wait_text.bind("<FocusOut>", lambda event: on_focusout(event,wait_text, "Enter wait time"))
    wait_text.grid(row=9, column=1, padx=20, pady=20)
    separator_3.grid(row=10,columnspan=6,sticky="ew",pady=(5,5),ipady=2)


    #====================== Button Functions ======================

    def add_task():
        task_name = task_name_entry.get()
        servo_1 = servo_1_entry.get()
        servo_2 = servo_2_entry.get()
        servo_3 = servo_3_entry.get()
        servo_4 = servo_4_entry.get()
        servo_5 = servo_5_entry.get()
        wait_time = wait_text.get()
        arm = arm_var.get()
        check1 = check1_var.get()
        check2 = check2_var.get()


        if task_name == "" or task_name == "Enter Task name":
            messagebox.showerror("Error", "Please enter a Task name",parent=data_entry_window)
            return
        else:

            task_name_entry.config(state=tk.DISABLED)
            if check1 == False and check2 == False:
                messagebox.showerror("Error", "Please select an arm",parent=data_entry_window)
                return
            else:
                if servo_1 == "" or servo_2 == "" or servo_3 == "" or servo_4 == "" or servo_5 == "" or servo_1 == "Enter servo 1 angle" or servo_2 == "Enter servo 2 angle" or servo_3 == "Enter 3 servo angle" or servo_4 == "Enter 4 servo angle" or servo_5 == "Enter 5 servo angle":
                    if wait_time == "" or wait_time == "Enter wait time":
                        messagebox.showerror("Error", "Please enter all angles",parent=data_entry_window)
                        return
                    else:
                        servo_1 = servo_2 = servo_3 = servo_4 = servo_5 = -1

                task_data = [{"arm":int(arm),"s1": int(servo_1), "s2": int(servo_2), "s3": int(servo_3), "s4": int(servo_4), "s5": int(servo_5)}]

                if wait_time != "Enter wait time":
                    if servo_1 != -1 and servo_2 != -1 and servo_3 != -1 and servo_4 != -1 and servo_5 != -1:
                        messagebox.showerror("Error","angles have to be empty to enter wait command",parent=data_entry_window)
                        return
                    else:
                        wait_time_append.append({"arm":int(arm),"wait": int(wait_time)})

                for task in tasks:
                    if task["task name"] == task_name:
                        if servo_1 == -1 and servo_2 == -1 and servo_3 == -1 and servo_4 == -1 and servo_5 == -1 == -1:
                            task["task data"].extend(wait_time_append)
                            wait_time_append.clear()
                            break
                        else:
                            task["task data"].extend(task_data)
                            break
                else:
                    task = {"task name": task_name, "task data": task_data}
                    tasks.append(task)

                update_list_view(list_view,tasks)

    def update_list_view(list_view, tasks):
        # Clear existing items in the list view
        list_view.delete(0, tk.END)

        # Loop over tasks and their steps, and add formatted strings to the list view
        for task in tasks:
            task_name = task["task name"]
            task_data = task["task data"]

            # Add task name as a heading
            list_view.insert(tk.END, f"Task: {task_name}")

            # Loop over task steps and add formatted strings to the list view
            for step in task_data:
                if "wait" in step:
                    list_view.insert(tk.END, f"Wait arm{step['arm']} for {step['wait']} seconds")
                elif "end" in step:
                    list_view.insert(tk.END, "End of task")
                else:
                    arm = step["arm"]
                    s1 = step["s1"]
                    s2 = step["s2"]
                    s3 = step["s3"]
                    s4 = step["s4"]
                    s5 = step["s5"]
                    list_view.insert(tk.END, f"Move arm{arm} to s1={s1} s2={s2} s3={s3} s4={s4} s5={s5}")

            # Add an empty line after each task
            list_view.insert(tk.END, "")

    def clear_task():
        response = messagebox.askquestion("Confirmation","Are you sure you want to clear all data?",icon="warning",parent=data_entry_window)

        if response == "yes":
            tasks.clear()
            update_list_view(list_view,tasks)
            task_name_entry.config(state=tk.NORMAL)
            task_name_entry.delete(0,tk.END)
            servo_1_entry.delete(0,tk.END)
            servo_2_entry.delete(0,tk.END)
            servo_3_entry.delete(0,tk.END)
            servo_4_entry.delete(0,tk.END)
            servo_5_entry.delete(0,tk.END)
            wait_text.delete(0,tk.END)

            on_focusout(None,task_name_entry,"Enter Task name")
            on_focusout(None,servo_1_entry,"Enter servo 1 angle")
            on_focusout(None,servo_2_entry,"Enter servo 2 angle")
            on_focusout(None,servo_3_entry,"Enter servo 3 angle")
            on_focusout(None,servo_4_entry,"Enter servo 4 angle")
            on_focusout(None,servo_5_entry,"Enter servo 5 angle")
            on_focusout(None,wait_text,"Enter wait time")
            check1_var.set(False)
            check2_var.set(False)
        
        if response == "no":
            return
        
    def clear_task_force():
        tasks.clear()
        update_list_view(list_view,tasks)
        task_name_entry.config(state=tk.NORMAL)
        task_name_entry.delete(0,tk.END)
        servo_1_entry.delete(0,tk.END)
        servo_2_entry.delete(0,tk.END)
        servo_3_entry.delete(0,tk.END)
        servo_4_entry.delete(0,tk.END)
        servo_5_entry.delete(0,tk.END)
        wait_text.delete(0,tk.END)
        on_focusout(None,task_name_entry,"Enter Task name")
        on_focusout(None,servo_1_entry,"Enter servo 1 angle")
        on_focusout(None,servo_2_entry,"Enter servo 2 angle")
        on_focusout(None,servo_3_entry,"Enter servo 3 angle")
        on_focusout(None,servo_4_entry,"Enter servo 4 angle")
        on_focusout(None,servo_5_entry,"Enter servo 5 angle")
        on_focusout(None,wait_text,"Enter wait time")
        check1_var.set(False)
        check2_var.set(False)
        
    def save_task():
        task_name = task_name_entry.get()
        if os.path.isfile(directory + task_name + ".json"):
            messagebox.showerror("Error","A task with the same name exists already!",parent=data_entry_window)

        else:
            if len(tasks) == 0:
                messagebox.showerror("Error","Please enter a task",parent=data_entry_window)
                return
            else:
                #add {"end":True} to the end of tasks
                tasks[-1]["task data"].append({"end":True})
                with open(f"{directory}{task_name}"+".json", "w") as f:
                    json.dump(tasks, f, indent=4)
                messagebox.showinfo("Success","Tasks saved successfully",parent=data_entry_window)
                clear_task_force()
                return
            

    #====================== Buttons ======================

    button_add = tk.Button(data_label_master,text="Add",width=10,command=add_task)
    button_clear = tk.Button(data_label_master,text="Clear",width=10,command=clear_task)
    button_save = tk.Button(data_label_master,text="Save",width=10,command=save_task)
    list_view_frame = tk.LabelFrame(data_label_master,text="Entered Tasks",font=("Helvetica",12))
    list_view = tk.Listbox(list_view_frame, justify="center", font=("Helvetica", 12))

    #====================== Buttons Formatting ======================

    button_add.grid(row=11,column=0,padx=20,pady=20)
    button_clear.grid(row=11,column=1,padx=20,pady=20)
    button_save.grid(row=11,column=2,padx=20,pady=20)
    list_view_frame.grid(row=0,column=4,rowspan=12,sticky="NS")
    list_view.grid(row=0,column=1,ipady=130,ipadx=40)

    #====================== Tkinter End Statements ======================
    sv_ttk.set_theme("dark")
    data_entry_window.mainloop()

