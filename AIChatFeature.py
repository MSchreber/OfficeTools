import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from Feature import Feature
from dotenv import load_dotenv
import markdown
from tkhtmlview import HTMLLabel

load_dotenv()


class AIChatFeature(Feature):
    def run(self, frame, return_callback):
        for widget in frame.winfo_children():
            widget.destroy()

        api_key = os.getenv("DEEPSEEK_API_KEY")
        api_url = "https://api.deepseek.com/v1/chat/completions"
        model_name = "deepseek-chat"

        if not api_key:
            messagebox.showerror("Fehlende API", "Bitte setze DEEPSEEK_API_KEY in deiner .env-Datei.")
            return_callback()
            return

        messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent."}]

        # Layout: Chat oben (scrollbar), Eingabe unten (fixiert)
        outer_frame = ttk.Frame(frame)
        outer_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer_frame, borderwidth=0)
        chat_frame = ttk.Frame(canvas)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=chat_frame, anchor="nw")

        chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Eingabebereich
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", side="bottom")

        user_input = tk.Text(input_frame, height=4, wrap=tk.WORD)
        user_input.pack(fill="x", padx=10, pady=(5, 2), expand=False)

        button_row = ttk.Frame(input_frame)
        button_row.pack(pady=2)
        ttk.Button(button_row, text="Senden", command=lambda: send_message()).pack(side="left", padx=5)
        ttk.Button(button_row, text="Zurück", command=return_callback).pack(side="left", padx=5)

        def send_message():
            content = user_input.get("1.0", tk.END).strip()
            if not content:
                return
            user_input.delete("1.0", tk.END)

            add_user_message("Du", content)
            messages.append({"role": "user", "content": content})

            # Antwort-Container vorbereiten
            html_label = HTMLLabel(chat_frame, html="Antwort wird geladen...", background="white", padx=10, pady=10)
            html_label.pack(fill="x", padx=10, pady=5)
            frame.update_idletasks()
            canvas.yview_moveto(1.0)

            try:
                response = requests.post(
                    api_url,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model_name,
                        "messages": messages,
                        "stream": False  # streaming buggy – daher erst einmal aus
                    }
                )
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]

                messages.append({"role": "assistant", "content": reply})
                html = markdown.markdown(reply, extensions=["fenced_code", "codehilite"])
                html_label.set_html(html)
                canvas.yview_moveto(1.0)

            except Exception as e:
                html_label.set_html(f"<b>Fehler:</b><br>{str(e)}")

        def add_user_message(sender, content):
            sender_label = ttk.Label(chat_frame, text=sender + ":", font=("Arial", 10, "bold"))
            sender_label.pack(anchor="w", padx=10, pady=(10, 0))
            msg_box = scrolledtext.ScrolledText(chat_frame, height=5, wrap=tk.WORD)
            msg_box.insert(tk.END, content)
            msg_box.configure(state="disabled")
            msg_box.pack(fill="x", padx=10, pady=(0, 10))
            canvas.yview_moveto(1.0)