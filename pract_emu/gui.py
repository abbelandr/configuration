import tkinter as tk
from tkinter import font


class ConsoleGUI:
    def __init__(self, root, shell_instance):
        self.root = root
        self.shell = shell_instance

        # Требование Этапа 1.2: Заголовок окна из реальных данных ОС
        self.root.title(f"Эмулятор - [{self.shell.username}@{self.shell.hostname}]")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.console_font = font.Font(family="Consolas", size=12)

        self.text_area = tk.Text(root, bg="black", fg="white", font=self.console_font,
                                 insertbackground="white", state="disabled", wrap="word")
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        self.text_area.tag_config("red", foreground="#FF5555")
        self.text_area.tag_config("green", foreground="#50FA7B")
        self.text_area.tag_config("blue", foreground="#8BE9FD")
        self.text_area.tag_config("yellow", foreground="#F1FA8C")
        self.text_area.tag_config("white", foreground="#F8F8F2")

        self.input_frame = tk.Frame(root, bg="black")
        self.input_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.prompt_label = tk.Label(self.input_frame, text="", bg="black", fg="#50FA7B", font=self.console_font)
        self.prompt_label.pack(side="left")

        self.entry = tk.Entry(self.input_frame, bg="black", fg="white", font=self.console_font,
                              insertbackground="white", bd=0, highlightthickness=0)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_enter)

        self.shell.write = self.print_to_console
        self.update_prompt()
        self.entry.focus_set()

    def print_to_console(self, text, color="white"):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, text, color)
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def update_prompt(self):
        self.prompt_label.config(text=self.shell.get_prompt())

    def on_enter(self, event):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        self.print_to_console(self.shell.get_prompt() + cmd + "\n")
        self.shell.execute_command(cmd)
        self.update_prompt()
        if not self.shell.running:
            self.root.after(1000, self.root.destroy)