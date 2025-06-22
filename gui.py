import tkinter as tk
from tkinter import messagebox, filedialog
from cipher import caesar_encrypt, caesar_decrypt
from utils import save_to_file, load_from_file

def normalize_shift(shift):
    return shift % 26

def brute_force_decrypt(cipher_text):
    possibilities = []
    for shift in range(1, 26):
        decrypted = caesar_decrypt(cipher_text, shift)
        possibilities.append(f"Shift {shift}: {decrypted}")
    return possibilities

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher - Encrypt & Decrypt")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")  # Dark background

        self.mode = tk.StringVar(value="encrypt")
        self.placeholder_text = "Enter your message here..."

        self.setup_ui()

    def setup_ui(self):
        # Mode selection
        mode_frame = tk.Frame(self.root, bg="#1e1e1e")
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Mode:", bg="#1e1e1e", fg="#00ff99").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Encrypt", variable=self.mode, value="encrypt",
                       bg="#1e1e1e", fg="#ffffff", selectcolor="#2e2e2e", activebackground="#2e2e2e",
                       command=self.toggle_shift).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Decrypt", variable=self.mode, value="decrypt",
                       bg="#1e1e1e", fg="#ffffff", selectcolor="#2e2e2e", activebackground="#2e2e2e",
                       command=self.toggle_shift).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Brute Force Decrypt", variable=self.mode, value="brute",
                       bg="#1e1e1e", fg="#ffffff", selectcolor="#2e2e2e", activebackground="#2e2e2e",
                       command=self.toggle_shift).pack(side=tk.LEFT, padx=10)

        # Message input
        self.input_text = tk.Text(self.root, height=8, width=70, bg="#2e2e2e", fg="#888888", insertbackground="white")
        self.input_text.pack(pady=10)
        self.input_text.insert(tk.END, self.placeholder_text)
        self.input_text.bind("<FocusIn>", self.clear_placeholder)
        self.input_text.bind("<FocusOut>", self.restore_placeholder)

        # Shift input
        shift_frame = tk.Frame(self.root, bg="#1e1e1e")
        shift_frame.pack(pady=10)

        tk.Label(shift_frame, text="Shift:", bg="#1e1e1e", fg="#00ff99").pack(side=tk.LEFT)
        self.shift_entry = tk.Entry(shift_frame, width=5, bg="#2e2e2e", fg="#ffffff", insertbackground="white")
        self.shift_entry.pack(side=tk.LEFT, padx=10)

        # Action buttons
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Run", command=self.process,
                  bg="#00ff99", fg="#1e1e1e", activebackground="#00cc77").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Clear", command=self.clear_all,
                  bg="#ff5555", fg="#ffffff", activebackground="#cc4444").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Load From File", command=self.load_file,
                  bg="#ffaa00", fg="#1e1e1e", activebackground="#e69500").pack(side=tk.LEFT, padx=10)

        # Output
        tk.Label(self.root, text="Result:", bg="#1e1e1e", fg="#00ff99").pack()
        self.output_text = tk.Text(self.root, height=10, width=70, bg="#2e2e2e", fg="#ffffff", insertbackground="white")
        self.output_text.pack(pady=10)

        # Save button
        tk.Button(self.root, text="Save Result to File", command=self.save_result,
                  bg="#007acc", fg="#ffffff", activebackground="#005f99").pack(pady=5)

    def toggle_shift(self):
        if self.mode.get() == "brute":
            self.shift_entry.config(state=tk.DISABLED)
        else:
            self.shift_entry.config(state=tk.NORMAL)

    def clear_placeholder(self, event):
        current_text = self.input_text.get("1.0", tk.END).strip()
        if current_text == self.placeholder_text:
            self.input_text.delete("1.0", tk.END)
            self.input_text.config(fg="#ffffff")

    def restore_placeholder(self, event):
        current_text = self.input_text.get("1.0", tk.END).strip()
        if not current_text:
            self.input_text.insert("1.0", self.placeholder_text)
            self.input_text.config(fg="#888888")

    def process(self):
        message = self.input_text.get("1.0", tk.END).strip()
        if message == self.placeholder_text:
            message = ""

        if self.mode.get() == "brute":
            results = brute_force_decrypt(message)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\n".join(results))
        else:
            try:
                shift = normalize_shift(int(self.shift_entry.get()))
            except ValueError:
                messagebox.showerror("Invalid Input", "Shift must be an integer.")
                return

            if self.mode.get() == "encrypt":
                result = caesar_encrypt(message, shift)
            else:
                result = caesar_decrypt(message, shift)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", self.placeholder_text)
        self.input_text.config(fg="#888888")
        self.output_text.delete("1.0", tk.END)
        self.shift_entry.config(state=tk.NORMAL)
        self.shift_entry.delete(0, tk.END)

    def save_result(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if not result:
            messagebox.showwarning("Empty Output", "There's no result to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            save_to_file(file_path, result)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            content = load_from_file(file_path)
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, content)
            self.input_text.config(fg="#ffffff")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()
