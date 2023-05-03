import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import json

root = tk.Tk()

def create_interface(master):
    #====================== Tkinter window creation ======================

    data_entry_window = tk.Toplevel(master)
    data_entry_window.title("Task Creator")
    data_entry_window.resizable(False,False)
    data_entry_frame = tk.Frame(data_entry_window)
    data_entry_frame.grid()


    #====================== Variable Init ======================

    tasks = []
    wait_time_append = []


    #====================== Begin UI ======================

    data_label_master = tk.LabelFrame(data_entry_frame, text="")
    label_main = tk.Label(data_label_master,text="Task Creator",font=("Helvetica",18))
    separator_0 = ttk.Separator(data_label_master, orient="horizontal")
    task_name = tk.Label(data_label_master,text="Task name")
    separator_1 = ttk.Separator(data_label_master, orient="horizontal")
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
    coord_x.grid(row=4, column=0, padx=20, pady=20)
    coord_y.grid(row=4, column=1, padx=20, pady=20)
    coord_z.grid(row=4, column=2, padx=20, pady=20)
    wait_time.grid(row=7, column=0, padx=20, pady=20)


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
    coord_x_entry.grid(row=5, column=0, padx=20, pady=20)
    coord_y_entry.insert(0, "Enter Y coord")
    coord_y_entry.bind("<FocusIn>", lambda event: on_entry_click(event, coord_y_entry))
    coord_y_entry.bind("<FocusOut>", lambda event: on_focusout(event,coord_y_entry, "Enter Y coord"))
    coord_y_entry.grid(row=5, column=1, padx=20, pady=20)
    coord_z_entry.insert(0, "Enter Z coord")
    coord_z_entry.bind("<FocusIn>", lambda event: on_entry_click(event, coord_z_entry))
    coord_z_entry.bind("<FocusOut>", lambda event: on_focusout(event,coord_z_entry, "Enter Z coord"))
    coord_z_entry.grid(row=5, column=2, padx=20, pady=20)
    separator_2.grid(row=6,columnspan=4,sticky="ew",pady=(5,5),ipady=2)
    wait_text.insert(0, "Enter wait time")
    wait_text.bind("<FocusIn>", lambda event: on_entry_click(event, wait_text))
    wait_text.bind("<FocusOut>", lambda event: on_focusout(event,wait_text, "Enter wait time"))
    wait_text.grid(row=7, column=1, padx=20, pady=20)
    separator_3.grid(row=8,columnspan=4,sticky="ew",pady=(5,5),ipady=2)


    #====================== Button Functions ======================

    def add_task():
        task_name = task_name_entry.get()
        coord_x = coord_x_entry.get()
        coord_y = coord_y_entry.get()
        coord_z = coord_z_entry.get()
        wait_time = wait_text.get()


        if task_name == "" or task_name == "Enter Task name":
            messagebox.showerror("Error", "Please enter a Task name")
            return
        else:

            task_name_entry.config(state=tk.DISABLED)

            if coord_x == "" or coord_y == "" or coord_z == "" or coord_x == "Enter X coord" or coord_y == "Enter Y coord" or coord_z == "Enter Z coord":
                if wait_time == "" or wait_time == "Enter wait time":
                    messagebox.showerror("Error", "Please enter all coordinates")
                    return
                else:
                    coord_x = coord_y = coord_z = -1

            task_data = [{"x": int(coord_x), "y": int(coord_y), "z": int(coord_z)}]

            if wait_time != "Enter wait time":
                if coord_x != -1 and coord_y != -1 and coord_z != -1:
                    messagebox.showerror("Error","Coordinates have to be empty to enter wait command")
                    return
                else:
                    wait_time_append.append({"wait": int(wait_time)})

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

            print(json.dumps(task, indent=4))
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
                    list_view.insert(tk.END, f"Wait for {step['wait']} seconds")
                elif "end" in step:
                    list_view.insert(tk.END, "End of task")
                else:
                    x = step["x"]
                    y = step["y"]
                    z = step["z"]
                    list_view.insert(tk.END, f"Move to x={x}, y={y}, z={z}")

            # Add an empty line after each task
            list_view.insert(tk.END, "")

    def clear_task():
        response = messagebox.askquestion("Confirmation","Are you sure you want to clear all data?",icon="warning")

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
        
        if response == "no":
            return
            

    #====================== Buttons ======================

    button_add = tk.Button(data_label_master,text="Add",width=10,command=add_task)
    button_clear = tk.Button(data_label_master,text="Clear",width=10,command=clear_task)
    button_save = tk.Button(data_label_master,text="Save",width=10)
    list_view_frame = tk.LabelFrame(data_label_master,text="Entered Tasks",font=("Helvetica",12))
    list_view = tk.Listbox(list_view_frame, justify="center", font=("Helvetica", 12))

    #====================== Buttons Formatting ======================

    button_add.grid(row=9,column=0,padx=20,pady=20)
    button_clear.grid(row=9,column=1,padx=20,pady=20)
    button_save.grid(row=9,column=2,padx=20,pady=20)
    list_view_frame.grid(row=0,column=4,rowspan=10,sticky="NS")
    list_view.grid(row=0,column=0,ipady=100)

    #====================== Tkinter End Statements ======================
    sv_ttk.set_theme("dark")
    data_entry_window.mainloop()


create_interface(root)