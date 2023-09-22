import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import datetime
import pickle

class Task:
    def __init__(self, description, due_date):
        self.description = description
        self.due_date = due_date
        self.is_done = False

    def mark_as_done(self):
        self.is_done = True

    def __str__(self):
        return ('[X]' if self.is_done else '[ ]') + ' ' + self.description + ' (Due: ' + self.due_date.strftime('%m/%d/%Y') + ')'


class ToDoList:
    def __init__(self, root):
        self.tasks = []
        self.root = root
        self.root.geometry("400x400")
        self.text = tk.Text(root, height=5)
        self.date_entry = tk.Entry(root)
        self.listbox = tk.Listbox(root)
        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.done_button = ttk.Button(root, text="Mark as Done", command=self.mark_task_as_done)
        self.update_button = ttk.Button(root, text="Update Task", command=self.update_task)

    def add_task(self):
        task_description = self.text.get("1.0", "end-1c")
        if len(task_description.split()) > 500:
            messagebox.showinfo("Warning", "Task description should be less than 500 words.")
            return
        try:
            due_date = datetime.datetime.strptime(self.date_entry.get(), '%m/%d/%Y')
            if task_description != "":
                task = Task(task_description, due_date)
                self.tasks.append(task)
                self.listbox.insert(tk.END, str(task))
                self.text.delete("1.0", tk.END)
                self.date_entry.delete(0, tk.END)
                self.save_tasks()
            else:
                messagebox.showinfo("Warning", "Please enter a task.")
        except ValueError:
            messagebox.showinfo("Warning", "Please enter a valid date in MM/DD/YYYY format.")

    def mark_task_as_done(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            task = self.tasks[index]
            task.mark_as_done()
            self.listbox.delete(index)
            self.listbox.insert(index, str(task))
            self.save_tasks()

    def update_task(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            new_description = self.text.get("1.0", "end-1c")
            if len(new_description.split()) > 500:
                messagebox.showinfo("Warning", "Task description should be less than 500 words.")
                return
            try:
                new_due_date = datetime.datetime.strptime(self.date_entry.get(), '%m/%d/%Y')
                task = Task(new_description, new_due_date)
                self.tasks[index] = task
                self.listbox.delete(index)
                self.listbox.insert(index, str(task))
                self.text.delete("1.0", tk.END)
                self.date_entry.delete(0, tk.END)
                self.save_tasks()
            except ValueError:
                messagebox.showinfo("Warning", "Please enter a valid date in MM/DD/YYYY format.")

    def save_tasks(self):
        with open('tasks.pkl', 'wb') as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open('tasks.pkl', 'rb') as f:
                self.tasks = pickle.load(f)
            for task in self.tasks:
                self.listbox.insert(tk.END, str(task))
        except FileNotFoundError:
            pass

    def run(self):
        ttk.Label(self.root, text="Task Description:").pack()
        self.text.pack()
        ttk.Label(self.root, text="Due Date (MM/DD/YYYY):").pack()
        self.date_entry.pack()
        self.add_button.pack()
        self.done_button.pack()
        self.update_button.pack()
        ttk.Separator(self.root).pack(fill=tk.X)  # Add a separator for better visual organization.
        ttk.Label(self.root, text="Tasks:").pack()
        # Add a scrollbar to the list box.
        scrollbar = ttk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Attach the scrollbar to the list box.
        scrollbar.config(command=self.listbox.yview)
        # Configure the list box to use the scrollbar.
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Pack the list box.
        # Use fill=tk.BOTH and expand=True to make the list box resize with the window.
        # This will make your application look better on different screen sizes.
        self.listbox.pack(fill=tk.BOTH, expand=True)
        # Load tasks from file when program starts
        self.load_tasks()
        # Start the main loop
        self.root.mainloop()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Use a modern-looking theme.
    todo_list = ToDoList(root)
    todo_list.run()
