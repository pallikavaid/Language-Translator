"""
Language Translator

A desktop application built with Python and Tkinter that translates text
between multiple languages using Google Translate.

Features
--------
• Multi-language translation
• Auto language detection
• Copy translated text
• Clear input/output
• Text-to-speech
• Keyboard shortcuts
• Responsive GUI using multithreading

Author: Pallika Vaid
GitHub: https://github.com/pallikavaid
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pyttsx3

from deep_translator import GoogleTranslator
from PIL import Image, ImageTk


# Supported language names mapped to Google Translate language codes.
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "Turkish": "tr",
    "Dutch": "nl",
}


class TranslatorApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Language Translator")
        self.root.geometry("700x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f4")

        # ------------------------------
        # Load Application Icon
        # ------------------------------
        try:
            icon = Image.open("assets/icon.png")
            icon = ImageTk.PhotoImage(icon)
            self.root.iconphoto(False, icon)

            # Prevent garbage collection
            self.root.icon_image = icon

        except Exception as e:
            print(e)

        # ------------------------------
        # Text-to-Speech Engine
        # ------------------------------
        self.tts_engine = pyttsx3.init()

        # Build Interface
        self._build_ui()

        # Keyboard Shortcuts
        self.root.bind("<Control-Return>", self.translate_shortcut)
        self.root.bind("<Escape>", self.clear_shortcut)

    # ==========================================================
    # USER INTERFACE
    # ==========================================================

    def _build_ui(self):

        title = tk.Label(
            self.root,
            text="🌍 Language Translator",
            font=("Segoe UI Variable", 22, "bold"),
            bg="#f4f4f4",
            fg="#1f2937"
        )
        title.pack(pady=(20, 15))

        # ------------------------------
        # Language Selection
        # ------------------------------

        lang_frame = tk.Frame(
            self.root,
            bg="#f4f4f4"
        )

        lang_frame.pack(pady=10)

        self.source_lang = tk.StringVar(value="Auto Detect")
        self.target_lang = tk.StringVar(value="English")

        tk.Label(
            lang_frame,
            text="From",
            font=("Segoe UI", 10),
            bg="#f4f4f4"
        ).grid(row=0, column=0, padx=8)

        self.source_menu = ttk.Combobox(
            lang_frame,
            textvariable=self.source_lang,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=18
        )

        self.source_menu.grid(
            row=0,
            column=1,
            padx=8
        )

        swap_btn = tk.Button(
            lang_frame,
            text="⇄",
            width=3,
            cursor="hand2",
            command=self.swap_languages,
            font=("Segoe UI", 10, "bold")
        )

        swap_btn.grid(
            row=0,
            column=2,
            padx=10
        )

        tk.Label(
            lang_frame,
            text="To",
            font=("Segoe UI", 10),
            bg="#f4f4f4"
        ).grid(row=0, column=3, padx=8)

        self.target_menu = ttk.Combobox(
            lang_frame,
            textvariable=self.target_lang,
            values=[
                lang
                for lang in LANGUAGES
                if lang != "Auto Detect"
            ],
            state="readonly",
            width=18
        )

        self.target_menu.grid(
            row=0,
            column=4,
            padx=8
        )

        # ------------------------------
        # Input Box
        # ------------------------------

        tk.Label(
            self.root,
            text="Enter Text",
            font=("Segoe UI", 11),
            bg="#f4f4f4"
        ).pack(anchor="w", padx=35)

        self.input_box = tk.Text(
            self.root,
            height=6,
            width=72,
            wrap="word",
            font=("Segoe UI", 11)
        )

        self.input_box.pack(
            padx=30,
            pady=(5, 15)
        )

        # ------------------------------
        # Translate Button
        # ------------------------------

        self.translate_btn = tk.Button(
            self.root,
            text="Translate",
            command=self.start_translation,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8,
            font=("Segoe UI", 11, "bold")
        )

        self.translate_btn.pack(
            pady=(0, 18)
        )
                # ------------------------------
        # Output Box
        # ------------------------------

        tk.Label(
            self.root,
            text="Translation",
            font=("Segoe UI", 11),
            bg="#f4f4f4"
        ).pack(anchor="w", padx=35)

        self.output_box = tk.Text(
            self.root,
            height=6,
            width=72,
            wrap="word",
            font=("Segoe UI", 11),
            bg="#eef2ff",
            state="disabled"
        )

        self.output_box.pack(
            padx=30,
            pady=(5, 18)
        )

        # ------------------------------
        # Bottom Buttons
        # ------------------------------

        button_frame = tk.Frame(
            self.root,
            bg="#f4f4f4"
        )

        button_frame.pack(pady=5)

        copy_btn = tk.Button(
            button_frame,
            text="📋 Copy",
            width=12,
            cursor="hand2",
            command=self.copy_output
        )

        copy_btn.grid(
            row=0,
            column=0,
            padx=8
        )

        clear_btn = tk.Button(
            button_frame,
            text="🗑 Clear",
            width=12,
            cursor="hand2",
            command=self.clear_fields
        )

        clear_btn.grid(
            row=0,
            column=1,
            padx=8
        )

        speak_btn = tk.Button(
            button_frame,
            text="🔊 Listen",
            width=12,
            cursor="hand2",
            command=self.speak_output
        )

        speak_btn.grid(
            row=0,
            column=2,
            padx=8
        )

        # ------------------------------
        # Status Bar
        # ------------------------------

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bg="#f4f4f4",
            fg="gray",
            font=("Segoe UI", 9)
        )

        self.status_label.pack(
            pady=12
        )

    # ==========================================================
    # EVENT HANDLERS
    # ==========================================================

    def translate_shortcut(self, event):
        self.start_translation()

    def clear_shortcut(self, event):
        self.clear_fields()

    def swap_languages(self):

        if self.source_lang.get() == "Auto Detect":
            messagebox.showinfo(
                "Swap Language",
                "Select a source language before swapping."
            )
            return

        source = self.source_lang.get()
        target = self.target_lang.get()

        self.source_lang.set(target)
        self.target_lang.set(source)

    # ==========================================================
    # TRANSLATION
    # ==========================================================

    def start_translation(self):

        text = self.input_box.get(
            "1.0",
            "end"
        ).strip()

        if not text:
            messagebox.showwarning(
                "Empty Input",
                "Please enter text to translate."
            )
            return

        self.translate_btn.config(
            state="disabled",
            text="Translating..."
        )

        self.status_label.config(
            text="Translating..."
        )

        threading.Thread(
            target=self._translate_worker,
            args=(text,),
            daemon=True
        ).start()

    def _translate_worker(self, text):

        try:

            source_code = LANGUAGES[
                self.source_lang.get()
            ]

            target_code = LANGUAGES[
                self.target_lang.get()
            ]

            translated = GoogleTranslator(
                source=source_code,
                target=target_code
            ).translate(text)

            self.root.after(
                0,
                self._show_translation,
                translated
            )

        except Exception as error:

            self.root.after(
                0,
                self._show_error,
                str(error)
            )

    def _show_translation(self, translated):

        self.output_box.config(
            state="normal"
        )

        self.output_box.delete(
            "1.0",
            "end"
        )

        self.output_box.insert(
            "1.0",
            translated
        )

        self.output_box.config(
            state="disabled"
        )

        self.translate_btn.config(
            state="normal",
            text="Translate"
        )

        self.status_label.config(
            text="Translation completed successfully."
        )
    def _show_error(self, error_message):

        self.translate_btn.config(
            state="normal",
            text="Translate"
        )

        self.status_label.config(
            text="Translation failed."
        )

        messagebox.showerror(
            "Translation Error",
            f"Unable to translate the text.\n\n{error_message}\n\n"
            "Please check your internet connection and try again."
        )

    # ==========================================================
    # COPY OUTPUT
    # ==========================================================

    def copy_output(self):

        text = self.output_box.get(
            "1.0",
            "end"
        ).strip()

        if not text:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        self.status_label.config(
            text="Copied to clipboard."
        )

    # ==========================================================
    # CLEAR INPUT & OUTPUT
    # ==========================================================

    def clear_fields(self):

        self.input_box.delete(
            "1.0",
            "end"
        )

        self.output_box.config(
            state="normal"
        )

        self.output_box.delete(
            "1.0",
            "end"
        )

        self.output_box.config(
            state="disabled"
        )

        self.status_label.config(
            text="Ready"
        )

    # ==========================================================
    # TEXT TO SPEECH
    # ==========================================================

    def speak_output(self):

        text = self.output_box.get(
            "1.0",
            "end"
        ).strip()

        if not text:
            messagebox.showinfo(
                "Nothing to Speak",
                "Translate something first."
            )
            return

        self.status_label.config(
            text="Speaking..."
        )

        threading.Thread(
            target=self._speak_worker,
            args=(text,),
            daemon=True
        ).start()

    def _speak_worker(self, text):

        try:

            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="Finished speaking."
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Speech Error",
                    str(error)
                )
            )


# ==========================================================
# MAIN PROGRAM
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TranslatorApp(root)

    root.mainloop()