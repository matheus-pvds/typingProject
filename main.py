from calendar import c
import random as r
from turtle import listen

import customtkinter as ctk
from turtledemo.penrose import star

class MyFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.PADX = 5
        self.PADY = 5
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        self.pack(padx=self.PADX, pady=self.PADY)
        self.start_button()
        self.add_text_field("Welcome to typemaster!", "Press start for quote and spacebar to start typing...")
        self.enable_spacebar()

    #TODO: Extract text from randomly extracted passages
    def extract_text_from_passage(self):
        with open("passages.txt", "r", encoding="ansi") as file:
            passages = file.readlines()
        # Randomly select a passage
        passage = r.choice(passages)
        #Extract only the quote (text between the quotation marks) from the passage and exhibit the author (after the dash)
        quote = passage.split('"')[1] if '"' in passage else ""
        author = passage.split('-')[-1].strip() if '-' in passage else ""
        return quote, author
    
    def listen_for_spacebar(self, event):
        if event.keysym == "space":
            # Extract text from the passage
            extracted_text = self.extract_text_from_passage()
            # Compare extracted text with the text in the text field
            self.compare_text(extracted_text)

    def compare_text(self, extracted_text):
        # Get the text from the text field
        text_field_text = self.entry.get()
        # Compare the extracted text with the text in the text field
        if extracted_text == text_field_text:
            # If the texts match, go to the next word in the passage and update the text field
            self.update_text_field()
        else:
            # If the texts do not match, change the color of the text to red and disable spacebar until corrected
            self.entry.configure(fg_color="red")
            self.disable_spacebar()
            self.enable_backspace()
            return None

    def enable_backspace(self):
        self.entry.bind("<BackSpace>", self.listen_for_backspace)

    def listen_for_backspace(self, event):
        if event.keysym == "BackSpace":
            self.compare_text(self.extract_text_from_passage())
            # Re-enable spacebar when backspace is pressed
            self.enable_spacebar()
            # Reset the text color to default
            self.entry.configure(fg_color="white")

            
    def update_text_field(self):
        # Get the next word in the passage and update the text field
        next_word = self.get_next_word()
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, next_word)
        # Re-enable spacebar
        self.enable_spacebar()

    def get_next_word(self):
        # Get the current text in the text field
        current_text = self.entry.get()
        # Split the current text into words
        words = current_text.split()
        # Get the next word in the passage
        next_word = words[1] if len(words) > 1 else ""
        return next_word

    def disable_spacebar(self):
        self.entry.unbind("<space>")

    def enable_spacebar(self):
        self.entry.bind("<space>", self.listen_for_spacebar)

    def add_text_field(self, label_text, placeholder_text):
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.grid(row=0, column=0, columnspan=2, padx=self.PADX, pady=self.PADY)

        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder_text)
        self.entry.grid(row=1, column=0, columnspan=2, padx=self.PADX, pady=self.PADY)

    def start_button(self):
        self.start_button_ = ctk.CTkButton(self, text="Start", command=self.update_text_label)
        self.start_button_.grid(row=2, column=0, columnspan=2, padx=self.PADX, pady=self.PADY)

    def update_text_label(self):
        #Extract text from passage
        extracted_text, author = self.extract_text_from_passage()
        self.label.configure(text=extracted_text + " - " + author)
        #Extract each word from quote and update the label with the first word
        word_by_word = extracted_text.split()
        self.next_word_index = nwi = 0
        self.label.configure(text=word_by_word[nwi])
        #In next call update with the next word in the quote
        self.next_word_index = 1

        

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter Example")
        self.geometry("800x600")

        self.frame = MyFrame(self)
        self.frame.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()