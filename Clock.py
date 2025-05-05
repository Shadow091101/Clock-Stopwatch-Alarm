import tkinter as tk
from tkinter import ttk
from tkinter import *
from plyer import notification
import pygame
import threading
import time
import os
import sys
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox 

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS  # This is set by PyInstaller at runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Root Window
root = tk.Tk()
root.title("Clock | Stopwatch | Timer")
root.geometry("600x500")
root.iconbitmap(resource_path("icon.ico"))
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# ----- Clock Tab -----
month=""
day_of_week=0
date_of_month=0

def date():
    global month,day_of_week,date_of_month
    day_of_week=time.strftime("%a")
    date_of_month=time.strftime("%d")
    month_of_year=str(time.strftime("%m")).strip("0")
    if(month_of_year=="1"):
        month="Jan"
    elif(month_of_year=="2"):
        month="Feb"
    elif(month_of_year=="3"):
        month="Mar"
    elif(month_of_year=="4"):
        month="Apr"
    elif(month_of_year=="5"):
        month="May"
    elif(month_of_year=="6"):
        month="Jun"
    elif(month_of_year=="7"):
        month="Jul"
    elif(month_of_year=="8"):
        month="Aug"
    elif(month_of_year=="9"):
        month="Sep"
    elif(month_of_year=="10"):
        month="Oct"
    elif(month_of_year=="11"):
        month="Nov"
    elif(month_of_year=="12"):
        month="Dec"
    date_label.config(text=f"Indian Standard Time | {day_of_week}, {date_of_month} {month}")
clock_tab = Frame(notebook)
notebook.add(clock_tab, text='Clock')

def update_clock():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

clock_label = Label(clock_tab, text="", font=("Helvetica", 48), fg='green', bg="black")
clock_label.pack(pady=50)
date_label_frame=LabelFrame(clock_tab)
date_label_frame.pack(pady=20)
date_label=Label(date_label_frame,text="",font=("Helvetica",20))
date_label.pack(pady=20)  


update_clock()

# ----- Stopwatch Tab -----
stopwatch_tab = Frame(notebook)
notebook.add(stopwatch_tab, text='Stopwatch')

millisec = hour = minute = sec = 0
running = False
lap_count = 1

def update_stopwatch():
    global millisec, hour, minute, sec, running
    if running:
        millisec += 1
        if millisec == 100:
            millisec = 0
            sec += 1
        if sec == 60:
            sec = 0
            minute += 1
        if minute == 60:
            minute = 0
            hour += 1
        stopwatch_label.config(text=f"{hour:02}:{minute:02}:{sec:02}:{millisec:02}")
        stopwatch_label.after(3, update_stopwatch)

def start_stopwatch():
    global running
    if not running:
        running = True
        update_stopwatch()

def stop_stopwatch():
    global running
    running = False

def reset_stopwatch():
    global millisec, hour, minute, sec, lap_count, running
    running = False
    millisec = hour = minute = sec = 0
    lap_count = 1
    stopwatch_label.config(text="00:00:00:00")
    for widget in lap_frame.winfo_children():
        widget.destroy()

def record_lap():
    global lap_count
    lap = Label(lap_frame, text=f"Lap {lap_count}: {hour:02}:{minute:02}:{sec:02}:{millisec:02}", border=1, relief="solid")
    lap.pack(fill="x", pady=1, padx=20)
    lap_count += 1

def export_laps_to_file(filetype='txt'):
    laps = []
    for widget in lap_frame.winfo_children():
        if isinstance(widget, Label):
            laps.append(widget.cget("text"))

    if not laps:
        return

    filename = "laps." + filetype
    
    if filetype=="txt":   
        file_path = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Lap Times"
        )
    else:
        file_path = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Lap Times"
        )

    if not file_path:
        return  # User cancelled
        
    try:
        with open(filename, "w", encoding="utf-8") as file:
            if filetype == "csv":
                file.write("Lap Number,Time\n")
                for lap in laps:
                    # Expected format: "Lap 1: 00:00:12:34"
                    if ':' in lap:
                        lap_number, time = lap.split(": ", 1)
                        file.write(f"{lap_number},{time}\n")
            else:
                for lap in laps:
                    file.write(lap + "\n")
        messagebox.showinfo("Success","File Saved Successfully") 
    except Exception as e:
        messagebox.showerror("Error", e) 


stopwatch_label = Label(stopwatch_tab, text="00:00:00:00", font=("Helvetica", 48), fg='green', bg='black')
stopwatch_label.pack(pady=20)

stopwatch_controls = Frame(stopwatch_tab)
stopwatch_controls.pack(pady=5)

Button(stopwatch_controls, text="Start", command=start_stopwatch).pack(side=LEFT, padx=5)
Button(stopwatch_controls, text="Stop", command=stop_stopwatch).pack(side=LEFT, padx=5)
Button(stopwatch_controls, text="Reset", command=reset_stopwatch).pack(side=LEFT, padx=5)
Button(stopwatch_controls, text="Lap", command=record_lap).pack(side=LEFT, padx=5)
Button(stopwatch_controls, text="Export Laps as .txt", command=lambda: export_laps_to_file("txt")).pack(side=LEFT, padx=5,pady=5)
Button(stopwatch_controls, text="Export Laps as .csv", command=lambda: export_laps_to_file("csv")).pack(side=LEFT, padx=5)



lap_container = LabelFrame(stopwatch_tab, text="Laps")
lap_container.pack(fill="both", expand=True, padx=10, pady=10)

canvas = Canvas(lap_container)
scrollbar = Scrollbar(lap_container, orient="vertical", command=canvas.yview)
lap_frame = Frame(canvas)

lap_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=lap_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ----- Timer Tab -----
timer_tab = Frame(notebook)
notebook.add(timer_tab, text='Timer')

hour = min = sec = 0
timer_running = False

def update_timer():
    global hour, min, sec, timer_running
    if timer_running:
        if hour == 0 and min == 0 and sec == 0:
            timer_running = False
            send_notification()
            start_button.config(state=NORMAL)
            stop_button.config(state=DISABLED)
            reset_button.config(state=DISABLED)
            hourB1.config(state=NORMAL)
            hourB1.config(state=NORMAL)
            minB1.config(state=NORMAL)
            minB2.config(state=NORMAL)
            secB1.config(state=NORMAL)
            secB2.config(state=NORMAL)
            return
        if sec == 0:
            sec = 59
            if min == 0:
                min = 59
                if hour > 0:
                    hour -= 1
            else:
                min -= 1
        else:
            sec -= 1
        update_timer_labels()
        timer_tab.after(1000, update_timer)

def update_timer_labels():
    hour_label.config(text=f"{hour:02}")
    minute_label.config(text=f"{min:02}")
    second_label.config(text=f"{sec:02}")

def send_notification():
    try:
        notification.notify(
            title="Timer",
            app_name="Clock",
            message="Time's up",
            app_icon=resource_path("icon.ico"),
            ticker="Time is up Buddy",
            timeout=10
        )
        threading.Thread(target=play_sound_for_notification, args=(10,), daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error",e) 

def play_sound_for_notification(duration=10):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(resource_path("timer.mp3"))
        pygame.mixer.music.play()
        time.sleep(duration)
        pygame.mixer.music.stop()
    except Exception as e:
        messagebox.showerror("Error",e) 



def start_timer():
    global timer_running
    if not timer_running:
        if hour==0 and min==0 and sec==0:
            return
        else:
            timer_running = True
            start_button.config(state=DISABLED)
            stop_button.config(state=NORMAL)
            reset_button.config(state=NORMAL)
            hourB1.config(state=DISABLED)
            hourB2.config(state=DISABLED)
            minB1.config(state=DISABLED)
            minB2.config(state=DISABLED)
            secB1.config(state=DISABLED)
            secB2.config(state=DISABLED)
            start_button.config(text="Start")
            update_timer()

def reset_timer():
    global hour, min, sec, timer_running
    timer_running = False
    hour = min = sec = 0
    start_button.config(state=NORMAL)
    stop_button.config(state=DISABLED)
    reset_button.config(state=DISABLED)
    hourB1.config(state=NORMAL)
    hourB1.config(state=NORMAL)
    minB1.config(state=NORMAL)
    minB2.config(state=NORMAL)
    secB1.config(state=NORMAL)
    secB2.config(state=NORMAL)
    update_timer_labels()
    

def stop_timer():
    global timer_running
    if timer_running:
        stop_button.config(state=DISABLED)
        start_button.config(state=NORMAL)
        start_button.config(text="Resume")
        timer_running=False 

def hour_up():    global hour; hour = (hour + 1) % 24; update_timer_labels()
def hour_down():  global hour; hour = (hour - 1) % 24; update_timer_labels()
def min_up():     global min; min = (min + 1) % 60; update_timer_labels()
def min_down():   global min; min = (min - 1) % 60; update_timer_labels()
def sec_up():     global sec; sec = (sec + 1) % 60; update_timer_labels()
def sec_down():   global sec; sec = (sec - 1) % 60; update_timer_labels()

def brush_teeth_timer():
    global hour,min,sec
    hour=0
    min=3
    sec=0
    hour_label.config(text=f"{hour:02}")
    minute_label.config(text=f"{min:02}")
    second_label.config(text=f"{sec:02}")
    
    
def reading_timer():
    global hour,min,sec
    hour=0
    min=15
    sec=0
    hour_label.config(text=f"{hour:02}")
    minute_label.config(text=f"{min:02}")
    second_label.config(text=f"{sec:02}")
    
    
def running_timer():
    global hour,min,sec
    hour=0
    min=10
    sec=0
    hour_label.config(text=f"{hour:02}")
    minute_label.config(text=f"{min:02}")
    second_label.config(text=f"{sec:02}")
    

timer_frame = Frame(timer_tab)
timer_frame.pack(pady=20)

# Buttons and Labels for timer
hourB1=Button(timer_frame, text="↑", command=hour_up)
hourB1.grid(row=0, column=0)
hour_label = Label(timer_frame, text="00", font=("Helvetica", 48))
hour_label.grid(row=1, column=0)

hourB2=Button(timer_frame, text="↓", command=hour_down)
hourB2.grid(row=2, column=0)

minB1=Button(timer_frame, text="↑", command=min_up)
minB1.grid(row=0, column=1)
minute_label = Label(timer_frame, text="00", font=("Helvetica", 48))
minute_label.grid(row=1, column=1)
minB2=Button(timer_frame, text="↓", command=min_down)
minB2.grid(row=2, column=1)

secB1=Button(timer_frame, text="↑", command=sec_up)
secB1.grid(row=0, column=2)
second_label = Label(timer_frame, text="00", font=("Helvetica", 48))
second_label.grid(row=1, column=2)
secB2=Button(timer_frame, text="↓", command=sec_down)
secB2.grid(row=2, column=2)

# Start/Reset buttons
timer_controls = Frame(timer_tab)
timer_controls.pack(pady=10)
start_button=Button(timer_controls, text="Start", command=start_timer)
start_button.pack(side=LEFT, padx=10)
stop_button=Button(timer_controls, text="Stop",state=DISABLED, command=stop_timer)
stop_button.pack(side=LEFT, padx=10)
reset_button=Button(timer_controls, text="Reset",state=DISABLED, command=reset_timer)
reset_button.pack(side=LEFT, padx=10)

#Various other timers
other_timers=Frame(timer_tab)
other_timers.pack(pady=10)
brush_teeth_btn=Button(other_timers,text="Brush Teeth = 3:00",command=brush_teeth_timer,font=("Helvetica",10))
brush_teeth_btn.pack(side=LEFT,padx=20)
running_btn=Button(other_timers,text="Running= 10:00",command=running_timer,font=("Helvetica",10))
running_btn.pack(side=LEFT,padx=20)
reading_btn=Button(other_timers,text="Reading = 15:00",command=reading_timer,font=("Helvetica",10))
reading_btn.pack(side=LEFT,padx=20)

date()

root.mainloop()
