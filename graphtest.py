import tkinter as tk
import datetime
from PIL import ImageTk, Image

import sv_ttk

class ProgressBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        # Load the images for the buttons
        self.play_image = ImageTk.PhotoImage(Image.open("assets/play.png").resize((30,30)))
        self.pause_image = ImageTk.PhotoImage(Image.open("assets/pause.png").resize((30,30)))
        self.stop_image = ImageTk.PhotoImage(Image.open("assets/stop.png").resize((30,30)))

        # Set the initial progress to 0
        self.progress = 0
        
        # Create the progress bar
        self.progress_bar = tk.Canvas(self, width=200, height=20)
        self.progress_bar.create_rectangle(0, 0, 200, 20, fill="grey")
        self.progress_bar.create_rectangle(0, 0, 0, 20, fill="green", tags="progress")
        self.progress_bar.pack()
        
        # Create the buttons
        self.play_button = tk.Button(self, image=self.play_image, command=self.start)
        self.pause_button = tk.Button(self, image=self.pause_image, state="disabled", command=self.pause)
        self.stop_button = tk.Button(self, image=self.stop_image, state="disabled", command=self.stop)
        
        self.play_button.pack(side=tk.LEFT, padx=20, pady=10)
        self.pause_button.pack(side=tk.LEFT, padx=20, pady=10)
        self.stop_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Set the current state to "stopped"
        self.state = "stopped"
        
        # Set the time of the last update to the current time
        self.last_update = datetime.datetime.now()
        
        # Start the main loop
        self.update_progress()
    
    def start(self):
        if self.state == "stopped":
            # Set the state to "playing"
            self.state = "playing"
    
            # Enable the pause and stop buttons
            self.pause_button.config(state="normal")
            self.stop_button.config(state="normal")
    
            # Disable the play button
            self.play_button.config(state="disabled")
    
            # Set the time of the last update to the current time
            self.last_update = datetime.datetime.now()
    
        elif self.state == "paused":
            # Set the state to "playing"
            self.state = "playing"
    
            # Enable the pause and stop buttons
            self.pause_button.config(state="normal")
            self.stop_button.config(state="normal")
    
            # Disable the play button
            self.play_button.config(state="disabled")
    
            # Calculate the time since the last update and add it to the last update time
            now = datetime.datetime.now()
            time_delta = (now - self.last_update).total_seconds()
            self.last_update += datetime.timedelta(seconds=time_delta)
            
    def pause(self):
        if self.state == "playing":
            # Set the state to "paused"
            self.state = "paused"
            
            # Disable the pause button
            self.pause_button.config(state="disabled")
            
            # Enable the play button
            self.play_button.config(state="normal")
            
            # Set the time of the last update to None
            self.last_update = None
            
        elif self.state == "paused":
            # Set the state to "playing"
            self.state = "playing"
            
            # Enable the pause and stop buttons
            self.pause_button.config(state="normal")
            self.stop_button.config(state="normal")
            
            # Disable the play button
            self.play_button.config(state="disabled")
            
            # Set the time of the last update to the current time
            self.last_update = datetime.datetime.now()
    
    def stop(self):
        if self.state != "stopped":
            # Set the state to "stopped"
            self.state = "stopped"
            
            # Disable the pause and stop buttons
            self.pause_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            
            # Enable the play button
            self.play_button.config(state="normal")
            
            # Reset the progress to 0
            self.progress = 0
            self.progress_bar.coords("progress", (0, 0, 0, 20))
        
    def update_progress(self):
        # Calculate the time since the last update
        now = datetime.datetime.now()
        time_delta = (now - self.last_update).total_seconds() if self.last_update is not None else 0

        if self.state == "playing" or self.state == "paused":
            # Update the progress based on the time delta
            if self.state == "playing":
                self.progress += time_delta * 10
            self.progress = min(self.progress, 100)

            # Update the progress bar
            self.progress_bar.coords("progress", (0, 0, self.progress * 2, 20))

            # Remove the previous progress text
            self.progress_bar.delete("text")

            # Add the new progress text
            progress_text = f"{int(self.progress)}%"
            self.progress_bar.create_text(100, 10, text=progress_text, tags="text")

            # Check if the progress has reached 100%
            if self.progress >= 100:
                self.stop()

        # Set the time of the last update to the current time
        self.last_update = now

        # Call this function again after a short delay
        self.after(100, self.update_progress)

root = tk.Tk()
progress_bar = ProgressBar(root)
progress_bar.pack()

sv_ttk.set_theme("dark")

root.mainloop()

