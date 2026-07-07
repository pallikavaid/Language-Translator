# 🌍 Language Translator

A desktop language translation application built with **Python** and **Tkinter** that translates text between multiple languages using **Google Translate**. The application features auto language detection, text-to-speech, keyboard shortcuts, and a responsive graphical user interface.

---

## 📌 Features

- 🌐 Translate text between multiple languages
- 🔍 Auto language detection
- 🔄 Language swap functionality
- 🔊 Text-to-Speech (Offline)
- 📋 Copy translated text to clipboard
- 🗑 Clear input and output fields
- ⌨ Keyboard shortcuts
  - **Ctrl + Enter** → Translate
  - **Esc** → Clear
- 🧵 Responsive GUI using multithreading
- 🖥 Clean and user-friendly interface

---

## 🖼 Application Preview

### Main Interface

![Main Interface](assets/screenshot1.png)

---

### Multi-language Translation

![Translation Example](assets/screenshot2.png)

---

### Auto Language Detection

![Auto Detect](assets/screenshot3.png)

---

## 🛠 Technologies Used

- Python
- Tkinter
- deep-translator
- pyttsx3
- Pillow

---

## 📂 Project Structure

```
Language-Translator/
│
├── assets/
│   ├── icon.png
│   ├── screenshot1.png
│   ├── screenshot2.png
│   └── screenshot3.png
│
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/pallikavaid/Language-Translator.git
```

Move into the project folder

```bash
cd Language-Translator
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

---

## 📖 Usage

1. Enter the text you want to translate.
2. Select the source language (or choose **Auto Detect**).
3. Select the target language.
4. Click **Translate** or press **Ctrl + Enter**.
5. Copy or listen to the translated text.
6. Press **Esc** or click **Clear** to reset the application.

---

## 💡 Future Improvements

- Translation history
- Dark mode
- Voice input
- Export translations
- Support for additional translation services

---

## 👩‍💻 Author

**Pallika Vaid**

Mechanical Engineering Student
GitHub: https://github.com/pallikavaid

---

## ⭐ Support

If you found this project useful, consider giving it a **star** on GitHub.