import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.configure(bg="black")

        self.root.state("zoomed")

        self.tasks = self.load_tasks()  # Load tasks from file on start

        # Frame for the Task list and Notes section (top portion of window)
        top_frame = tk.Frame(root, bg="black")
        top_frame.pack(side=tk.TOP, fill=tk.Y, padx=20, pady=20)

        # Task treeview with columns for Task Name, Status, Due Date, and Priority
        self.tree = ttk.Treeview(top_frame, columns=("Task", "Status", "Due Date", "Priority"), show="headings", height=25)

        self.tree.heading("Task", text="TASK NAME")
        self.tree.heading("Status", text="STATUS")
        self.tree.heading("Due Date", text="DUE DATE")
        self.tree.heading("Priority", text="PRIORITY")

        # Apply bold and uppercase font to all column titles
        self.tree.tag_configure('bold', font=('Helvetica', 45, 'bold'))  # Set bold font
        for col in ["Task", "Status", "Due Date", "Priority"]:
            self.tree.heading(col, anchor=tk.CENTER)
            self.tree.tag_configure(col, font=('Helvetica', 45, 'bold'))

        # Center text in the columns
        self.tree.column("Task", anchor=tk.CENTER)
        self.tree.column("Status", anchor=tk.CENTER)
        self.tree.column("Due Date", anchor=tk.CENTER)
        self.tree.column("Priority", anchor=tk.CENTER)

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        # Frame for the Notes textbox (next to task list, top-right)
        self.notes_frame = tk.Frame(top_frame)
        self.notes_frame.grid(row=0, column=1, padx=20, pady=20)

        # Label for displaying date and time (moved to center above task list)
        self.time_label = tk.Label(root, font=("Helvetica", 18), anchor="center", bg = "grey")
        self.time_label.pack(pady=10)

        # Frame for buttons at the bottom center
        button_frame = tk.Frame(root, bg="black")
        button_frame.pack(side=tk.BOTTOM, anchor="center", pady=20)

        # Add Task button
        self.add_button = tk.Button(button_frame, text="Add Task", width=20, height=3, command=self.open_add_task_window, bg="lightgreen")
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Delete Task button
        self.delete_button = tk.Button(button_frame, text="Delete Task", width=20, height=3, command=self.delete_task, bg="lightgreen")
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Frame for task count status table at the bottom right
        self.status_table_frame = tk.Frame(root, bg="black")
        self.status_table_frame.pack(side=tk.BOTTOM, anchor="ne", padx=20, pady=20)

        # Status count table (columns: Status, Count)
        self.status_table = ttk.Treeview(self.status_table_frame, columns=("Status", "Count"), show="headings", height=6)
        self.status_table.heading("Status", text="STATUS")
        self.status_table.heading("Count", text="COUNT")
        self.status_table.column("Status", anchor=tk.CENTER)
        self.status_table.column("Count", anchor=tk.CENTER)

        self.status_table.grid(row=0, column=0, padx=10, pady=10)

        # Bind tree events
        self.tree.bind("<ButtonRelease-1>", self.open_notes_box)  # Click event on task
        self.tree.bind("<Double-1>", self.open_edit_task_window)  # Double-click event on task

        self.update_task_list()
        self.update_status_count()  # Initial status count update

        # Update time every second
        self.update_time()

        # Close event to save tasks before closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_time(self):
        """Update the time label to show the current date and time."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time, bg="black", fg="white")
        self.root.after(1000, self.update_time)  # Update every second

    def open_add_task_window(self):
        """Open a window to add a new task."""
        add_window = tk.Toplevel(self.root, bg="black")
        add_window.title("Add New Task")
        add_window.geometry("600x500")

        task_name_label = tk.Label(add_window, text="Task Name:")
        task_name_label.pack(pady=5)

        task_name_entry = tk.Entry(add_window, width=40)
        task_name_entry.pack(pady=5)

        priority_label = tk.Label(add_window, text="Priority (1, 2, 3):")
        priority_label.pack(pady=5)

        priority_combobox = ttk.Combobox(add_window, values=["1", "2", "3"], state="readonly")
        priority_combobox.pack(pady=5)
        priority_combobox.set("1")  # Default value

        status_label = tk.Label(add_window, text="Status:")
        status_label.pack(pady=5)

        status_combobox = ttk.Combobox(add_window, values=["New", "Open", "In Progress", "Awaiting Action", "Awaiting Parts", "Completed"], state="readonly")
        status_combobox.pack(pady=5)
        status_combobox.set("New")  # Default value

        due_date_label = tk.Label(add_window, text="Due Date (YYYY-MM-DD):")
        due_date_label.pack(pady=5)

        due_date_entry = tk.Entry(add_window, width=40)
        due_date_entry.pack(pady=5)

        def save_task(event=None):
            task_name = task_name_entry.get()
            priority = priority_combobox.get()
            status = status_combobox.get()
            due_date = due_date_entry.get()

            if task_name:
                self.tasks.append({'task': task_name, 'status': status, 'due_date': due_date, 'priority': priority, 'notes': {}})
                self.update_task_list()
                self.update_status_count()  # Update status counts
                add_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter a task name.")

        save_button = tk.Button(add_window, text="Save Task", command=save_task, bg="lightgreen")
        save_button.pack(pady=10)

        # Bind "Enter" key to save task when pressed
        add_window.bind("<Return>", save_task)

    def open_edit_task_window(self, event):
        """Open a window to edit an existing task."""
        selected_item = self.tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            task_name = self.tree.item(selected_item, "values")[0]
            task = next((task for task in self.tasks if task['task'] == task_name), None)

            if task:
                edit_window = tk.Toplevel(self.root, bg="black")
                edit_window.title("Edit Task")
                edit_window.geometry("600x500")

                task_name_label = tk.Label(edit_window, text="Task Name:")
                task_name_label.pack(pady=5)

                task_name_entry = tk.Entry(edit_window, width=40)
                task_name_entry.insert(0, task['task'])
                task_name_entry.pack(pady=5)

                priority_label = tk.Label(edit_window, text="Priority (1, 2, 3):")
                priority_label.pack(pady=5)

                priority_combobox = ttk.Combobox(edit_window, values=["1", "2", "3"], state="readonly")
                priority_combobox.set(task['priority'])
                priority_combobox.pack(pady=5)

                status_label = tk.Label(edit_window, text="Status:")
                status_label.pack(pady=5)

                status_combobox = ttk.Combobox(edit_window, values=["New", "Open", "In Progress", "Awaiting Action", "Awaiting Parts", "Completed"], state="readonly")
                status_combobox.set(task['status'])
                status_combobox.pack(pady=5)

                due_date_label = tk.Label(edit_window, text="Due Date (YYYY-MM-DD):")
                due_date_label.pack(pady=5)

                due_date_entry = tk.Entry(edit_window, width=40)
                due_date_entry.insert(0, task['due_date'])
                due_date_entry.pack(pady=5)

                def save_edited_task():
                    task['task'] = task_name_entry.get()
                    task['priority'] = priority_combobox.get()
                    task['status'] = status_combobox.get()
                    task['due_date'] = due_date_entry.get()
                    self.update_task_list()
                    self.update_status_count()  # Update status counts
                    edit_window.destroy()

                save_button = tk.Button(edit_window, text="Save Changes", command=save_edited_task, bg="lightgreen")
                save_button.pack(pady=10)

    def open_notes_box(self, event):
        """Open the notes text box when a task is clicked."""
        selected_item = self.tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            task_name = self.tree.item(selected_item, "values")[0]
            task = next((task for task in self.tasks if task['task'] == task_name), None)

            # Clear any previous notes
            for widget in self.notes_frame.winfo_children():
                widget.destroy()

            # Display previous notes if they exist
            if task['notes']:
                notes_label = tk.Label(self.notes_frame, text="Previous Notes:", font=("Helvetica", 18, "bold"))
                notes_label.pack(pady=5)

                self.note_labels = []
                for timestamp, note_content in task['notes'].items():
                    note_label = tk.Label(self.notes_frame, text=f"{timestamp}: {note_content}", font=("Helvetica", 10), cursor="hand2")
                    note_label.bind("<Button-1>", lambda e, ts=timestamp: self.edit_note(e, ts, task))  # Bind click event for editing the note
                    note_label.pack(pady=5)
                    self.note_labels.append((timestamp, note_label, note_content))

            # Button to add a new note
            add_note_button = tk.Button(self.notes_frame, text="Add New Note", command=lambda: self.add_new_note(task), bg="lightgreen")
            add_note_button.pack(pady=5)

    def add_new_note(self, task):
        """Open a text box for adding a new note."""
        note_title = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        note_label = tk.Label(self.notes_frame, text=f"New Note: {note_title}", font=("Helvetica", 18, "bold"))
        note_label.pack(pady=5)

        note_text = tk.Text(self.notes_frame, height=5, width=40)
        note_text.pack(pady=5)

        def save_note():
            note_content = note_text.get("1.0", tk.END).strip()  # Get the note content
            if note_content:
                task['notes'][note_title] = note_content
                self.update_task_list()
                self.update_status_count()  # Update status counts
                note_text.delete("1.0", tk.END)  # Clear text box after saving
            else:
                messagebox.showwarning("Input Error", "Please enter a note.")

        save_button = tk.Button(self.notes_frame, text="Save Note", command=save_note, bg="lightgreen")
        save_button.pack(pady=5)

    def edit_note(self, event, timestamp, task):
        """Edit the clicked note."""
        selected_note_label = event.widget
        old_content = task['notes'][timestamp]

        # Replace the note label with a Text widget for editing
        selected_note_label.destroy()

        edit_note_text = tk.Text(self.notes_frame, height=5, width=40, font=("Ariel", 20))
        edit_note_text.insert(tk.END, old_content)  # Pre-fill with the current note content
        edit_note_text.pack(pady=5)

        def save_edited_note():
            new_content = edit_note_text.get("1.0", tk.END).strip()
            if new_content:
                task['notes'][timestamp] = new_content  # Update the note content
                self.update_task_list()
                self.update_status_count()  # Update status counts
            else:
                messagebox.showwarning("Input Error", "Please enter a note.")

        save_button = tk.Button(self.notes_frame, text="Save Edited Note", command=save_edited_note, bg="lightgreen")
        save_button.pack(pady=5)

    def update_task_list(self):
        """Update the task list in the treeview."""
        # Clear existing tasks in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add updated tasks to the treeview
        for task in self.tasks:
            # Assign color to the priority
            if task["priority"] == "1":
                priority_color = "red"
            elif task["priority"] == "2":
                priority_color = "orange"
            else:
                priority_color = "green"

            self.tree.insert("", "end", values=(task["task"], task["status"], task["due_date"], task["priority"]), tags=(priority_color,))

        # Apply color coding to priority
        self.tree.tag_configure("red", foreground="red")
        self.tree.tag_configure("orange", foreground="orange")
        self.tree.tag_configure("green", foreground="green")

    def delete_task(self):
        """Delete the selected task."""
        selected_item = self.tree.selection()
        if selected_item:
            task_name = self.tree.item(selected_item, "values")[0]
            self.tasks = [task for task in self.tasks if task['task'] != task_name]
            self.update_task_list()
            self.update_status_count()  # Update status counts

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                return json.load(f)
        else:
            return []

    def update_status_count(self):
        """Update the status count table at the bottom-right."""
        # Count tasks for each status
        status_counts = {"New": 0, "Open": 0, "In Progress": 0, "Awaiting Action": 0, "Awaiting Parts": 0, "Completed": 0}
        for task in self.tasks:
            status_counts[task['status']] += 1

        # Clear existing status count entries in the table
        for row in self.status_table.get_children():
            self.status_table.delete(row)

        # Insert new status counts into the table
        for status, count in status_counts.items():
            self.status_table.insert("", "end", values=(status, count))

    def on_close(self):
        """Save tasks before closing the app."""
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
