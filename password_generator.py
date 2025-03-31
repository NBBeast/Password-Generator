import random
import string
import pyperclip
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import ttkbootstrap as ttkb  # Uvozite ttkbootstrap

# Seznam za zgodovino gesel
password_history = []

# Globalne nastavitve jezika
language = "sl"  # "sl" za slovenščino, "en" za angleščino

# Slovenski in angleški prevodi
translations = {
    "sl": {
        "password_length": "Dolžina gesla (8-50):",
        "lowercase_letters": "Male črke",
        "uppercase_letters": "Velike črke",
        "digits": "Številke",
        "special_characters": "Posebni znaki",
        "exclude_characters": "Izključi znake:",
        "generate": "Generiraj",
        "copy_password": "Kopiraj geslo",
        "password_history": "Zgodovina gesel",
        "clear": "Počisti",
        "generated_password": "Generirano geslo:",
        "error_length": "Dolžina gesla mora biti med 8 in 50 znaki!",
        "error_invalid_input": "Vnesite veljavno dolžino gesla!",
        "error_no_character_type": "Izbrati morate vsaj en tip znakov!",
        "error_all_characters_excluded": "Izključili ste vse znake tega tipa!",
        "clear_history": "Počisti zgodovino",
        "close": "Zapri",
        "help": "Pomoč",
        "help_content": "1. Vnesite dolžino gesla.\n"
                        "2. Izberite tipe znakov, ki jih želite vključiti.\n"
                        "3. Pritisnite 'Generiraj'.\n"
                        "4. Geslo bo prikazano in kopirano v odložišče.\n"
                        "5. Prejšnja gesla so shranjena v zgodovini.\n"
                        "6. Če želite počistiti zgodovino, uporabite gumb 'Počisti'.",
        "error": "Napaka!"  # Dodano za napako
    },
    "en": {
        "password_length": "Password Length (8-50):",
        "lowercase_letters": "Lowercase Letters",
        "uppercase_letters": "Uppercase Letters",
        "digits": "Digits",
        "special_characters": "Special Characters",
        "exclude_characters": "Exclude Characters:",
        "generate": "Generate",
        "copy_password": "Copy Password",
        "password_history": "Password History",
        "clear": "Clear",
        "generated_password": "Generated Password:",
        "error_length": "Password length must be between 8 and 50 characters!",
        "error_invalid_input": "Please enter a valid password length!",
        "error_no_character_type": "You must select at least one type of character!",
        "error_all_characters_excluded": "You have excluded all characters of this type!",
        "clear_history": "Clear History",
        "close": "Close",
        "help": "Help",
        "help_content": "1. Enter the desired password length.\n"
                        "2. Select the types of characters you want to include.\n"
                        "3. Press 'Generate'.\n"
                        "4. The password will be shown and copied to the clipboard.\n"
                        "5. Previous passwords are saved in history.\n"
                        "6. To clear the history, click 'Clear'.",
        "error": "Error!"  # Dodano za napako
    }
}

# Funkcija za pridobivanje prevoda
def translate(key):
    global language
    return translations[language].get(key, key)

def generate_password(length, use_lower, use_upper, use_digits, use_punctuation, exclude_chars):
    characters = ""
    if use_lower:
        lowercase_chars = ''.join(c for c in string.ascii_lowercase if c not in exclude_chars)
        if not lowercase_chars:
            messagebox.showerror(translate("error"), translate("error_all_characters_excluded"))
            return ""
        characters += lowercase_chars
    if use_upper:
        uppercase_chars = ''.join(c for c in string.ascii_uppercase if c not in exclude_chars)
        if not uppercase_chars:
            messagebox.showerror(translate("error"), translate("error_all_characters_excluded"))
            return ""
        characters += uppercase_chars
    if use_digits:
        digit_chars = ''.join(c for c in string.digits if c not in exclude_chars)
        if not digit_chars:
            messagebox.showerror(translate("error"), translate("error_all_characters_excluded"))
            return ""
        characters += digit_chars
    if use_punctuation:
        punctuation_chars = ''.join(c for c in string.punctuation if c not in exclude_chars)
        if not punctuation_chars:
            messagebox.showerror(translate("error"), translate("error_all_characters_excluded"))
            return ""
        characters += punctuation_chars

    if not characters:
        messagebox.showerror(translate("error"), translate("error_no_character_type"))
        return ""

    return ''.join(random.choice(characters) for _ in range(length))

def copy_from_history(event, history_listbox):
    selected = history_listbox.curselection()
    if selected:
        pyperclip.copy(history_listbox.get(selected[0]))

def show_history():
    global history_window
    if 'history_window' in globals() and history_window.winfo_exists():
        return  # Če je okno že odprto, ne odpiraj novega

    history_window = tk.Toplevel(root)
    history_window.title(translate("password_history"))
    history_window.geometry("600x400")  # Povečana velikost okna zgodovine

    label_history = ttk.Label(history_window, text=translate("password_history") + ":", font=("Arial", 12))
    label_history.pack(pady=10)

    history_listbox = tk.Listbox(history_window, width=50, height=10, font=("Arial", 12))
    history_listbox.pack(pady=10)

    for password in password_history:
        history_listbox.insert(tk.END, password)

    history_listbox.bind("<Double-1>", lambda event: copy_from_history(event, history_listbox))

    def clear_history():
        password_history.clear()
        history_listbox.delete(0, tk.END)

    button_clear = ttk.Button(history_window, text=translate("clear_history"), command=clear_history, width=20)
    button_clear.pack(pady=5)
    
    button_close = ttk.Button(history_window, text=translate("close"), command=history_window.destroy, width=20)
    button_close.pack(pady=10)

def on_generate():
    try:
        length = int(entry_length.get())

        # Preveri, če je dolžina med 8 in 50
        if length < 8 or length > 50:
            messagebox.showerror(translate("error"), translate("error_length"))
            return
        
        use_lower = var_lower.get()
        use_upper = var_upper.get()
        use_digits = var_digits.get()
        use_punctuation = var_punctuation.get()
        exclude_chars = entry_exclude.get().strip()

        if not (use_lower or use_upper or use_digits or use_punctuation):
            messagebox.showerror(translate("error"), translate("error_no_character_type"))
            return

        password = generate_password(length, use_lower, use_upper, use_digits, use_punctuation, exclude_chars)
        
        if password:
            label_result.config(text=f"{translate('generated_password')} {password}", foreground="green")
            pyperclip.copy(password)
            button_copy.config(text="✔ Kopirano!", state=tk.DISABLED)
            root.after(2000, lambda: button_copy.config(text=translate("copy_password"), state=tk.NORMAL))
            password_history.append(password)
    except ValueError:
        messagebox.showerror(translate("error"), translate("error_invalid_input"))

def show_help():
    global help_window  # Deklaracija globalne spremenljivke
    # Preveri, ali je okno za pomoč že odprto
    if 'help_window' in globals() and help_window.winfo_exists():
        return  # Če je okno že odprto, ga ne odpremo ponovno
    
    help_window = tk.Toplevel(root)
    help_window.title(translate("help"))
    help_window.geometry("670x400")  # Povečano za 70px

    label_help = ttk.Label(help_window, text=translations[language]["help_content"], font=("Arial", 12), justify="left")
    label_help.pack(pady=20, padx=20)  # Dodan tudi notranji razmik (padding), da besedilo ni preblizu robov

    button_close = ttk.Button(help_window, text=translate("close"), command=help_window.destroy, width=20)
    button_close.pack(pady=10)

def clear_inputs():
    entry_length.delete(0, tk.END)
    var_lower.set(False)
    var_upper.set(False)
    var_digits.set(False)
    var_punctuation.set(False)
    entry_exclude.delete(0, tk.END)
    label_result.config(text="")

# Ustvarite osnovno okno z uporabo ttkbootstrap in teme "superhero"
root = ttkb.Window(themename="superhero")  # Tukaj uporabite temo "superhero"
root.title("Generator Gesel")
root.geometry("800x800")  # Velikost okna nastavljena na 800x800

# Okno z gumbi v navigacijski vrstici
frame_nav = ttk.Frame(root)
frame_nav.pack(pady=20, padx=20, fill=tk.X)

# Funkcija za spremembo jezika
def set_language(lang):
    global language
    language = lang
    update_ui()

# Funkcija za osvežitev besedila v uporabniškem vmesniku
def update_ui():
    label_length.config(text=translate("password_length"))
    checkbox_lower.config(text=translate("lowercase_letters"))
    checkbox_upper.config(text=translate("uppercase_letters"))
    checkbox_digits.config(text=translate("digits"))
    checkbox_punctuation.config(text=translate("special_characters"))
    label_exclude.config(text=translate("exclude_characters"))
    button_generate.config(text=translate("generate"))
    button_copy.config(text=translate("copy_password"))
    button_history.config(text=translate("password_history"))
    button_clear.config(text=translate("clear"))
    label_result.config(text="")

# Dodaj gumbe za nastavitve in pomoč v navigacijsko vrstico
def on_settings_click():
    global settings_window
    if 'settings_window' in globals() and settings_window.winfo_exists():
        return  # Če je okno že odprto, ne odpiraj novega

    settings_window = tk.Toplevel(root)
    settings_window.title("Jezik")
    settings_window.geometry("400x300")  # Povečana velikost okna nastavitev
    
    label_settings = ttk.Label(settings_window, text="Izberi jezik:", font=("Arial", 12))
    label_settings.pack(pady=10)

    button_slovenian = ttk.Button(settings_window, text="Slovenščina", command=lambda: set_language("sl"))
    button_slovenian.pack(pady=5)
    button_english = ttk.Button(settings_window, text="English", command=lambda: set_language("en"))
    button_english.pack(pady=5)

# Dodaj gumb za pomoč
def on_help_click():
    show_help()

button_settings = ttk.Button(frame_nav, text="⚙", command=on_settings_click, width=10, bootstyle="info")
button_settings.grid(row=0, column=0, padx=10)

button_help = ttk.Button(frame_nav, text="❓", command=on_help_click, width=10, bootstyle="info")
button_help.grid(row=0, column=1, padx=10)

# --- Prvi odsek: Navigacija in nastavitve --- 
separator1 = ttk.Separator(root, orient="horizontal")
separator1.pack(fill="x", pady=10)

# --- Drugi odsek: Generiranje gesla --- 
frame = ttk.Frame(root, padding=30)
frame.pack(pady=20)

label_length = ttk.Label(frame, text=translate("password_length"), font=("Arial", 12))
label_length.grid(row=0, column=0, sticky="w", padx=10, pady=10)

entry_length = ttk.Entry(frame, font=("Arial", 12))
entry_length.grid(row=0, column=1, pady=10, padx=10)

var_lower = tk.BooleanVar(value=False)
var_upper = tk.BooleanVar(value=False)
var_digits = tk.BooleanVar(value=False)
var_punctuation = tk.BooleanVar(value=False)

checkbox_lower = ttk.Checkbutton(frame, text=translate("lowercase_letters"), variable=var_lower, style="TCheckbutton")
checkbox_lower.grid(row=1, column=0, sticky="w", padx=10, pady=5)
checkbox_upper = ttk.Checkbutton(frame, text=translate("uppercase_letters"), variable=var_upper, style="TCheckbutton")
checkbox_upper.grid(row=2, column=0, sticky="w", padx=10, pady=5)
checkbox_digits = ttk.Checkbutton(frame, text=translate("digits"), variable=var_digits, style="TCheckbutton")
checkbox_digits.grid(row=3, column=0, sticky="w", padx=10, pady=5)
checkbox_punctuation = ttk.Checkbutton(frame, text=translate("special_characters"), variable=var_punctuation, style="TCheckbutton")
checkbox_punctuation.grid(row=4, column=0, sticky="w", padx=10, pady=5)

label_exclude = ttk.Label(frame, text=translate("exclude_characters"), font=("Arial", 12))
label_exclude.grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_exclude = ttk.Entry(frame, font=("Arial", 12))
entry_exclude.grid(row=5, column=1, pady=10, padx=10)

button_generate = ttk.Button(frame, text=translate("generate"), command=on_generate, width=20, bootstyle="primary")
button_generate.grid(row=6, column=0, columnspan=2, pady=10)

button_copy = ttk.Button(frame, text=translate("copy_password"), command=lambda: pyperclip.copy(label_result.cget("text").replace(translate("generated_password") + " ", "")), width=20, bootstyle="success")
button_copy.grid(row=7, column=0, columnspan=2, pady=5)

label_result = ttk.Label(frame, text="", font=("Arial", 14))
label_result.grid(row=8, column=0, columnspan=2, pady=5)

# --- Tretji odsek: Počisti zgodovino --- 
separator2 = ttk.Separator(root, orient="horizontal")
separator2.pack(fill="x", pady=10)

frame_clear = ttk.Frame(root)
frame_clear.pack(pady=20)

# Premaknjen gumb "Počisti" v srednji odsek
button_clear = ttk.Button(frame_clear, text=translate("clear"), command=clear_inputs, width=20, bootstyle="warning")
button_clear.grid(row=0, column=0, columnspan=2, pady=5)

# Premaknjen gumb "Zgodovina gesel" v spodnji odsek
button_history = ttk.Button(frame_clear, text=translate("password_history"), command=show_history, width=20, bootstyle="info")
button_history.grid(row=1, column=0, columnspan=2, pady=5)

root.mainloop()
   