import threading
import time
import random
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

# ------------------------
# Setup: Main Window
# ------------------------
root = tk.Tk()
root.title("MULTITHREADING MODELS SIMULATOR")
root.geometry("700x500")  # Further reduced window size for 14-inch screen
root.configure(bg="#f0f0f0")  # Soft gray background

# Style Configuration for UI Enhancements
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f0f0f0", foreground="black", font=("Segoe UI", 9))  # Smaller font size
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#1f77b4")  # Reduced header font size
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, relief="flat", width=15)  # Slightly smaller button
style.configure("TEntry", padding=5, font=("Consolas", 10))  # Reduced entry font size

# ------------------------
# Header
# ------------------------
header = ttk.Label(root, text="MULTITHREADING MODELS SIMULATOR", style="Header.TLabel")
header.pack(pady=15)

# ------------------------
# Input Frame
# ------------------------
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Enter Number of Threads:").grid(row=0, column=0, padx=5)
thread_count_entry = ttk.Entry(input_frame, width=6)
thread_count_entry.grid(row=0, column=1, padx=5)

# ------------------------
# Canvas for Thread States (Circles)
# ------------------------
canvas = tk.Canvas(root, width=650, height=150, bg="#e6f7ff", highlightthickness=2, highlightbackground="#1f77b4")
canvas.pack(pady=10)

thread_circles = {}

def draw_circle(x_pos, label, color):
    radius = 15
    y_pos = 75
    circle = canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill=color, outline="")
    text = canvas.create_text(x_pos, y_pos, text=label, fill="white", font=("Segoe UI", 8, "bold"))  # Smaller font for labels
    thread_circles[label] = (circle, text)
    root.update_idletasks()

def update_circle_color(label, color):
    if label in thread_circles:
        circle, _ = thread_circles[label]
        canvas.itemconfig(circle, fill=color)
        root.update_idletasks()

# ------------------------
# Log Output Frame
# ------------------------
log_frame = ttk.Frame(root)
log_frame.pack(pady=10)

log_text = tk.Text(log_frame, height=8, width=80, bg="#f9f9f9", fg="black", font=("Consolas", 9), wrap="word", relief="sunken", bd=1)
log_text.pack()

def log_activity(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    root.update_idletasks()

def save_log():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, "w") as f:
            f.write(log_text.get("1.0", tk.END))
        log_activity("Log saved to file.")

ttk.Button(log_frame, text="Save Log", command=save_log).pack(pady=5)

# ------------------------
# Multithreading Logic
# ------------------------
semaphore = threading.Semaphore(2)
resource_lock = threading.Lock()

def get_thread_count():
    try:
        return max(1, int(thread_count_entry.get()))
    except ValueError:
        return 3

def clear_canvas():
    canvas.delete("all")
    thread_circles.clear()

# Many-to-One Model
def many_to_one_thread(name, x_pos):
    draw_circle(x_pos, name, "orange")
    log_activity(f"{name} is READY to run")
    time.sleep(random.uniform(0.5, 1))

    with resource_lock:
        update_circle_color(name, "green")
        log_activity(f"{name} is RUNNING on a single kernel thread")
        time.sleep(random.uniform(1, 2))

    update_circle_color(name, "grey")
    log_activity(f"{name} has TERMINATED")

def many_to_one():
    def run():
        log_activity("Running Many-to-One Model...\n")
        clear_canvas()
        threads = []
        count = get_thread_count()
        spacing = 650 // (count + 1)

        for i in range(count):
            x = (i + 1) * spacing
            t = threading.Thread(target=many_to_one_thread, args=(f"T{i}", x))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        log_activity("Many-to-One Model Completed.\n")

    threading.Thread(target=run).start()

# ------------------------
# One-to-Many Model
# ------------------------
def one_to_many_thread(name, x_pos):
    draw_circle(x_pos, name, "blue")
    log_activity(f"{name} is READY to run")
    time.sleep(random.uniform(0.5, 1))

    update_circle_color(name, "green")
    log_activity(f"{name} is RUNNING on its own kernel thread")
    time.sleep(random.uniform(1, 2))

    update_circle_color(name, "grey")
    log_activity(f"{name} has TERMINATED")

def one_to_many():
    def run():
        log_activity("Running One-to-Many Model...\n")
        clear_canvas()
        threads = []
        count = get_thread_count()
        spacing = 650 // (count + 1)

        for i in range(count):
            x = (i + 1) * spacing
            t = threading.Thread(target=one_to_many_thread, args=(f"K{i}", x))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        log_activity("One-to-Many Model Completed.\n")

    threading.Thread(target=run).start()

# ------------------------
# Many-to-Many Model
# ------------------------
def many_to_many_thread(name, x_pos):
    draw_circle(x_pos, name, "green")
    log_activity(f"{name} is READY to run")
    time.sleep(random.uniform(0.5, 1))

    acquired = semaphore.acquire(timeout=5)
    if acquired:
        update_circle_color(name, "green")
        log_activity(f"{name} is RUNNING using shared kernel thread")
        time.sleep(random.uniform(1, 2))
        semaphore.release()

    update_circle_color(name, "grey")
    log_activity(f"{name} has TERMINATED")

def many_to_many():
    def run():
        log_activity("Running Many-to-Many Model...\n")
        clear_canvas()
        threads = []
        count = get_thread_count()
        spacing = 650 // (count + 1)

        for i in range(count):
            x = (i + 1) * spacing
            t = threading.Thread(target=many_to_many_thread, args=(f"M{i}", x))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        log_activity("Many-to-Many Model Completed.\n")

    threading.Thread(target=run).start()

# ------------------------
# Monitor Synchronization Model
# ------------------------
monitor_condition = threading.Condition()
monitor_shared_resource = 0

def monitor_thread(name, x_pos):
    draw_circle(x_pos, name, "purple")
    log_activity(f"{name} is READY to access shared resource")
    time.sleep(random.uniform(0.5, 1))

    with monitor_condition:
        if monitor_shared_resource == 0:
            update_circle_color(name, "red")
            log_activity(f"{name} is WAITING for shared resource")
            monitor_condition.wait()

        update_circle_color(name, "green")
        log_activity(f"{name} is RUNNING after getting access")
        time.sleep(random.uniform(1, 2))

    update_circle_color(name, "grey")
    log_activity(f"{name} has TERMINATED")

def run_monitor_synchronization():
    def run():
        global monitor_shared_resource
        log_activity("Running Monitor Synchronization...\n")
        clear_canvas()

        monitor_shared_resource = 0
        threads = []
        count = get_thread_count()
        spacing = 650 // (count + 1)

        for i in range(count):
            x = (i + 1) * spacing
            t = threading.Thread(target=monitor_thread, args=(f"Mo{i}", x))
            threads.append(t)
            t.start()

        time.sleep(2)

        with monitor_condition:
            monitor_shared_resource = 1
            monitor_condition.notify_all()
            log_activity("Shared resource AVAILABLE, all waiting threads NOTIFIED")

        for t in threads:
            t.join()

        log_activity("Monitor Synchronization Completed.\n")

    threading.Thread(target=run).start()

# ------------------------
# Button Panel
# ------------------------
button_frame = ttk.Frame(root)
button_frame.pack(pady=15)

# Keep the original button design but with reduced size and spacing
ttk.Button(button_frame, text="Run Many-to-One", command=many_to_one).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(button_frame, text="Run One-to-Many", command=one_to_many).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(button_frame, text="Run Many-to-Many", command=many_to_many).grid(row=0, column=2, padx=10, pady=5)
ttk.Button(button_frame, text="Run Monitor Sync", command=run_monitor_synchronization).grid(row=0, column=3, padx=10, pady=5)

# ------------------------
# Start GUI
# ------------------------
root.mainloop()
