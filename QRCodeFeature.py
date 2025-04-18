import qrcode
from PIL import ImageTk, Image
import io
import tkinter as tk
from tkinter import ttk, filedialog
from Feature import Feature

class QRCodeFeature(Feature):
    def run(self, frame, return_callback):
        # Vorherigen Inhalt löschen
        for widget in frame.winfo_children():
            widget.destroy()

        label = ttk.Label(frame, text="Gib eine URL ein:")
        label.pack(pady=10)

        url_entry = ttk.Entry(frame, width=40)
        url_entry.pack(pady=5)

        qr_label = ttk.Label(frame)
        qr_label.pack(pady=10)

        def generate_qr():
            url = url_entry.get()
            img = qrcode.make(url)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            photo = ImageTk.PhotoImage(Image.open(buffer))
            qr_label.configure(image=photo)
            qr_label.image = photo  # Referenz behalten

        def save_qr():
            url = url_entry.get()
            img = qrcode.make(url)
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Dateien", "*.png")])
            if filepath:
                img.save(filepath)

        gen_btn = ttk.Button(frame, text="QR erzeugen", command=generate_qr)
        gen_btn.pack(pady=5)

        save_btn = ttk.Button(frame, text="Speichern", command=save_qr)
        save_btn.pack(pady=5)

        back_btn = ttk.Button(frame, text="Zurück", command=return_callback)
        back_btn.pack(pady=20)