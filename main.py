import random as r
import customtkinter as ctk

class MyFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.PADX = 5
        self.PADY = 5
        self.grid_columnconfigure((0,1), weight=1)
        #self.grid_rowconfigure((0,1), weight=1)
        self.pack(padx=self.PADX, pady=self.PADY)
        self.start_button()
        self.add_text_field("Welcome to TypeMaster!", "Press start for quote and spacebar to start typing...")
        self.spacebar_on_off(switch="on")
        self.enable_backspace()

    def add_text_field(self, label_text, placeholder_text):
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.grid(row=0, column=0, columnspan=2, padx=self.PADX, pady=self.PADY)

        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder_text)
        self.entry.grid(row=1, column=0, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="ew")
    
    def start_button(self):
        self.start_button_ = ctk.CTkButton(self, text="Start", command=self.start_typing)
        self.start_button_.grid(row=2, column=0, columnspan=2, padx=self.PADX, pady=self.PADY)

    def start_typing(self):
        self.extract_text_from_passage()
        self.generator = self.get_next_word()
        self.update_text_label()

    def extract_text_from_passage(self):
        with open("passages.txt", "r", encoding="utf-8") as file:
            passages = file.readlines()
        # Randomly select a passage
        passage = r.choice(passages)
        #Extract only the quote (text between the quotation marks) from the passage and exhibit the author (after the dash)
        self.quote = passage.split('"')[1] if '"' in passage else ""
        self.author = passage.split('-')[-1].strip() if '-' in passage else ""
        self.words = self.quote.split()
    
    def spacebar_press(self, event):
        # Compare extracted text with the text in the text field
        self.compare_text()

    def spacebar_on_off(self, switch):
        if switch=="on":
            self.entry.bind("<space>", self.spacebar_press)
        elif switch=="off":
            self.entry.unbind("<space>")

    def compare_text(self, event=None):
        text_field_text = self.entry.get().strip()
        text_minus_space = text_field_text[:-1]  # Get the text up to the last character (excluding the space)
        # If the texts match, change the color of the text to white and enable spacebar
        if self.next_word == text_field_text:
            self.entry.configure(fg_color="green")
            self.spacebar_on_off(switch="on")
            self.update_text_field()
            self.update_text_label()
        elif self.next_word.startswith(text_field_text) or self.entry.get()=="":
            self.entry.configure(fg_color="gray")
            self.spacebar_on_off(switch="on")
        elif self.next_word.startswith(text_field_text) or self.next_word != text_field_text:
        # If the texts do not match, change the color of the text to red and disable spacebar until corrected
            self.entry.configure(fg_color="red")
            self.spacebar_on_off(switch="off")
            self.enable_backspace()

    def backspace_press(self, event):
        # Compare extracted text with the text in the text field
        self.compare_text()

    def enable_backspace(self):
        self.entry.bind("<BackSpace>", self.backspace_press)
            
    def update_text_field(self):
        # delete the current text in the text field
        self.entry.delete(0, "end")
        # Re-enable spacebar
        self.spacebar_on_off(switch="on")

    def get_next_word(self):
        for word in self.words:
            yield word

    def update_text_label(self):
        # Update the text label with the next word in the passage
        self.next_word = next(self.generator, "")
        self.label.configure(text=self.next_word)

        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TypeMaster")
        self.geometry("800x600")

        self.frame = MyFrame(self)
        self.frame.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()