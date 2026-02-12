import os

def create_i18n():
    # Ścieżka do folderu i18n w katalogu projektu
    base_dir = os.path.dirname(os.path.abspath(__file__))
    i18n_dir = os.path.join(base_dir, "i18n")
    
    # Tworzenie folderu
    os.makedirs(i18n_dir, exist_ok=True)
    
    # Tworzenie pliku __init__.py
    with open(os.path.join(i18n_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Pakiet i18n")
        
    # Tworzenie pliku pl.py
    pl_content = """STRINGS = {
    "app_title": "Ayo Arch v0.0.1 - Archive Viewer",
    "open_archive": "Otwórz archiwum",
    "save_dir": "Katalog zapisu",
    "settings": "Ustawienia",
    "close": "Zamknij",
    "drop_zone_text": "Przeciągnij i upuść archiwum tutaj",
    "theme_label": "Motyw kolorystyczny:",
    "lang_label": "Język:",
    "theme_dark": "Ciemny",
    "theme_light": "Jasny",
    "theme_system": "Systemowy",
    "not_zip_error": "To nie jest plik .zip!",
    "no_images_error": "Brak obrazów w ZIP!",
    "error_prefix": "Błąd: ",
    "save": "Zapisz",
    "cancel": "Anuluj"
}"""
    with open(os.path.join(i18n_dir, "pl.py"), "w", encoding="utf-8") as f:
        f.write(pl_content)

    # Tworzenie pliku lt.py
    lt_content = """STRINGS = {
    "app_title": "Ayo Arch v0.0.1 - Archive Viewer",
    "open_archive": "Atidaryti archyvą",
    "save_dir": "Pasirinkti išsaugojimo aplanką",
    "settings": "Nustatymai",
    "close": "Uždaryti",
    "drop_zone_text": "Nutempkite archyvą čia",
    "theme_label": "Tema:",
    "lang_label": "Kalba:",
    "theme_dark": "Tamsi",
    "theme_light": "Šviesi",
    "theme_system": "Sistemos",
    "not_zip_error": "Tai nėra .zip failas!",
    "no_images_error": "Archyve nėra vaizdų!",
    "error_prefix": "Klaida: ",
    "save": "Išsaugoti",
    "cancel": "Atšaukti"
}"""
    with open(os.path.join(i18n_dir, "lt.py"), "w", encoding="utf-8") as f:
        f.write(lt_content)

    # Tworzenie pliku en.py
    en_content = """STRINGS = {
    "app_title": "Ayo Arch v0.0.1 - Archive Viewer",
    "open_archive": "Open Archive",
    "save_dir": "Save Directory",
    "settings": "Settings",
    "close": "Close",
    "drop_zone_text": "Drag and drop archive here",
    "theme_label": "Color Theme:",
    "lang_label": "Language:",
    "theme_dark": "Dark",
    "theme_light": "Light",
    "theme_system": "System",
    "not_zip_error": "This is not a .zip file!",
    "no_images_error": "No images in ZIP!",
    "error_prefix": "Error: ",
    "save": "Save",
    "cancel": "Cancel"
}"""
    with open(os.path.join(i18n_dir, "en.py"), "w", encoding="utf-8") as f:
        f.write(en_content)

    print(f"Sukces! Utworzono folder i18n i pliki językowe w: {i18n_dir}")

if __name__ == "__main__":
    create_i18n()