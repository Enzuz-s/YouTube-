import os
import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk, filedialog

# Import your YouTube downloader script functions
from YouMain import download_video_with_options, move_thumbnails, remove_ytdl_files


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader GUI")
        self.root.geometry("")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.video_url_var = tk.StringVar()
        self.file_location_var = tk.StringVar()
        self.options_var = {
            'video_quality': tk.StringVar(value='best'),
            'audio_format': tk.StringVar(value='best'),
            'subtitles': tk.BooleanVar(value=True)
        }

        self.create_widgets()

    def create_widgets(self):
        # Video URL Entry
        tk.Label(self.root, text="YouTube Video URL:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.video_url_var, width=40).grid(row=0, column=1, padx=10, pady=5)

        # File Location Entry with Browse button
        tk.Label(self.root, text="Save Files to:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.file_location_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_file_location).grid(row=1, column=2, pady=5)

        # Options Frame
        options_frame = ttk.LabelFrame(self.root, text="Download Options")
        options_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Video Quality Dropdown
        tk.Label(options_frame, text="Video Quality:").grid(row=0, column=0, padx=5, pady=5)
        video_quality_menu = ttk.Combobox(options_frame, textvariable=self.options_var['video_quality'],
                                          values=['best', '720p', '1080p'])
        video_quality_menu.grid(row=0, column=1, padx=5, pady=5)

        # Audio Format Dropdown
        tk.Label(options_frame, text="Audio Format:").grid(row=1, column=0, padx=5, pady=5)
        audio_format_menu = ttk.Combobox(options_frame, textvariable=self.options_var['audio_format'],
                                         values=['best', 'mp3', 'aac'])
        audio_format_menu.grid(row=1, column=1, padx=5, pady=5)

        # Subtitles Checkbutton
        tk.Checkbutton(options_frame, text="Include Subtitles", variable=self.options_var['subtitles']).grid(row=2, column=0,
                                                                                                             columnspan=2,
                                                                                                             pady=5)

        # Download Button
        tk.Button(self.root, text="Download", command=self.download).grid(row=3, column=0, columnspan=3, pady=10)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, mode='indeterminate')
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

    def browse_file_location(self):
        file_location = filedialog.askdirectory()
        if file_location:
            self.file_location_var.set(file_location)

    def download(self):
        video_url = self.video_url_var.get()
        file_location = self.file_location_var.get()
        options = {
            'video_quality': self.options_var['video_quality'].get(),
            'audio_format': self.options_var['audio_format'].get(),
            'subtitles': self.options_var['subtitles'].get()
        }

        if not os.path.isdir(file_location):
            messagebox.showerror("Error", "Invalid file location.")
            return

        # Disable the Download button during download
        download_button = self.root.nametowidget(".!button")
        download_button["state"] = "disabled"

        # Run the YouTube downloader script functions in a separate thread
        thread = Thread(target=self.run_youtube_downloader, args=(video_url, file_location, options))
        thread.start()

    def run_youtube_downloader(self, video_url, file_location, options):
        try:
            # Show the progress bar
            self.progress_bar.start()

            download_video_with_options(video_url, file_location, options)
            move_thumbnails(file_location, os.path.join(file_location, 'thumbnails'))
            remove_ytdl_files(file_location)
            messagebox.showinfo("Success", "Download completed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            # Enable the Download button after download completion or failure
            download_button = self.root.nametowidget(".!button")
            download_button["state"] = "normal"

            # Stop the progress bar
            self.progress_bar.stop()

    def on_close(self):
        # Ask for confirmation before closing the application
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
