# Youtube-Watch-Later-Save
**ListTube**
A program that takes the youtube video link and saves it as thumbnail table list. Powered with Tkinter, graphical user interface.

**ttk**: Standart Tkinter components compatable with modern OS
**messagebox**: It is a library used to report errors and issues to the user.
**requests**: Enables us to send HTTP requests to the internet. It is used to connect to YouTube's servers and download thumbnail images for the programs.
**PILLOW**: Python's offical photo processing libary.
**io.BytesIO**: A library that allows us to use RAM to save images instead of saving it to the disk. (After the program closes, the photos in RAM do not persist, nor do they continue to occupy space in the RAM.)
**json**: A classic database allows us to store and read video links and cover image URLs in a text-like file json.
**OS**: In the file system, It checks If the file that the program uses exist, or not.

## How It Works (Architecture)

1. **Initialization (`__init__` & `load_from_json`)**
   - The application initializes the main Tkinter window and hooks a window close event (`WM_DELETE_WINDOW`) to trigger auto-saving.
   - It checks for an existing `videos.json` file on launch and populates the stored video data.

2. **Scrollable Container Setup (`setup_ui`)**
   - Uses a `tk.Canvas` combined with a `ttk.Scrollbar` and an inner `ttk.Frame`.
   - The canvas dynamically updates its scrollable region whenever new video cards alter the internal height of the frame.

3. **URL Processing & Image Fetching (`add_video` & `add_video_card`)**
   - Extracts the YouTube Video ID from the user input.
   - Generates the standard thumbnail URL (`https://img.youtube.com/vi/<VIDEO_ID>/hqdefault.jpg`).
   - Fetches the image asynchronously via `requests`, loads it into memory using `io.BytesIO`, and resizes it with `Pillow` (PIL) for UI display.
   - Holds references in `self.image_references` to prevent Python's garbage collector from purging rendered thumbnails.

4. **Data Persistence (`on_closing`)**
   - When exiting the app, the state array containing all video URLs and thumbnail endpoints is dumped safely into `videos.json`.
