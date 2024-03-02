'''

TODO:

    - Reconfigure the deletion and recreation of the reset and settings buttons due to the change to using pack.
    - Modify the snipping overlay to closer resemble the original snipping tool (with a hole in the overlay).

'''



import tkinter as tk
import customtkinter as ctk
from PIL import ImageGrab, Image
import io
import base64
import requests
import os
from threading import *
import pyaudio
import soundfile as sf
import dotenv
import numpy as np



class SnippingTool(ctk.CTk):

    def __init__(self):
        '''Class Initialization'''

        # Initialize the parent class (ctk.CTk)
        super().__init__()

        # Set and load config.env for environment variables
        dotenv_file = dotenv.find_dotenv(filename='config.env')
        dotenv.load_dotenv(dotenv_file)

        # Set the appearance mode and default color theme (from config.env)
        ctk.set_appearance_mode(os.environ['appearanceMode'])
        ctk.set_default_color_theme(os.environ['colorTheme'])

        # Set the title, icon, and geometry of the window
        self.title("Smart Snipping Tool")
        self.iconbitmap(os.environ['icon'])
        self.geometry("300x100")

        # Set the window to be always on top
        self.attributes("-topmost", True)

        # Create a frame to hold snip_button, send_to_gpt4_button, and generate_TTS_button
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a button to start the snipping process
        self.snip_button = ctk.CTkButton(self.button_frame, text="New Snip", command=self.start_snipping)
        self.snip_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create a flag to stop the audio stream
        self.streamStop = False









    def start_snipping(self):
        '''Start the snipping process'''

        # Hide the window
        self.withdraw()

        # Call create_overlay() to create the overlay
        self.create_overlay()




    def create_overlay(self):
        '''Create the overlay for the snipping process'''

        # Create a new Toplevel window for the overlay
        self.overlay = tk.Toplevel(self)

        # Make the overlay window fullscreen, transparent, and always on top
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.4)  # Adjust transparency here
        self.overlay.attributes("-topmost", True)

        # Create a canvas to draw the snip on
        self.canvas = tk.Canvas(self.overlay, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)



        # ----- Bind mouse events to snip functions -----

        # Left click to start snipping
        self.canvas.bind('<Button-1>', self.on_canvas_click)

        # Left drag to draw the snip
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)

        # Left release to end snipping
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)

        # Click 'Escape' to cancel snipping
        self.overlay.bind('<Escape>', self.cancel_snipping)





    def on_canvas_click(self, event):
        '''Initialize the starting coordinates of the snip'''

        # Save the starting coordinates of the snip
        self.x1 = event.x_root
        self.y1 = event.y_root

        # Create a rectangle to draw the snip
        self.snip_rect = self.canvas.create_rectangle(self.x1, # Initialize the top left x coordinate
                                                      self.y1, # Initialize the top left y coordinate
                                                      self.x1, # Initialize the bottom right x coordinate
                                                      self.y1, # Initialize the bottom right y coordinate
                                                      outline='white', width=2  # Set the outline color and width
                                                      )





    def on_canvas_drag(self, event):
        '''Update the coordinates of the snip and resize the rectangle as the mouse is dragged'''

        # Save the current coordinates of the snip (the mouse coordinates)
        self.x2 = event.x_root
        self.y2 = event.y_root

        # Update the coordinates of the snip rectangle
        self.canvas.coords(self.snip_rect,
                           self.x1,
                           self.y1,
                           self.x2, # Update the bottom right x coordinate
                           self.y2  # Update the bottom right y coordinate
                           )



    def on_canvas_release(self, event):
        '''End the snipping process when the mouse is released'''

        # Destroy the overlay
        self.overlay.destroy()

        # Call take_screenshot() to take a screenshot of the snip using the current coordinates
        self.take_screenshot()

        # Call main_window() to create the main window
        self.main_window()





    def cancel_snipping(self, event=None):
        '''Cancel the snipping process'''

        # Destroy the overlay
        self.overlay.destroy()

        # Call deiconify() to show the main window again (un-withdraw it)
        self.deiconify()









    def take_screenshot(self):
        '''Take a screenshot of the snip using the current coordinates'''

        # Ensure the top-left and bottom-right coordinates are correctly ordered
        x1, y1 = min(self.x1, self.x2), min(self.y1, self.y2)
        x2, y2 = max(self.x1, self.x2), max(self.y1, self.y2)

        # Take a screenshot of the selected snip area
        self.screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))








    def main_window(self):
        '''Create the main window after the snipping process is complete'''

        # Update the window size
        self.geometry("400x500")


        # ----- Textbox default text handling -----

        def handle_focus_in(_):
            '''If the textbox is selected, delete the default text and change the text color'''
            if self.query_entry.get() == defaultText:
                self.query_entry.delete(0, ctk.END)

            if ctk.get_appearance_mode() == 'Dark':
                self.query_entry.configure(text_color='white')
            elif ctk.get_appearance_mode() == 'Light':
                self.query_entry.configure(text_color='black')

        def handle_focus_out(_):
            '''If the textbox is deselected, insert the default text (if empty) and change the text color'''
            if len(self.query_entry.get())==0:
                self.query_entry.delete(0, ctk.END)
                self.query_entry.configure(text_color='grey')
                self.query_entry.insert(0, defaultText)

        def handle_enter(txt):
            '''If the enter key is pressed, submit the text to gpt_threading()'''
            self.focus()
            self.gpt_threading()

        # ------------------------------------------



        # Create a frame and the contained widgets, only if they don't already exist (to prevent duplicates)
        if not hasattr(self, 'output_frame'):

            # Create a frame to hold the output widgets
            self.output_frame = ctk.CTkFrame(self)
            self.output_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

            # Create a frame to hold reset, settings, and entry label
            self.settings_frame = ctk.CTkFrame(self.output_frame)
            self.settings_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

            # Create settings button
            self.settings = ctk.CTkButton(self.settings_frame, text="Settings", width=18, height=10, border_width=0, command=self.settings_window)
            self.settings.pack(side=tk.RIGHT, padx = 5, pady=5)

            # Create reset button
            self.reset_button = ctk.CTkButton(self.settings_frame, text="Reset", width=18, height=10, border_width=0, command=self.reset_app)
            self.reset_button.pack(side=tk.LEFT, padx = 5, pady = 5)

            # Create a label to function as the entry title
            self.entry_label = ctk.CTkLabel(self.settings_frame, text="Enter your question:", font=("", 15, 'bold','italic'))
            self.entry_label.pack(side=tk.TOP, padx=5, pady=5)

            # Create an entry field to enter the question, and set the default text
            defaultText = "What is in this image?"
            self.query_entry = ctk.CTkEntry(self.output_frame, text_color='grey')
            self.query_entry.pack(side=ctk.TOP, fill=ctk.X, padx=5, pady=(0, 5))
            self.query_entry.insert(0, defaultText)
            self.query_entry.bind("<FocusIn>", handle_focus_in)
            self.query_entry.bind("<FocusOut>", handle_focus_out)
            self.query_entry.bind("<Return>", handle_enter)


            # Create a frame to hold the response widgets
            self.response_frame = ctk.CTkFrame(self.output_frame)
            self.response_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=15, pady=15, expand=True)

            # Create a textbox to display the response
            self.textbox = ctk.CTkTextbox(self.response_frame, width=350, height=100, wrap='word', state="disabled")
            self.textbox.pack(fill=tk.BOTH)

            # Create a button to send the response to GPT-4V API
            self.send_to_gpt4_button = ctk.CTkButton(self.button_frame, text="Send", command=self.gpt_threading)
            self.send_to_gpt4_button.pack(side=tk.LEFT, padx=5, pady=5)

            # Create a button to send the response to OpenAI's TTS API
            self.generate_TTS_button = ctk.CTkButton(self.button_frame, text="TTS", width=10, state=ctk.DISABLED, command=self.tts_threading)
            self.generate_TTS_button.pack(side=tk.LEFT, padx=5, pady=5)

            # Create a label to hold the image
            self.image_label = ctk.CTkLabel(self, text="")
            self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        # Create a thumbnail of the screenshot
        self.create_thumbnail()

        # Display the resized thumbnail in the main window (Update the image_label)
        self.image_label.configure(image=self.thumbnail)
        self.image_label.image = self.thumbnail  # Keep reference to avoid garbage-collection


        # Call deiconify() to show the main window again (un-withdraw it)
        self.deiconify()





    def create_thumbnail(self):
        '''Create a thumbnail of the screenshot to display in the main window'''

        # Resize the image to fit within the maximum dimensions (400x400)
        max_size = (400, 400)
        thumbnail_image = self.screenshot.copy()
        thumbnail_image.thumbnail(max_size, Image.LANCZOS)

        # Convert PIL Image to CTkImage (with size adjustment if necessary)
        screenshot_width, screenshot_height = thumbnail_image.size
        self.thumbnail = ctk.CTkImage(light_image=thumbnail_image, size=(screenshot_width, screenshot_height))



    def change_env_value(self, variable, newValue):
        '''Modify config.env to permanently change the value of a variable'''
        dotenv_file = dotenv.find_dotenv(filename='config.env')
        dotenv.load_dotenv(dotenv_file)
        os.environ[variable] = newValue
        dotenv.set_key(dotenv_file, variable, os.environ[variable])



    def settings_window(self):
        '''Open the settings window'''

        def change_appearance_mode_event(new_appearance_mode: str):
            '''Modify config.env to permanently change the appearance mode'''
            ctk.set_appearance_mode(new_appearance_mode)
            self.change_env_value('appearanceMode', new_appearance_mode)

        def change_theme_event(new_theme: str):
            '''Modify config.env to permanently change the theme'''
            #ctk.set_default_color_theme(themeDict[new_theme])
            self.change_env_value('colorTheme', themeDict[new_theme])

        def save_API_key(new_API: str):
            '''Modify config.env to permanently change the API key'''
            self.change_env_value('API_KEY', new_API)

        def change_TTS_voice_event(new_tts_voice: str):
            '''Modify config.env to permanently change the TTS voice'''
            self.change_env_value('TTSVoice', new_tts_voice)

        def change_TTS_model_event(new_tts_model: str):
            '''Modify config.env to permanently change the TTS model'''
            self.change_env_value('TTSModel', new_tts_model)


        # Create a dictionary to hold theme translations
        themeDict = {
            'blue': 'blue',
            'dark-blue': 'dark-blue',
            'green': 'green',
            'coffee': 'themes/coffee.json',
            'violet': 'themes/violet.json',
            'metal': 'themes/metal.json',
            'red': 'themes/red.json',
            'marsh': 'themes/marsh.json',
            'pink': 'themes/pink.json',
            'carrot': 'themes/carrot.json',
            'sky': 'themes/sky.json',
            'rose': 'themes/rose.json'
        }


        # Withdraw the main window to hide it
        self.withdraw()

        # Create the settings window
        self.settings = ctk.CTkToplevel(self)
        self.settings.attributes("-topmost", True)
        self.settings.title("Settings")
        self.settings.geometry("300x390")

        # Set the icon for the settings window (Must set a delay due to customtkinter bug with CTkToplevel)
        self.settings.after(190, lambda: self.settings.iconbitmap(os.environ['icon']))

        # Ensure the settings window appears on top and receives immediate focus
        self.settings.focus_force()


        # Create a frame that will hold all settings
        self.settings.settings_frame = ctk.CTkFrame(self.settings)
        self.settings.settings_frame.pack(fill=tk.BOTH, padx=5, pady=5)


        # Create API key label, entry, and save button within its own frame
        self.settings.API_key_label = ctk.CTkLabel(self.settings.settings_frame, text="\nOpenAI API Key")
        self.settings.API_key_label.pack(padx=5, pady=2)

        self.settings.settings_frame.API_frame = ctk.CTkFrame(self.settings.settings_frame)
        self.settings.settings_frame.API_frame.pack(fill=tk.X, padx=5, pady=5)

        self.settings.API_key_entry = ctk.CTkEntry(self.settings.settings_frame.API_frame)
        self.settings.API_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.settings.API_key_entry.insert(0, os.environ['API_KEY'])

        self.settings.API_key_save = ctk.CTkButton(self.settings.settings_frame.API_frame, text="Save", width=10,
                                                   command=lambda: save_API_key(self.settings.API_key_entry.get()))
        self.settings.API_key_save.pack(side=tk.RIGHT, padx=5, pady=5)


        # Create drop-down to choose appearance mode
        self.settings.appearance_mode_label = ctk.CTkLabel(self.settings.settings_frame, text="\nAppearance Mode")
        self.settings.appearance_mode_label.pack(padx=5, pady=2)
        self.settings.appearance_mode_optionmenu = ctk.CTkOptionMenu(self.settings.settings_frame,
                                                                     values=["light", "dark", "system"],
                                                                     command=change_appearance_mode_event)
        self.settings.appearance_mode_optionmenu.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.settings.appearance_mode_optionmenu.set(os.environ['appearanceMode'])


        # Create drop-down to choose theme
        self.settings.theme_label = ctk.CTkLabel(self.settings.settings_frame, text="\nTheme (requires restart)")
        self.settings.theme_label.pack(padx=5, pady=2)
        self.settings.theme_optionmenu = ctk.CTkOptionMenu(self.settings.settings_frame,
                                                           values=['blue', 'dark-blue', 'green', 'coffee', 'violet', 'metal', 'red', 'marsh', 'pink', 'carrot', 'sky', 'rose'],
                                                           command=change_theme_event)
        self.settings.theme_optionmenu.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.settings.theme_optionmenu.set(list(filter(lambda x: themeDict[x] == os.environ['colorTheme'], themeDict))[0])


        # Create drop-down to choose TTS voice
        self.settings.TTS_voice_label = ctk.CTkLabel(self.settings.settings_frame, text="\nTTS Voice")
        self.settings.TTS_voice_label.pack(padx=5, pady=2)
        self.settings.TTS_voice_optionmenu = ctk.CTkOptionMenu(self.settings.settings_frame,
                                                                     values=["onyx", "alloy", "echo", "fable", "nova", "shimmer"],
                                                                     command=change_TTS_voice_event)
        self.settings.TTS_voice_optionmenu.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.settings.TTS_voice_optionmenu.set(os.environ['TTSVoice'])


        # Create drop-down to choose TTS Model
        self.settings.TTS_model_label = ctk.CTkLabel(self.settings.settings_frame, text="\nTTS Model")
        self.settings.TTS_model_label.pack(padx=5, pady=2)
        self.settings.TTS_model_optionmenu = ctk.CTkOptionMenu(self.settings.settings_frame,
                                                               values=["tts-1", "tts-1-hd"],
                                                               command=change_TTS_model_event)
        self.settings.TTS_model_optionmenu.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.settings.TTS_model_optionmenu.set(os.environ['TTSModel'])



        # Bind the settings window destroy event to a method
        self.settings.protocol("WM_DELETE_WINDOW", self.on_settings_close)



    def on_settings_close(self):
        '''Close the settings window and show the main window'''

        # Deiconify (show) the main window
        self.deiconify()

        # Destroy the settings window
        self.settings.destroy()




    def reset_app(self):
        '''Reset the app to its initial state (minimize)'''

        # Destroy the overlay if it exists
        if self.overlay:
            self.overlay.destroy()

        # Destroy the image label if it exists
        if self.image_label:
            self.image_label.destroy()

        # Destroy the output frame and its widgets if they exist
        if hasattr(self, 'output_frame'):
            self.output_frame.destroy()
            del self.output_frame  # Use del to remove the attribute

        # Destroy the send_to_gpt4_button if it exists
        if hasattr(self, 'send_to_gpt4_button'):
            self.send_to_gpt4_button.destroy()

        # Destroy the generate_TTS_button if it exists
        if hasattr(self, 'generate_TTS_button'):
            self.generate_TTS_button.destroy()

        # Revert window to the initial size and bring it back to focus
        self.geometry("300x100")
        self.deiconify()


    def button_states(self, buttonName, state):
        '''Change the button state ('normal' <=> 'disabled'), for buttons that have a bug.'''
        # When enabling and disabling some buttons, the button becomes malformed and causes undefined behaviour. .after() appears to solve this issue.

        if buttonName == 'reset_button':
            if state == 'disabled':
                self.after(25, lambda: (self.reset_button.configure(state=ctk.DISABLED)))
            elif state == 'normal':
                self.after(25, lambda: (self.reset_button.configure(state=ctk.NORMAL)))
            else:
                print("Incorrect state provided.")

        elif buttonName == 'generate_TTS_button':
            if state == 'disabled':
                self.after(25, lambda: (self.generate_TTS_button.configure(state=ctk.DISABLED)))
            elif state == 'normal':
                self.after(25, lambda: (self.generate_TTS_button.configure(state=ctk.NORMAL)))
            else:
                print("Incorrect state provided.")

        else:
            print("Incorrect button name provided.")




    def gpt_threading(self):
        '''Create a thread to send the image to send_to_gpt4()'''

        GPT = Thread(target=self.send_to_gpt4)
        GPT.start()



    def send_to_gpt4(self):
        '''Send the image and prompt to GPT-4V API'''

        # Disable the "Send to GPT-4" button while processing the request
        self.send_to_gpt4_button.configure(state=ctk.DISABLED)

        # Disable other buttons
        self.snip_button.configure(state=ctk.DISABLED)

        # Use button_states to disable the button, preventing bug
        self.button_states('reset_button', 'disabled')

        # Delete and re-create the generate_TTS_button to disable it (re-creation is required until I find a better solution that doesn't result in bugs when the button is disabled)
        self.button_states('generate_TTS_button', 'disabled')


        self.display_response("processing...")

        # Convert the image to a  base64 string
        img_byte_arr = io.BytesIO()                                    # Create a byte array in memory
        self.screenshot.save(img_byte_arr, format='JPEG')              # Use 'JPEG' format for base64 encoding
        img_byte_arr = img_byte_arr.getvalue()                         # Save the byte array as a value
        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')  # Convert image to base64

        # Get the user input text
        user_input_text = self.query_entry.get()


        # Create the headers for the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['API_KEY']}"
        }

        # Create the JSON payload
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_input_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }

        # Send the request to the GPT-4V API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:

            # Get the response text from the JSON response
            result = response.json().get('choices', [])[0].get('message', {}).get('content', '')

            # After getting the response re-enable the "Send to GPT-4" and "TTS" buttons
            self.send_to_gpt4_button.configure(state=ctk.NORMAL)
            self.button_states('generate_TTS_button', 'normal')

            # Enable other buttons
            self.snip_button.configure(state=ctk.NORMAL)

            # Use button_states to enable the button, preventing bug
            self.button_states('reset_button', 'normal')

            # Display the response in the textbox
            self.display_response(result)

        # If the request was unsuccessful
        else:

            # After getting the response re-enable the "Send to GPT-4" button
            self.send_to_gpt4_button.configure(state=ctk.NORMAL)

            # Enable other buttons
            self.snip_button.configure(state=ctk.NORMAL)

            # Use button_states to enable the button, preventing bug
            self.button_states('reset_button', 'normal')

            # Display the response in the textbox
            self.display_response("Error: "+ str(response.status_code) + response.text)




    def tts_threading(self):
        '''Create a thread to send the response to streamed_audio()'''

        TTS = Thread(target=self.streamed_audio, args=(self.textbox.get(1.0, tk.END),))
        TTS.start()



    def streamed_audio(self, input_text):
        '''Send the response to OpenAI's TTS API and stream the audio'''

        def create_delayed_button():
            '''create a delayed button to prevent a bug where the button is destroyed before it is created (temporary solution)'''

            self.generate_TTS_button = ctk.CTkButton(self.button_frame, fg_color='red', hover_color='darkred', text="TTS", width=10, state=ctk.NORMAL, command=self.cancelAudio)
            self.generate_TTS_button.pack(side=tk.LEFT, padx=5, pady=5)



        # Change the button color to red, and change the command to cancelAudio() (Save the original colors)
        fgcolor = self.generate_TTS_button.cget("fg_color")
        hovercolor = self.generate_TTS_button.cget("hover_color")


        # Delete and re-create the generate_TTS_button to modify it (re-creation is required until I find a better solution that doesn't result in bugs when the button is modified)
        if hasattr(self, 'generate_TTS_button'):
            # Delay the destruction of the button to prevent a bug where the button is destroyed before it is created
            self.after(25, self.generate_TTS_button.destroy)
            self.after(25, create_delayed_button)


        # Disable all other buttons until the audio stream ends, or is canceled
        self.send_to_gpt4_button.configure(state=ctk.DISABLED)
        self.snip_button.configure(state=ctk.DISABLED)

        # Use button_states to disable the button, preventing bug
        self.button_states('reset_button', 'disabled')


        # OpenAI API endpoint and parameters
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {os.environ['API_KEY']}",
        }
        payload = {
            "model": os.environ['TTSModel'],
            "input": input_text,
            "voice": os.environ['TTSVoice'],
            "response_format": "opus",
        }


        audio = pyaudio.PyAudio()

        # Get the audio format from the OpenAI response
        def get_pyaudio_format(subtype):
            if subtype == 'PCM_16':
                return pyaudio.paInt16
            return pyaudio.paInt16


        with requests.post(url, headers=headers, json=payload, stream=True) as response:

            # If the request was successful, create a buffer to hold the streamed audio
            if response.status_code == 200:

                buffer = io.BytesIO()
                for chunk in response.iter_content(chunk_size=4096):
                    buffer.write(chunk)

                buffer.seek(0)

                # Create a sound file from the response
                with sf.SoundFile(buffer, 'r') as sound_file:

                    format = get_pyaudio_format(sound_file.subtype)
                    channels = sound_file.channels
                    rate = sound_file.samplerate

                    # Create a stream to play the audio
                    stream = audio.open(format=format, channels=channels, rate=rate, output=True)
                    chunk_size = 1024
                    data = sound_file.read(chunk_size, dtype='int16')

                    # Play the audio
                    while len(data) > 0:

                        stream.write(data.tobytes())
                        data = sound_file.read(chunk_size, dtype='int16')

                        if self.streamStop:
                            break

                    # Close the stream
                    stream.stop_stream()
                    stream.close()
                    self.streamStop = False

            # If the request was unsuccessful
            else:
                #print(f"Error: {response.status_code} - {response.text}")
                pass

            # Close the audio object
            audio.terminate()

            # Change generate_TTS_button back to it's initial state
            # Delete and re-create the generate_TTS_button to modify it (re-creation is required until I find a better solution that doesn't result in bugs when the button is modified)
            if hasattr(self, 'generate_TTS_button'):
                self.generate_TTS_button.destroy()
                self.generate_TTS_button = ctk.CTkButton(self.button_frame, text="TTS", fg_color=fgcolor, hover_color=hovercolor, width=10, state=ctk.NORMAL, command=self.tts_threading)
                self.generate_TTS_button.pack(side=tk.LEFT, padx=5, pady=5)

            # Enable all other buttons after the audio stream stops
            self.send_to_gpt4_button.configure(state=ctk.NORMAL)
            self.snip_button.configure(state=ctk.NORMAL)

            # Use button_states to enable the button, preventing bug
            self.button_states('reset_button', 'normal')



    def cancelAudio(self):
        '''Cancel the audio stream (change the streamStop flag to True)'''

        self.streamStop = True




    def display_response(self, response_text):
        '''Display the response in the textbox'''

        self.textbox.configure(state='normal')           # Enable the textbox to clear it
        self.textbox.delete("1.0", tk.END)         # Clear current text
        self.textbox.insert("1.0", response_text)   # Insert the response text
        self.textbox.configure(state="disabled")         # Disable the textbox to make it read-only


if __name__ == "__main__":
    app = SnippingTool()
    app.mainloop()