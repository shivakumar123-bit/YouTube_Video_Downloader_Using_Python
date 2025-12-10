import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox

# -----------------------------
# SELECT FOLDER
# -----------------------------
def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    folder = filedialog.askdirectory(title="Select Folder to Save Video")
    root.destroy()
    return folder

# -----------------------------
# GET AVAILABLE WEBM VIDEO QUALITIES
# -----------------------------
def get_webm_formats(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = info.get("formats", [])
    quality_list = []

    for f in formats:
        if (
            f.get("ext") == "webm" 
            and f.get("vcodec") != "none"
        ):
            height = f.get("height")
            if height:
                label = f"{height}p"
                if label not in quality_list:
                    quality_list.append(label)

    # Sort by resolution (highest first)
    quality_list.sort(key=lambda x: int(x.replace("p", "")), reverse=True)

    return quality_list

# -----------------------------
# DOWNLOAD VIDEO + MERGE AUDIO
# -----------------------------
def download_webm(url, path, quality):
    try:
        ydl_opts = {
            "format": f"bestvideo[height={quality.replace('p','')}][ext=webm]+bestaudio[ext=webm]/best",
            "merge_output_format": "webm",
            "outtmpl": f"{path}/%(title)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", f"Downloaded Successfully in {quality} 🎉")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# -----------------------------
# MAIN
# -----------------------------
def main():
    url = input("Enter YouTube Video URL: ")

    # Fetch available qualities
    print("\nFetching available qualities... Please wait...\n")
    qualities = get_webm_formats(url)

    if not qualities:
        print("No WebM qualities found! (Very rare)")
        return

    print("Available WebM Qualities:")
    for i, q in enumerate(qualities, start=1):
        print(f"{i}) {q}")

    choice = int(input("\nSelect quality number: "))
    selected_quality = qualities[choice - 1]

    # Folder selection
    folder = select_folder()
    if not folder:
        messagebox.showwarning("Warning", "No folder selected!")
        return

    # Download
    download_webm(url, folder, selected_quality)

# Run program
if __name__ == "__main__":
    main()