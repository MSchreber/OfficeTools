import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog
from Feature import Feature


class CompareFoldersFeature(Feature):
    def run(self, frame, return_callback):
        for widget in frame.winfo_children():
            widget.destroy()

        label = ttk.Label(frame, text="Vergleiche zwei Ordner nach Dateiinhalt (Hash)", font=("Arial", 12))
        label.pack(pady=10)

        info_label = ttk.Label(frame, text="", font=("Arial", 10))
        info_label.pack(pady=5)

        def choose_and_compare():
            folder1 = filedialog.askdirectory(title="Wähle Ordner 1")
            if not folder1:
                return
            folder2 = filedialog.askdirectory(title="Wähle Ordner 2")
            if not folder2:
                return

            def get_files_with_hash(folder, ordner_nummer):
                entries = []
                for root, _, filenames in os.walk(folder):
                    for filename in filenames:
                        path = os.path.join(root, filename)
                        try:
                            with open(path, "rb") as f:
                                file_hash = hashlib.sha256(f.read()).hexdigest()
                            entries.append({
                                "filename": filename,
                                "hash": file_hash,
                                "folder": ordner_nummer,
                                "full_path": path
                            })
                        except Exception as e:
                            print(f"Fehler bei {path}: {e}")
                return entries

            entries1 = get_files_with_hash(folder1, 1)
            entries2 = get_files_with_hash(folder2, 2)
            all_entries = entries1 + entries2

            # Prüfen, ob Hash in beiden Ordnern existiert
            hash_map = {}
            for entry in all_entries:
                h = entry["hash"]
                if h not in hash_map:
                    hash_map[h] = set()
                hash_map[h].add(entry["folder"])

            matched = 0
            for entry in all_entries:
                h = entry["hash"]
                entry["in_both"] = "✔️" if len(hash_map[h]) > 1 else "❌"
                if entry["in_both"] == "✔️":
                    matched += 1

            total = len(all_entries)
            info_label.config(text=f"Übereinstimmungen: {matched} / {total} Dateien ({matched / total:.1%})")

            # Tabelle
            table_frame = ttk.Frame(frame)
            table_frame.pack(fill="both", expand=True, pady=10)

            tree = ttk.Treeview(table_frame, columns=("filename", "hash", "folder", "both"), show="headings")
            tree.heading("filename", text="Dateiname")
            tree.heading("hash", text="SHA-256")
            tree.heading("folder", text="Ordner")
            tree.heading("both", text="In beiden Ordnern?")
            tree.column("filename", width=200)
            tree.column("hash", width=300)
            tree.column("folder", width=80, anchor="center")
            tree.column("both", width=150, anchor="center")

            for entry in all_entries:
                tree.insert("", "end", values=(
                    entry["filename"],
                    entry["hash"],
                    entry["folder"],
                    entry["in_both"]
                ))

            tree.pack(fill="both", expand=True)

        ttk.Button(frame, text="Ordner auswählen & vergleichen", command=choose_and_compare).pack(pady=10)
        ttk.Button(frame, text="Zurück", command=return_callback).pack(pady=20)