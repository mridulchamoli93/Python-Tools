import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
import hashlib
import os
import threading
import requests
from bs4 import BeautifulSoup
import webbrowser

# Tor proxy configuration
PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Search using DuckDuckGo onion service
def search_dark_web(keyword):
    try:
        url = f"https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/html?q={keyword}"
        headers = {"User-Agent": "DarkWebHunter/1.0"}
        response = requests.get(url, proxies=PROXIES, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for result in soup.find_all('a', class_='result__a'):
            title = result.get_text()
            link = result.get('href')
            results.append(f"• {title}\n🔗 {link}\n")
        
        return "\n".join(results) if results else "[×] No readable results found."
    except Exception as e:
        return f"[×] Error: Could not connect to .onion site.\nDetails: {e}"

# Hash image
def get_image_hash(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        return hashlib.sha256(data).hexdigest()
    except Exception as e:
        return f"[×] Failed to hash image: {e}"

# Save results
def save_results_to_file(data):
    with open("search_results.txt", "w") as f:
        f.write(data)
    messagebox.showinfo("Success", "Results have been saved to 'search_results.txt'.")

# Show related images
def show_related_images(keyword):
    search_url = f"https://duckduckgo.com/?q={keyword}+images&t=h_&iar=images&iax=images&ia=images"
    webbrowser.open(search_url)

# Simulate image display
def display_images(images, image_label):
    for img_path in images:
        try:
            image = Image.open(img_path)
            image = image.resize((150, 150))
            image_tk = ImageTk.PhotoImage(image)
            image_label.config(image=image_tk)
            image_label.image = image_tk
            break
        except Exception as e:
            print(f"[×] Error: Could not display image: {e}")

# Threaded search
def threaded_search(keyword, output_box, spinner_label, image_label):
    spinner_label.config(text="🔄 Loading...")
    output_box.insert(tk.END, f"\n[🔍] Searching: {keyword}\n", 'bold_green')
    result = search_dark_web(keyword)
    output_box.insert(tk.END, f"{result}\n", 'normal')
    spinner_label.config(text="")

    # Dummy local image paths (you can add your own)
    display_images(['abc.jpeg'], image_label)

# GUI function
def run_gui():
    def on_search():
        keyword = keyword_entry.get().strip()
        if not keyword:
            output_box.insert(tk.END, "[!] Enter a keyword first.\n")
            return
        search_thread = threading.Thread(target=threaded_search, args=(keyword, output_box, spinner_label, image_label))
        search_thread.start()

    def on_upload():
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if filepath:
            hash_val = get_image_hash(filepath)
            output_box.insert(tk.END, f"\n[📁] Image: {os.path.basename(filepath)}\n[🔑] SHA-256 Hash:\n{hash_val}\n", 'bold_green')
            output_box.insert(tk.END, "[~] (Simulated) Searching image hash on dark web...\n", 'normal')
        else:
            output_box.insert(tk.END, "[!] No image selected.\n", 'warning')

    def on_save():
        data = output_box.get("1.0", tk.END)
        if data.strip():
            save_results_to_file(data)
        else:
            messagebox.showwarning("No Data", "No data to save.")

    def on_show_images():
        keyword = keyword_entry.get().strip()
        if keyword:
            show_related_images(keyword)
        else:
            messagebox.showwarning("No Keyword", "Please enter a keyword to search for related images.")

    root = tk.Tk()
    root.title("🕶️ Dark Web Hunter")
    root.geometry("920x800")
    root.configure(bg="#111111")

    # Load and display logo
    try:
        logo_image = Image.open("abc.jpeg")
        logo_image = logo_image.resize((120, 120))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(root, image=logo_photo, bg="#0d0d0d")
        logo_label.image = logo_photo
        logo_label.pack(pady=(10, 5))
    except Exception as e:
        print(f"[×] Error loading logo: {e}")

    # Fonts and palette
    font_header = ("Courier New", 14, "bold")
    font_text = ("Courier New", 10)
    root.tk_setPalette(background="#0d0d0d", foreground="#00ff00")

    # App Title
    app_title = tk.Label(root, text="Dark Web Hunter", font=("Courier New", 18, "bold"), fg="#00ff00", bg="#0d0d0d")
    app_title.pack(pady=10)

    # Entry field
    keyword_entry = tk.Entry(root, width=60, font=font_text, bg="#222222", fg="#00ff00",
                             insertbackground="#00ff00", bd=0, highlightthickness=1, highlightcolor="#00ff00")
    keyword_entry.pack(pady=10)

    # Buttons
    btn_frame = tk.Frame(root, bg="#0d0d0d")
    btn_frame.pack(pady=15)

    style_btn = {
        "font": font_text, "bg": "#00ff00", "fg": "#000000",
        "activebackground": "#33ff33", "activeforeground": "#000000",
        "relief": tk.FLAT, "width": 15, "highlightthickness": 0
    }

    tk.Button(btn_frame, text="Search Keyword", command=on_search, **style_btn).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Upload Image", command=on_upload, **style_btn).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Save Results", command=on_save, **style_btn).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Show Related Images", command=on_show_images, **style_btn).pack(side=tk.LEFT, padx=10)

    # Spinner label
    spinner_label = tk.Label(root, text="", font=font_header, fg="#00ff00", bg="#0d0d0d")
    spinner_label.pack(pady=5)

    # Output box
    output_box = scrolledtext.ScrolledText(root, width=110, height=20, font=font_text, bg="#000000",
                                           fg="#00ff00", insertbackground="#00ff00", wrap=tk.WORD, borderwidth=0)
    output_box.pack(padx=15, pady=10)

    # Image preview label
    image_label = tk.Label(root, bg="#0d0d0d", width=150, height=150)
    image_label.pack(pady=10)

    # Text styling
    output_box.tag_configure('bold_green', foreground="#00ff00", font=("Courier New", 10, "bold"))
    output_box.tag_configure('warning', foreground="#ff0000")
    output_box.tag_configure('normal', foreground="#00ff00")

    root.mainloop()

# Launch
if __name__ == "__main__":
    run_gui()
