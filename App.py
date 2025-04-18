import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from QRCodeFeature import QRCodeFeature
from AIChatFeature import AIChatFeature
from CompareFoldersFeature import CompareFoldersFeature
from FileListFeature import FileListFeature
from HashFeature import HashFeature
from OpenAllPDFsFeature import OpenAllPDFsFeature


class App(tk.Tk):
    def __init__(self, features):
        super().__init__()
        self.title("Meine App mit Features")
        self.geometry("700x700")
        self.features = features

        self.content_frame = ttk.Frame(self, padding=10)
        self.content_frame.pack(fill="both", expand=True)

        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title = ttk.Label(self.content_frame, text="Wähle ein Feature:", font=("Arial", 18))
        title.pack(pady=20)

        grid_frame = ttk.Frame(self.content_frame)
        grid_frame.pack()

        columns = 3
        size = 180  # Größe der Kachel

        for index, feature in enumerate(self.features):
            row = index // columns
            col = index % columns

            name = feature.__class__.__name__
            icon_path = f"icons/{name}.png"

            try:
                img = Image.open(icon_path).resize((96, 96), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Fehler beim Laden von {icon_path}: {e}")
                photo = None

            tile = ttk.Frame(grid_frame, width=size, height=size, relief="flat", padding=5)
            tile.grid(row=row, column=col, padx=20, pady=20)
            tile.grid_propagate(False)

            tile.bind("<Button-1>", lambda e, f=feature: f.run(self.content_frame, self.show_main_menu))

            if photo:
                label_img = ttk.Label(tile, image=photo)
                label_img.image = photo
                label_img.pack(pady=(5, 5))
                label_img.bind("<Button-1>", lambda e, f=feature: f.run(self.content_frame, self.show_main_menu))

            label_txt = ttk.Label(tile, text=name, anchor="center", wraplength=140, font=("Arial", 11))
            label_txt.pack()
            label_txt.bind("<Button-1>", lambda e, f=feature: f.run(self.content_frame, self.show_main_menu))


if __name__ == "__main__":
    features = [
        QRCodeFeature(),
        AIChatFeature(),
        CompareFoldersFeature(),
        FileListFeature(),
        HashFeature(),
        OpenAllPDFsFeature()
    ]

    app = App(features=features)
    app.mainloop()