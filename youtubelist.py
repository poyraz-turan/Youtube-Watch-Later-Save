import json
import os
from io import BytesIO
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser  # Tarayıcıda link açmak için eklendi
from PIL import Image, ImageTk
import requests


class YouTubeSaverApp:

    def __init__(self, root):
        self.root = root
        self.root.title("ListTube")
        self.root.geometry("480x600")

        self.json_file = "video_list.json"
        self.video_data = []  
        self.image_references = []  # To Prevent Garbage collector from deleting images.

        # Json save
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Json load
        self.load_from_json()

        self.setup_ui()

        # load the previus saved youtube videos to the list fron json
        self.render_saved_videos()

    def extract_video_id(self, url):
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return None

    def get_thumbnail_url(self, video_id):
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    def open_link(self, url):
        """Varsayılan web tarayıcısında YouTube linkini açar."""
        webbrowser.open_new_tab(url)

    def setup_ui(self):
        # Yeşil buton için ttk stili
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Green.TButton",
            background="#28a745",
            foreground="white",
            font=("Helvetica", 9, "bold"),
            padding=5
        )
        style.map(
            "Green.TButton",
            background=[('active', '#218838')]  # Fareyle üzerine gelindiğinde koyu yeşil
        )

        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="YouTube Link:").pack(
            side=tk.LEFT, padx=(0, 5)
        )

        self.url_entry = ttk.Entry(top_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        add_btn = ttk.Button(
            top_frame, text="ADD", style="Green.TButton", command=self.add_video
        )
        add_btn.pack(side=tk.RIGHT)

        list_container = ttk.Frame(self.root)
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.canvas = tk.Canvas(list_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            list_container, orient="vertical", command=self.canvas.yview
        )

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            ),
        )

    def add_video(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Hey!", "Please type a valid youtube link. Make sure that you copied the correct link. Try pressing share button on youtube and copy the link provided there")
            return

        video_id = self.extract_video_id(url)
        if not video_id:
            messagebox.showerror(
                "Hey!", "Invalid youtube link. A problem occured while trying to load this youtube video. Maybe it is off-listed or private or removed from youtube."
            )
            return

        thumb_url = self.get_thumbnail_url(video_id)

        item = {"link": url, "thumbnail": thumb_url}
        self.video_data.append(item)
        self.add_video_card(item)

        self.url_entry.delete(0, tk.END)

    def add_video_card(self, item):
        card = ttk.Frame(self.scrollable_frame, padding=5, relief="groove")
        card.pack(fill=tk.X, expand=True, pady=5, padx=5)

        # download thumbnail
        try:
            res = requests.get(item["thumbnail"], timeout=5)
            img_data = Image.open(BytesIO(res.content))
            img_data = img_data.resize((160, 90), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_data)

            self.image_references.append(photo)

            img_label = ttk.Label(card, image=photo, cursor="hand2")
            img_label.pack(side=tk.LEFT, padx=(0, 10))
            # Resme tıklayınca videoyu açma
            img_label.bind("<Button-1>", lambda e, u=item["link"]: self.open_link(u))
        except Exception:
            err_label = ttk.Label(card, text="[Couldn't Load]")
            err_label.pack(side=tk.LEFT, padx=(0, 10))

        # Link etiketi (mavi renkte ve tıklanabilir)
        link_label = ttk.Label(
            card, text=item["link"], wraplength=240, cursor="hand2", foreground="blue"
        )
        link_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Link metnine tıklayınca videoyu açma
        link_label.bind("<Button-1>", lambda e, u=item["link"]: self.open_link(u))

    def render_saved_videos(self):
        for item in self.video_data:
            self.add_video_card(item)

    def load_from_json(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    self.video_data = json.load(f)
            except Exception as e:
                print(f"An Error occured while trying to load JSON file. Try again: {e}")
                self.video_data = []

    def on_closing(self):
        try:
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(self.video_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Data save, failed: {e}")

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeSaverApp(root)
    root.mainloop()