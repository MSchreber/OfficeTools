import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import platform

from Feature import Feature


class OpenAllPDFsFeature(Feature):
    def run(self, frame, return_callback):
        for widget in frame.winfo_children():
            widget.destroy()

        label = ttk.Label(frame, text="Alle PDFs in einem Ordner öffnen")
        label.pack(pady=10)

        def choose_and_open():
            folder = filedialog.askdirectory(title="Wähle einen Ordner")
            if not folder:
                return

            pdf_files = []
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        pdf_files.append(os.path.join(root, file))

            if not pdf_files:
                messagebox.showinfo("Keine PDFs", "Keine PDF-Dateien gefunden.")
                return

            opened = 0
            for pdf in pdf_files:
                try:
                    if platform.system() == "Windows":
                        os.startfile(pdf)
                    elif platform.system() == "Darwin":
                        subprocess.run(["open", pdf])
                    else:
                        subprocess.run(["xdg-open", pdf])
                    opened += 1
                except Exception as e:
                    print(f"Fehler beim Öffnen: {pdf} → {e}")

            messagebox.showinfo("Fertig", f"{opened} PDF(s) wurden geöffnet.")

        open_btn = ttk.Button(frame, text="Ordner auswählen und PDFs öffnen", command=choose_and_open)
        open_btn.pack(pady=10)

        back_btn = ttk.Button(frame, text="Zurück", command=return_callback)
        back_btn.pack(pady=20)