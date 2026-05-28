import threading
import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext

from main import download_novel


class DownloaderUI:

    def __init__(self, root):

        self.root = root

        self.root.title("NovelBin Downloader")

        self.root.geometry("900x700")

        self.root.configure(bg="#1e1e1e")

        self.build_ui()

    def build_ui(self):

        title = tk.Label(
            self.root,
            text="NovelBin Downloader",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#1e1e1e"
        )

        title.pack(pady=20)

        # URL
        url_label = tk.Label(
            self.root,
            text="Novel URL",
            fg="white",
            bg="#1e1e1e",
            font=("Segoe UI", 11)
        )

        url_label.pack(anchor="w", padx=20)

        self.url_entry = tk.Entry(
            self.root,
            width=110,
            font=("Segoe UI", 10)
        )

        self.url_entry.pack(
            padx=20,
            pady=5
        )

        # Range Frame
        range_frame = tk.Frame(
            self.root,
            bg="#1e1e1e"
        )

        range_frame.pack(pady=10)

        tk.Label(
            range_frame,
            text="Start Chapter",
            fg="white",
            bg="#1e1e1e"
        ).grid(row=0, column=0, padx=5)

        self.start_entry = tk.Entry(
            range_frame,
            width=10
        )

        self.start_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            range_frame,
            text="End Chapter",
            fg="white",
            bg="#1e1e1e"
        ).grid(row=0, column=2, padx=5)

        self.end_entry = tk.Entry(
            range_frame,
            width=10
        )

        self.end_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        # Download Button
        self.download_btn = tk.Button(
            self.root,
            text="Start Download",
            width=22,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.start_download
        )

        self.download_btn.pack(pady=15)

        # Progress
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=750,
            mode="determinate"
        )

        self.progress.pack(pady=10)

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Idle",
            fg="#4CAF50",
            bg="#1e1e1e",
            font=("Segoe UI", 10)
        )

        self.status_label.pack()

        # Logs
        self.logs = scrolledtext.ScrolledText(
            self.root,
            width=110,
            height=28,
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

    def update_progress(self, current, total):

        self.progress["maximum"] = total

        self.progress["value"] = current

        self.root.update_idletasks()

    def update_status(self, message):

        self.status_label.config(
            text=message
        )

        self.root.update_idletasks()

    def start_download(self):

        thread = threading.Thread(
            target=self.download
        )

        thread.daemon = True

        thread.start()

    def download(self):

        url = self.url_entry.get().strip()

        if not url:

            messagebox.showerror(
                "Error",
                "Please enter a URL"
            )

            return

        try:

            start = int(
                self.start_entry.get()
            )

            end = int(
                self.end_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Start and End must be numbers"
            )

            return

        self.download_btn.config(
            state=tk.DISABLED
        )

        self.logs.delete(
            "1.0",
            tk.END
        )

        self.log("Starting download...\n")

        try:

            result = download_novel(
                url=url,
                start=start,
                end=end,
                progress_callback=self.update_progress,
                status_callback=self.update_status,
                log_callback=self.log
            )

            self.log("\nDownload complete.\n")

            self.log(
                f"Saved: {result['saved']}"
            )

            self.log(
                f"Failed: {result['failed']}"
            )

            self.log(
                f"Folder: {result['folder']}"
            )

            messagebox.showinfo(
                "Finished",
                f"Saved: {result['saved']}\n"
                f"Failed: {result['failed']}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            self.download_btn.config(
                state=tk.NORMAL
            )

            self.status_label.config(
                text="Idle"
            )


root = tk.Tk()

app = DownloaderUI(root)

root.mainloop()