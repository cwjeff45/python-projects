import socket
import threading
import tkinter as tk
from tkinter import messagebox

def scan_port(target, port, results):
    """Checks if a port is open on the target IP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((target, port))  # Returns 0 if open
        if result == 0:
            results.append(port)

def start_scan():
    """Starts scanning and updates the GUI."""
    target_ip = ip_entry.get()
    if not target_ip:
        messagebox.showerror("Error", "Please enter a valid IP address!")
        return

    results = []
    ports = range(1, 1025)  # Common ports

    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(target_ip, port, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Display results in a pop-up
    if results:
        messagebox.showinfo("Scan Complete", f"Open Ports on {target_ip}:\n" + ", ".join(map(str, results)))
    else:
        messagebox.showinfo("Scan Complete", "No open ports found.")

# GUI setup
root = tk.Tk()
root.title("Port Scanner")
root.geometry("300x150")

tk.Label(root, text="Enter IP Address:").pack(pady=5)
ip_entry = tk.Entry(root, width=25)
ip_entry.pack(pady=5)

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=10)

root.mainloop()
