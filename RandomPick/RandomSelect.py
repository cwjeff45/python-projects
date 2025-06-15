import random
import tkinter as tk
from tkinter import simpledialog, messagebox

class RandomSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Selector")
        self.root.geometry("350x250")

        self.inputs = []

        tk.Label(root, text="Random Item Selector", font=("Arial", 14)).pack(pady=10)
        
        self.add_button = tk.Button(root, text="Set Number of Inputs", command=self.set_inputs)
        self.add_button.pack(pady=5)

        self.select_button = tk.Button(root, text="Select Random Item", command=self.select_random, state=tk.DISABLED)
        self.select_button.pack(pady=5)

    def set_inputs(self):
        self.inputs.clear()
        num = simpledialog.askinteger("Input Count", "How many inputs do you want?", minvalue=1, maxvalue=50)
        if num:
            for i in range(num):
                item = simpledialog.askstring("Input", f"Enter item {i+1}:")
                if item:
                    self.inputs.append(item)

            if self.inputs:
                self.select_button.config(state=tk.NORMAL)

    def select_random(self):
        if self.inputs:
            choice = random.choice(self.inputs)
            messagebox.showinfo("Random Selection", f"Selected Item: {choice}")

root = tk.Tk()
app = RandomSelectorApp(root)
root.mainloop()
