import tkinter as tk
import sv_ttk

#REMOVE THIS WHILE USING MAIN APPLICATION
root = tk.Tk()

def create_interface(master):
    data_entry_window = tk.Toplevel(master)
    data_entry_window.geometry("500x500")
    data_entry_window.title("Data Entry")

    # Create a frame for the data entry window
    data_entry_frame = tk.Frame(data_entry_window)
    data_entry_frame.pack()

    data_label_master = tk.LabelFrame(data_entry_frame,text="Data Entry System")
    data_label_master.grid(row=0,column=0)

    coord_x = tk.Label(data_label_master,text="Enter X coordinate")
    coord_x.grid(row=0,column=0,padx=20,pady=20)
    coord_y = tk.Label(data_label_master,text="Enter Y coordinate")
    coord_y.grid(row=0,column=1,padx=20,pady=20)
    coord_z = tk.Label(data_label_master,text="Enter Z coordinate")
    coord_z.grid(row=0,column=2,padx=20,pady=20)

    def on_entry_click(event):
        if coord_x_entry.get() == "Enter X coord":
            coord_x_entry.delete(0,"end")
            coord_x_entry.insert(0,'')
            coord_x_entry.config(fg='black')
        
        if coord_y_entry.get() == "Enter Y coord":
            coord_y_entry.delete(0,"end")
            coord_y_entry.insert(0,'')
            coord_y_entry.config(fg='black')

        if coord_z_entry.get() == "Enter Z coord":
            coord_z_entry.delete(0,"end")
            coord_z_entry.insert(0,'')
            coord_z_entry.config(fg='black')
    
    def on_focusout(event):
        if coord_x_entry.get() == '':
            coord_x_entry.insert(0,'Enter X coord')
            coord_x_entry.config(fg='grey')
        
        if coord_y_entry.get() == '':
            coord_y_entry.insert(0,'Enter Y coord')
            coord_y_entry.config(fg='grey')
        
        if coord_z_entry.get() == '':
            coord_z_entry.insert(0,'Enter Z coord')
            coord_z_entry.config(fg='grey')

    coord_x_entry = tk.Entry(data_label_master,fg='grey')
    coord_x_entry.insert(0,'Enter X coord')
    coord_x_entry.bind('<FocusIn>',on_entry_click)
    coord_x_entry.bind('<FocusOut>',on_focusout)
    coord_x_entry.grid(row=1,column=0,padx=20,pady=20)
    coord_y_entry = tk.Entry(data_label_master,fg='grey')
    coord_y_entry.insert(0,'Enter Y coord')
    coord_y_entry.bind('<FocusIn>',on_entry_click)
    coord_y_entry.bind('<FocusOut>',on_focusout)
    coord_y_entry.grid(row=1,column=1,padx=20,pady=20)
    coord_z_entry = tk.Entry(data_label_master,fg='grey')
    coord_z_entry.insert(0,'Enter Z coord')
    coord_z_entry.bind('<FocusIn>',on_entry_click)
    coord_z_entry.bind('<FocusOut>',on_focusout)
    coord_z_entry.grid(row=1,column=2,padx=20,pady=20)

    

    sv_ttk.set_theme("dark")
    data_entry_window.mainloop()

create_interface(root)