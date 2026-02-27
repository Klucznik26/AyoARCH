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
    "app_title": "Ayo Arch v1.2.0 - Archive Viewer",
    "open_archive": "Otwórz archiwum",
    "save_dir": "Katalog zapisu",
    "settings": "Ustawienia",
    "close": "Zamknij",
    "drop_zone_text": "Przeciągnij i upuść archiwum tutaj",
    "theme_label": "Motyw kolorystyczny:",
    "lang_label": "Język:",
    "theme_dark": "Ciemny",
    "theme_light": "Jasny",
    "theme_relax": "Relaksacyjny",
    "theme_creative": "Kreatywny",
    "theme_system": "Systemowy",
    "not_zip_error": "To nie jest plik .zip!",
    "no_images_error": "Brak obrazów w ZIP!",
    "error_prefix": "Błąd: ",
    "save": "Zapisz",
    "cancel": "Anuluj",
    "dep_install_title": "Wymagany dodatek",
    "dep_install_question": "Obsługa plików .7z wymaga biblioteki 'py7zr'.\\nCzy chcesz, aby program pobrał i zainstalował ją teraz automatycznie?",
    "dep_installing": "Instalowanie biblioteki py7zr... Proszę czekać.",
    "dep_install_error": "Błąd instalacji: ",
    "dep_install_cancel": "Anulowano. Biblioteka py7zr jest wymagana dla plików .7z.",
    "file_name": "Nazwa pliku"
}"""
    with open(os.path.join(i18n_dir, "pl.py"), "w", encoding="utf-8") as f:
        f.write(pl_content)

    # Tworzenie pliku lt.py
    lt_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Archyvų peržiūra",
    "open_archive": "Atidaryti archyvą",
    "save_dir": "Pasirinkti išsaugojimo aplanką",
    "settings": "Nustatymai",
    "close": "Uždaryti",
    "drop_zone_text": "Nutempkite archyvą čia",
    "theme_label": "Tema:",
    "lang_label": "Kalba:",
    "theme_dark": "Tamsi",
    "theme_light": "Šviesi",
    "theme_relax": "Atpalaiduojanti",
    "theme_creative": "Kūrybinis",
    "theme_system": "Sistemos",
    "not_zip_error": "Tai nėra .zip failas!",
    "no_images_error": "Archyve nėra vaizdų!",
    "error_prefix": "Klaida: ",
    "save": "Išsaugoti",
    "cancel": "Atšaukti",
    "dep_install_title": "Trūksta priklausomybės",
    "dep_install_question": ".7z failų palaikymui reikalinga 'py7zr' biblioteka.\\nAr norite ją atsisiųsti ir įdiegti automatiškai dabar?",
    "dep_installing": "Diegiama py7zr biblioteka... Prašome palaukti.",
    "dep_install_error": "Diegimo klaida: ",
    "dep_install_cancel": "Atšaukta. .7z failams reikalinga py7zr biblioteka.",
    "file_name": "Failo pavadinimas"
}"""
    with open(os.path.join(i18n_dir, "lt.py"), "w", encoding="utf-8") as f:
        f.write(lt_content)

    # Tworzenie pliku en.py
    en_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Archive Viewer",
    "open_archive": "Open Archive",
    "save_dir": "Save Directory",
    "settings": "Settings",
    "close": "Close",
    "drop_zone_text": "Drag and drop archive here",
    "theme_label": "Color Theme:",
    "lang_label": "Language:",
    "theme_dark": "Dark",
    "theme_light": "Light",
    "theme_relax": "Relax",
    "theme_creative": "Creative",
    "theme_system": "System",
    "not_zip_error": "This is not a .zip file!",
    "no_images_error": "No images in ZIP!",
    "error_prefix": "Error: ",
    "save": "Save",
    "cancel": "Cancel",
    "dep_install_title": "Missing Dependency",
    "dep_install_question": "Support for .7z files requires 'py7zr' library.\\nDo you want to download and install it automatically now?",
    "dep_installing": "Installing py7zr library... Please wait.",
    "dep_install_error": "Installation error: ",
    "dep_install_cancel": "Cancelled. The py7zr library is required for .7z files.",
    "file_name": "File Name"
}"""
    with open(os.path.join(i18n_dir, "en.py"), "w", encoding="utf-8") as f:
        f.write(en_content)

    # Tworzenie pliku es.py (Hiszpański)
    es_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Visor de Archivos",
    "open_archive": "Abrir archivo",
    "save_dir": "Directorio de guardado",
    "settings": "Configuración",
    "close": "Cerrar",
    "drop_zone_text": "Arrastra y suelta el archivo aquí",
    "theme_label": "Tema de color:",
    "lang_label": "Idioma:",
    "theme_dark": "Oscuro",
    "theme_light": "Claro",
    "theme_relax": "Relax",
    "theme_creative": "Creativo",
    "theme_system": "Sistema",
    "not_zip_error": "¡No es un archivo .zip!",
    "no_images_error": "¡No hay imágenes en el ZIP!",
    "error_prefix": "Error: ",
    "save": "Guardar",
    "cancel": "Cancelar",
    "dep_install_title": "Dependencia faltante",
    "dep_install_question": "El soporte para archivos .7z requiere la biblioteca 'py7zr'.\\n¿Desea descargarla e instalarla automáticamente ahora?",
    "dep_installing": "Instalando la biblioteca py7zr... Por favor espere.",
    "dep_install_error": "Error de instalación: ",
    "dep_install_cancel": "Cancelado. La biblioteca py7zr es necesaria para archivos .7z.",
    "file_name": "Nombre del archivo"
}"""
    with open(os.path.join(i18n_dir, "es.py"), "w", encoding="utf-8") as f:
        f.write(es_content)

    # Tworzenie pliku fr.py (Francuski)
    fr_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Visionneuse d'archives",
    "open_archive": "Ouvrir l'archive",
    "save_dir": "Répertoire de sauvegarde",
    "settings": "Paramètres",
    "close": "Fermer",
    "drop_zone_text": "Glissez et déposez l'archive ici",
    "theme_label": "Thème de couleur :",
    "lang_label": "Langue :",
    "theme_dark": "Sombre",
    "theme_light": "Clair",
    "theme_relax": "Relax",
    "theme_creative": "Créatif",
    "theme_system": "Système",
    "not_zip_error": "Ce n'est pas un fichier .zip !",
    "no_images_error": "Aucune image dans le ZIP !",
    "error_prefix": "Erreur : ",
    "save": "Enregistrer",
    "cancel": "Annuler",
    "dep_install_title": "Dépendance manquante",
    "dep_install_question": "Le support des fichiers .7z nécessite la bibliothèque 'py7zr'.\\nVoulez-vous la télécharger et l'installer automatiquement maintenant ?",
    "dep_installing": "Installation de la bibliothèque py7zr... Veuillez patienter.",
    "dep_install_error": "Erreur d'installation : ",
    "dep_install_cancel": "Annulé. La bibliothèque py7zr est requise pour les fichiers .7z.",
    "file_name": "Nom du fichier"
}"""
    with open(os.path.join(i18n_dir, "fr.py"), "w", encoding="utf-8") as f:
        f.write(fr_content)

    # Tworzenie pliku it.py (Włoski)
    it_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Visualizzatore di archivi",
    "open_archive": "Apri archivio",
    "save_dir": "Cartella di salvataggio",
    "settings": "Impostazioni",
    "close": "Chiudi",
    "drop_zone_text": "Trascina l'archivio qui",
    "theme_label": "Tema colore:",
    "lang_label": "Lingua:",
    "theme_dark": "Scuro",
    "theme_light": "Chiaro",
    "theme_relax": "Relax",
    "theme_creative": "Creativo",
    "theme_system": "Sistema",
    "not_zip_error": "Non è un file .zip!",
    "no_images_error": "Nessuna immagine nello ZIP!",
    "error_prefix": "Errore: ",
    "save": "Salva",
    "cancel": "Annulla",
    "dep_install_title": "Dipendenza mancante",
    "dep_install_question": "Il supporto per i file .7z richiede la libreria 'py7zr'.\\nVuoi scaricarla e installarla automaticamente ora?",
    "dep_installing": "Installazione della libreria py7zr... Attendere prego.",
    "dep_install_error": "Errore di installazione: ",
    "dep_install_cancel": "Annullato. La libreria py7zr è richiesta per i file .7z.",
    "file_name": "Nome del file"
}"""
    with open(os.path.join(i18n_dir, "it.py"), "w", encoding="utf-8") as f:
        f.write(it_content)

    # Tworzenie pliku ro.py (Rumuński)
    ro_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Vizualizator de arhive",
    "open_archive": "Deschide arhiva",
    "save_dir": "Director de salvare",
    "settings": "Setări",
    "close": "Închide",
    "drop_zone_text": "Trage și plasează arhiva aici",
    "theme_label": "Temă de culoare:",
    "lang_label": "Limbă:",
    "theme_dark": "Întunecat",
    "theme_light": "Luminos",
    "theme_relax": "Relax",
    "theme_creative": "Creativ",
    "theme_system": "Sistem",
    "not_zip_error": "Nu este un fișier .zip!",
    "no_images_error": "Nu există imagini în ZIP!",
    "error_prefix": "Eroare: ",
    "save": "Salvează",
    "cancel": "Anulează",
    "dep_install_title": "Dependență lipsă",
    "dep_install_question": "Suportul pentru fișierele .7z necesită biblioteca 'py7zr'.\\nDoriți să o descărcați și să o instalați automat acum?",
    "dep_installing": "Se instalează biblioteca py7zr... Vă rugăm să așteptați.",
    "dep_install_error": "Eroare la instalare: ",
    "dep_install_cancel": "Anulat. Biblioteca py7zr este necesară pentru fișierele .7z.",
    "file_name": "Nume fișier"
}"""
    with open(os.path.join(i18n_dir, "ro.py"), "w", encoding="utf-8") as f:
        f.write(ro_content)

    # Tworzenie pliku sk.py (Słowacki)
    sk_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Prehliadač archívov",
    "open_archive": "Otvoriť archív",
    "save_dir": "Adresár pre uloženie",
    "settings": "Nastavenia",
    "close": "Zavrieť",
    "drop_zone_text": "Presuňte archív sem",
    "theme_label": "Farebný motív:",
    "lang_label": "Jazyk:",
    "theme_dark": "Tmavý",
    "theme_light": "Svetlý",
    "theme_relax": "Relax",
    "theme_creative": "Kreatívny",
    "theme_system": "Systémový",
    "not_zip_error": "Toto nie je súbor .zip!",
    "no_images_error": "Žiadne obrázky v ZIP!",
    "error_prefix": "Chyba: ",
    "save": "Uložiť",
    "cancel": "Zrušiť",
    "dep_install_title": "Chýbajúca závislosť",
    "dep_install_question": "Podpora súborov .7z vyžaduje knižnicu 'py7zr'.\\nChcete ju teraz automaticky stiahnuť a nainštalovať?",
    "dep_installing": "Inštalácia knižnice py7zr... Čakajte prosím.",
    "dep_install_error": "Chyba inštalácie: ",
    "dep_install_cancel": "Zrušené. Knižnica py7zr je vyžadovaná pre súbory .7z.",
    "file_name": "Názov súboru"
}"""
    with open(os.path.join(i18n_dir, "sk.py"), "w", encoding="utf-8") as f:
        f.write(sk_content)

    # Tworzenie pliku el.py (Grecki)
    el_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Προβολή Αρχείων",
    "open_archive": "Άνοιγμα αρχείου",
    "save_dir": "Κατάλογος αποθήκευσης",
    "settings": "Ρυθμίσεις",
    "close": "Κλείσιμο",
    "drop_zone_text": "Σύρετε και αποθέστε το αρχείο εδώ",
    "theme_label": "Θέμα χρώματος:",
    "lang_label": "Γλώσσα:",
    "theme_dark": "Σκοτεινό",
    "theme_light": "Φωτεινό",
    "theme_relax": "Χαλαρό",
    "theme_creative": "Δημιουργικό",
    "theme_system": "Σύστημα",
    "not_zip_error": "Δεν είναι αρχείο .zip!",
    "no_images_error": "Δεν υπάρχουν εικόνες στο ZIP!",
    "error_prefix": "Σφάλμα: ",
    "save": "Αποθήκευση",
    "cancel": "Ακύρωση",
    "dep_install_title": "Λείπει εξάρτηση",
    "dep_install_question": "Η υποστήριξη αρχείων .7z απαιτεί τη βιβλιοθήκη 'py7zr'.\\nΘέλετε να τη κατεβάσετε και να την εγκαταστήσετε αυτόματα τώρα?",
    "dep_installing": "Εγκατάσταση βιβλιοθήκης py7zr... Παρακαλώ περιμένετε.",
    "dep_install_error": "Σφάλμα εγκατάστασης: ",
    "dep_install_cancel": "Ακυρώθηκε. Η βιβλιοθήκη py7zr απαιτείται για αρχεία .7z.",
    "file_name": "Όνομα αρχείου"
}"""
    with open(os.path.join(i18n_dir, "el.py"), "w", encoding="utf-8") as f:
        f.write(el_content)

    # Tworzenie pliku ka.py (Gruziński)
    ka_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - არქივის დამთვალიერებელი",
    "open_archive": "არქივის გახსნა",
    "save_dir": "შენახვის დირექტორია",
    "settings": "პარამეტრები",
    "close": "დახურვა",
    "drop_zone_text": "გადმოიტანეთ არქივი აქ",
    "theme_label": "ფერის თემა:",
    "lang_label": "ენა:",
    "theme_dark": "მუქი",
    "theme_light": "ნათელი",
    "theme_relax": "რელაქსი",
    "theme_creative": "კრეატიული",
    "theme_system": "სისტემური",
    "not_zip_error": "ეს არ არის .zip ფაილი!",
    "no_images_error": "არქივში სურათები არ არის!",
    "error_prefix": "შეცდომა: ",
    "save": "შენახვა",
    "cancel": "გაუქმება",
    "dep_install_title": "დამოკიდებულება აკლია",
    "dep_install_question": ".7z ფაილების მხარდაჭერა მოითხოვს 'py7zr' ბიბლიოთეკას.\\nგსურთ მისი ავტომატურად ჩამოტვირთვა და ინსტალაცია ახლა?",
    "dep_installing": "py7zr ბიბლიოთეკის ინსტალაცია... გთხოვთ დაელოდოთ.",
    "dep_install_error": "ინსტალაციის შეცდომა: ",
    "dep_install_cancel": "გაუქმებულია. py7zr ბიბლიოთეკა საჭიროა .7z ფაილებისთვის.",
    "file_name": "ფაილის სახელი"
}"""
    with open(os.path.join(i18n_dir, "ka.py"), "w", encoding="utf-8") as f:
        f.write(ka_content)

    # Tworzenie pliku pt.py (Portugalski)
    pt_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Visualizador de Arquivos",
    "open_archive": "Abrir Arquivo",
    "save_dir": "Diretório de Salvamento",
    "settings": "Configurações",
    "close": "Fechar",
    "drop_zone_text": "Arraste e solte o arquivo aqui",
    "theme_label": "Tema de Cor:",
    "lang_label": "Idioma:",
    "theme_dark": "Escuro",
    "theme_light": "Claro",
    "theme_relax": "Relax",
    "theme_creative": "Criativo",
    "theme_system": "Sistema",
    "not_zip_error": "Isto não é um arquivo .zip!",
    "no_images_error": "Sem imagens no ZIP!",
    "error_prefix": "Erro: ",
    "save": "Salvar",
    "cancel": "Cancelar",
    "dep_install_title": "Dependência em falta",
    "dep_install_question": "O suporte a arquivos .7z requer a biblioteca 'py7zr'.\\nDeseja baixar e instalá-la automaticamente agora?",
    "dep_installing": "Instalando a biblioteca py7zr... Por favor, aguarde.",
    "dep_install_error": "Erro de instalação: ",
    "dep_install_cancel": "Cancelado. A biblioteca py7zr é necessária para arquivos .7z.",
    "file_name": "Nome do Arquivo"
}"""
    with open(os.path.join(i18n_dir, "pt.py"), "w", encoding="utf-8") as f:
        f.write(pt_content)

    # Tworzenie pliku cs.py (Czeski)
    cs_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Prohlížeč archivů",
    "open_archive": "Otevřít archiv",
    "save_dir": "Adresář pro uložení",
    "settings": "Nastavení",
    "close": "Zavřít",
    "drop_zone_text": "Přetáhněte archiv sem",
    "theme_label": "Barevný motiv:",
    "lang_label": "Jazyk:",
    "theme_dark": "Tmavý",
    "theme_light": "Světlý",
    "theme_relax": "Relax",
    "theme_creative": "Kreativní",
    "theme_system": "Systémový",
    "not_zip_error": "Toto není soubor .zip!",
    "no_images_error": "Žádné obrázky v ZIP!",
    "error_prefix": "Chyba: ",
    "save": "Uložit",
    "cancel": "Zrušit",
    "dep_install_title": "Chybějící závislost",
    "dep_install_question": "Podpora souborů .7z vyžaduje knihovnu 'py7zr'.\\nChcete ji nyní automaticky stáhnout a nainstalovat?",
    "dep_installing": "Instalace knihovny py7zr... Čekejte prosím.",
    "dep_install_error": "Chyba instalace: ",
    "dep_install_cancel": "Zrušeno. Knihovna py7zr je vyžadována pro soubory .7z.",
    "file_name": "Název souboru"
}"""
    with open(os.path.join(i18n_dir, "cs.py"), "w", encoding="utf-8") as f:
        f.write(cs_content)

    # Tworzenie pliku uk.py (Ukraiński)
    uk_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Переглядач архівів",
    "open_archive": "Відкрити архів",
    "save_dir": "Каталог збереження",
    "settings": "Налаштування",
    "close": "Закрити",
    "drop_zone_text": "Перетягніть архів сюди",
    "theme_label": "Колірна тема:",
    "lang_label": "Мова:",
    "theme_dark": "Темна",
    "theme_light": "Світла",
    "theme_relax": "Релакс",
    "theme_creative": "Креативна",
    "theme_system": "Системна",
    "not_zip_error": "Це не файл .zip!",
    "no_images_error": "Немає зображень у ZIP!",
    "error_prefix": "Помилка: ",
    "save": "Зберегти",
    "cancel": "Скасувати",
    "dep_install_title": "Відсутня залежність",
    "dep_install_question": "Підтримка файлів .7z вимагає бібліотеки 'py7zr'.\\nВи хочете завантажити та встановити її автоматично зараз?",
    "dep_installing": "Встановлення бібліотеки py7zr... Будь ласка, зачекайте.",
    "dep_install_error": "Помилка встановлення: ",
    "dep_install_cancel": "Скасовано. Бібліотека py7zr необхідна для файлів .7z.",
    "file_name": "Ім'я файлу"
}"""
    with open(os.path.join(i18n_dir, "uk.py"), "w", encoding="utf-8") as f:
        f.write(uk_content)

    # Tworzenie pliku lv.py (Łotewski)
    lv_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Arhīvu skatītājs",
    "open_archive": "Atvērt arhīvu",
    "save_dir": "Saglabāšanas direktorija",
    "settings": "Iestatījumi",
    "close": "Aizvērt",
    "drop_zone_text": "Velciet un nometiet arhīvu šeit",
    "theme_label": "Krāsu tēma:",
    "lang_label": "Valoda:",
    "theme_dark": "Tumša",
    "theme_light": "Gaiša",
    "theme_relax": "Relaksējoša",
    "theme_creative": "Radoša",
    "theme_system": "Sistēmas",
    "not_zip_error": "Tas nav .zip fails!",
    "no_images_error": "ZIP arhīvā nav attēlu!",
    "error_prefix": "Kļūda: ",
    "save": "Saglabāt",
    "cancel": "Atcelt",
    "dep_install_title": "Trūkst atkarības",
    "dep_install_question": ".7z failu atbalstam nepieciešama 'py7zr' bibliotēka.\\nVai vēlaties to lejupielādēt un instalēt automātiski tagad?",
    "dep_installing": "Instalē py7zr bibliotēku... Lūdzu, uzgaidiet.",
    "dep_install_error": "Instalācijas kļūda: ",
    "dep_install_cancel": "Atcelts. .7z failiem nepieciešama py7zr bibliotēka.",
    "file_name": "Faila nosaukums"
}"""
    with open(os.path.join(i18n_dir, "lv.py"), "w", encoding="utf-8") as f:
        f.write(lv_content)

    # Tworzenie pliku et.py (Estoński)
    et_content = """STRINGS = {
    "app_title": "Ayo Arch v1.2.0 - Arhiivivaatur",
    "open_archive": "Ava arhiiv",
    "save_dir": "Salvestamise kaust",
    "settings": "Seaded",
    "close": "Sulge",
    "drop_zone_text": "Lohista arhiiv siia",
    "theme_label": "Värviteema:",
    "lang_label": "Keel:",
    "theme_dark": "Tume",
    "theme_light": "Hele",
    "theme_relax": "Lõõgastav",
    "theme_creative": "Loominguline",
    "theme_system": "Süsteemi",
    "not_zip_error": "See ei ole .zip fail!",
    "no_images_error": "ZIP-is pole pilte!",
    "error_prefix": "Viga: ",
    "save": "Salvesta",
    "cancel": "Tühista",
    "dep_install_title": "Puuduv sõltuvus",
    "dep_install_question": ".7z failide tugi vajab 'py7zr' teeki.\\nKas soovite selle kohe automaatselt alla laadida ja installida?",
    "dep_installing": "py7zr teegi installimine... Palun oodake.",
    "dep_install_error": "Installimise viga: ",
    "dep_install_cancel": "Tühistatud. .7z failide jaoks on vajalik py7zr teek.",
    "file_name": "Faili nimi"
}"""
    with open(os.path.join(i18n_dir, "et.py"), "w", encoding="utf-8") as f:
        f.write(et_content)

    print(f"Sukces! Utworzono folder i18n i pliki językowe w: {i18n_dir}")

if __name__ == "__main__":
    create_i18n()