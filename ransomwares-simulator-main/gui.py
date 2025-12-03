
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\inter\OneDrive\Desktop\ransomeware\images")



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def decryption_key():
    pass


window = Tk()

window.geometry("857x390")
window.configure(bg = "#FF727A")


canvas = Canvas(window,bg = "#FF727A",height = 390,width = 857,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
    
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(428.0,195.0,image=image_image_1)

canvas.create_text(192.0,15.0,anchor="nw",text="Pandora Box\n",fill="#000000",font=("InknutAntiqua Bold", 64 * -1))

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(325.5,222.5,image=entry_image_1)
entry_1 = Entry(bd=0,bg="#D9D9D9",fg="#000716",highlightthickness=0)
entry_1.place(x=29.0,y=195.0,width=593.0,height=53.0)

canvas.create_text(24.0,142.0,anchor="nw",text="Enter The Key",fill="#000000",font=("Inika Bold", 32 * -1))

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=decryption_key,relief="flat")
button_1.place(x=29.0,y=290.0,width=246.0,height=51.0)
window.resizable(False, False)
window.mainloop()
