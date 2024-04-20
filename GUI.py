import tkinter as tk
from speech_recog import speech_to_text, text_to_speech

def button1_command():
    
    new_window = tk.Toplevel(window)
    new_window.title("Response Window")

    text_box = tk.Entry(new_window)
    text_box.pack(pady=10)

    def store_text_command():
        entered_text = text_box.get()
        result_label.config(text=f"You entered: {entered_text}")

    store_button = tk.Button(new_window, text="Enter", command=store_text_command)
    store_button.pack(pady=10)

    result_label = tk.Label(new_window, text="Waiting for you")
    result_label.pack(pady=10)

def button2_command():
    new_window = tk.Toplevel(window)
    new_window.title("Response Window")

    

    def store_speak_command():
        text_to_speech("You may speak now")
        
        spoken = speech_to_text()
        user_label.config(text=f"You entered: {spoken}")

    store_button = tk.Button(new_window, text="speak", command=store_speak_command)
    store_button.pack(pady=10)

    user_label = tk.Label(new_window, text="")
    user_label.pack(pady=10)
    
    result_label = tk.Label(new_window, text="Waiting for you")
    result_label.pack(pady=10)

# Create the main window
window = tk.Tk()
window.title("Button Example")

# Create buttons
button1 = tk.Button(window, text="Writing Bot", command=button1_command)
button2 = tk.Button(window, text="Speaking Bot", command=button2_command)

# Create a label to display the result
label = tk.Label(window, text="Which bot do you want?")

# Pack the widgets into the window
button1.pack(pady=10)
button2.pack(pady=10)
label.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()
