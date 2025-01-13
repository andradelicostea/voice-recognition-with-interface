import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import threading
from PIL import Image, ImageTk, ImageDraw

class VoiceToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recunoaștere Vocală în Timp Real")
        self.root.geometry("800x500")
        
        # Titlul aplicației
        self.label = tk.Label(self.root, text="Aplicatie de Recunoastere Vocala", font=("Cooper Black", 16))
        self.label.pack(pady=10)
        
        # Câmp de text pentru afișarea transcrierii
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 12), height=15, width=70)
        self.text_area.pack(pady=10)
        self.text_area.insert(tk.END, "Apăsați Start pentru a începe recunoașterea vocală...\n")
        
        # Butoanele Start și Stop
        self.start_button = tk.Button(self.root, text="Start", command=self.start_recognition, font=("Cooper Black", 12), bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recognition, font=("Cooper Black", 12), bg="red", fg="white")
        self.stop_button.pack(side=tk.RIGHT, padx=10)
        self.stop_button.config(state=tk.DISABLED)  # Dezactivează inițial butonul Stop
        
        # Flag pentru controlul recunoașterii
        self.recognizing = False

        # Imagine rotundă
        self.circular_image = self.create_circular_image(r"C:\Users\Andra\Desktop\fac- an 4 sem 1\iom\proiect\pisi.jpg", size=(50, 50))

    def create_circular_image(self, image_path, size=(50, 50)):
        """Transformă o imagine într-una rotundă."""
        img = Image.open(image_path).resize(size, Image.ANTIALIAS)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        rounded_img = Image.new("RGBA", size)
        rounded_img.paste(img, (0, 0), mask)
        return ImageTk.PhotoImage(rounded_img)

    def start_recognition(self):
        """Pornește recunoașterea vocală."""
        self.display_text_with_image("Ascult... Vorbiți acum!")
        self.start_button.config(state=tk.DISABLED)  # Dezactivează butonul Start
        self.stop_button.config(state=tk.NORMAL)    # Activează butonul Stop
        self.recognizing = True
        threading.Thread(target=self.voice_to_text, daemon=True).start()  # Rulează într-un thread separat

    def stop_recognition(self):
        """Oprește recunoașterea vocală."""
        self.recognizing = False
        self.display_text_with_image("Recunoașterea a fost oprită.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def voice_to_text(self):
        """Funcția de recunoaștere vocală."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Ajustează zgomotul de fundal
            while self.recognizing:
                try:
                    # Ascultă vocea utilizatorului
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio, language="ro-RO")  # Recunoaștere în limba română
                    self.display_text_with_image(f"Text recunoscut: {text}")
                except sr.UnknownValueError:
                    self.display_text_with_image("Nu am înțeles. Încercați din nou!")
                except sr.RequestError as e:
                    self.display_text_with_image(f"Eroare de conexiune: {e}")
                except Exception as ex:
                    self.display_text_with_image(f"Eroare: {str(ex)}")

    def display_text_with_image(self, text):
        """Afișează textul recunoscut alături de o imagine."""
        frame = tk.Frame(self.text_area, pady=2)
        # Adaugă imaginea la fiecare mesaj
        tk.Label(frame, image=self.circular_image).pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text=text, font=("Arial", 12), wraplength=550, justify="left").pack(side=tk.LEFT)
        self.text_area.window_create(tk.END, window=frame)
        self.text_area.insert(tk.END, "\n")
        self.text_area.see(tk.END)  # Derulează automat la final

# Rulează aplicația
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceToTextApp(root)
    root.mainloop()
