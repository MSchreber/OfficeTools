import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Feature import Feature


class HashFeature(Feature):
    def run(self, frame, return_callback):
        for widget in frame.winfo_children():
            widget.destroy()

        hash_algorithms = {
            "SHA-256": hashlib.sha256,
            "SHA-1": hashlib.sha1,
            "MD5": hashlib.md5
        }

        selected_algo = tk.StringVar(value="SHA-256")

        ttk.Label(frame, text="Wähle Hash-Verfahren:").pack(pady=5)
        algo_menu = ttk.OptionMenu(frame, selected_algo, "SHA-256", *hash_algorithms.keys())
        algo_menu.pack(pady=5)

        def hash_file(path, algo_func):
            hasher = algo_func()
            try:
                with open(path, "rb") as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
                return hasher.hexdigest()
            except Exception as e:
                return f"Fehler: {e}"

        def choose_file():
            clear_frame()
            file_path = filedialog.askopenfilename()
            if not file_path:
                return

            hasher = hash_algorithms[selected_algo.get()]
            hash_value = hash_file(file_path, hasher)

            ttk.Label(content_frame, text="Dateipfad:").pack(pady=5)
            ttk.Label(content_frame, text=file_path, wraplength=500).pack(pady=5)

            ttk.Label(content_frame, text="Hashwert:").pack(pady=5)
            hash_var = tk.StringVar(value=hash_value)
            entry = ttk.Entry(content_frame, textvariable=hash_var, width=80)
            entry.pack(pady=5)

            def copy_hash():
                frame.clipboard_clear()
                frame.clipboard_append(hash_var.get())
                frame.update()
                messagebox.showinfo("Kopiert", "Hashwert kopiert.")

            ttk.Button(content_frame, text="Kopieren", command=copy_hash).pack(pady=5)

        def choose_folder():
            clear_frame()
            folder_path = filedialog.askdirectory()
            if not folder_path:
                return

            hasher = hash_algorithms[selected_algo.get()]
            files = []
            for root, _, filenames in os.walk(folder_path):
                for name in filenames:
                    path = os.path.join(root, name)
                    hash_val = hash_file(path, hasher)
                    files.append((name, path, hash_val))

            files.sort(key=lambda x: x[0])

            table = ttk.Treeview(content_frame, columns=("name", "path", "hash"), show="headings")
            table.heading("name", text="Dateiname")
            table.heading("path", text="Pfad")
            table.heading("hash", text="Hashwert")
            table.column("name", width=150)
            table.column("path", width=300)
            table.column("hash", width=300)
            table.pack(fill="both", expand=True)

            for name, path, hash_val in files:
                table.insert("", "end", values=(name, path, hash_val))

        def clear_frame():
            for w in content_frame.winfo_children():
                w.destroy()

        ttk.Button(frame, text="Datei auswählen", command=choose_file).pack(pady=5)
        ttk.Button(frame, text="Ordner auswählen", command=choose_folder).pack(pady=5)

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, pady=10)

        ttk.Button(frame, text="Zurück", command=return_callback).pack(pady=10)