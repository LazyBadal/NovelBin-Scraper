import threading
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

from epub_builder import build_epub


class EPUBBuilderUI:

    def __init__(self, root):

        self.root = root

        self.root.title("EPUB Builder")

        self.root.geometry("800x500")

        self.root.configure(bg="#1e1e1e")

        self.folder_path = ""

        self.build_ui()

    def build_ui(self):

        title = tk.Label(
            self.root,
            text="TXT → EPUB Builder",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#1e1e1e"
        )

        title.pack(pady=20)

        # Folder section
        folder_frame = tk.Frame(
            self.root,
            bg="#1e1e1e"
        )

        folder_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.folder_label = tk.Label(
            folder_frame,
            text="No folder selected",
            fg="#00ff88",
            bg="#1e1e1e",
            anchor="w",
            font=("Segoe UI", 10)
        )

        self.folder_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        browse_btn = tk.Button(
            folder_frame,
            text="Browse Folder",
            command=self.select_folder,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold")
        )

        browse_btn.pack(side="right")

        # Convert button
        self.convert_btn = tk.Button(
            self.root,
            text="Build EPUB",
            width=22,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.start_build
        )

        self.convert_btn.pack(pady=20)

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Idle",
            fg="#00ff88",
            bg="#1e1e1e",
            font=("Segoe UI", 10)
        )

        self.status_label.pack()

        # Logs
        self.logs = scrolledtext.ScrolledText(
            self.root,
            width=95,
            height=18,
            bg="#121212",
            fg="#00ff88",
            insertbackground="white",
            font=("Consolas", 9)
        )

        self.logs.pack(
            padx=20,
            pady=20
        )

    def log(self, message):

        self.logs.insert(
            tk.END,
            message + "\n"
        )

        self.logs.see(tk.END)

        self.root.update_idletasks()

    def select_folder(self):

        folder = filedialog.askdirectory()

        if not folder:
            return

        self.folder_path = folder

        self.folder_label.config(
            text=folder
        )

        self.log(f"Selected folder: {folder}")

    def start_build(self):

        thread = threading.Thread(
            target=self.build_epub_thread
        )

        thread.daemon = True

        thread.start()

    def build_epub_thread(self):

        if not self.folder_path:

            messagebox.showerror(
                "Error",
                "Please select a folder"
            )

            return

        self.convert_btn.config(
            state=tk.DISABLED
        )

        self.status_label.config(
            text="Building EPUB..."
        )

        self.logs.delete(
            "1.0",
            tk.END
        )

        try:

            book_title = self.folder_path.split("/")[-1]

            self.log("Starting EPUB creation...\n")

            build_epub(
                self.folder_path,
                book_title
            )

            self.log("\nEPUB created successfully.")

            self.log(
                f"Saved in:\n{self.folder_path}"
            )

            messagebox.showinfo(
                "Success",
                "EPUB created successfully."
            )

        except Exception as e:

            self.log(f"\nERROR:\n{str(e)}")

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            self.convert_btn.config(
                state=tk.NORMAL
            )

            self.status_label.config(
                text="Idle"
            )


root = tk.Tk()

app = EPUBBuilderUI(root)

root.mainloop()