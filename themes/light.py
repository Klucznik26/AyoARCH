STYLE = """
    /* 1. GLOBALNE TŁO APLIKACJI */
    QMainWindow, QWidget#SettingsWindow {
        background-color: #F9F3E0;
    }

    /* 2. GŁÓWNE POWIERZCHNIE / PANELS */
    QWidget#Sidebar {
        background-color: #F9F3E0;
        border: 1px solid #DCCEA8;
        border-radius: 8px; /* Karty / sekcje / groupbox / sidebar */
    }

    /* 3. TYPOGRAFIA */
    QLabel {
        color: #3E3529; /* Tekst podstawowy */
        font-size: 14px;
    }

    /* 5. PRZYCISKI - SECONDARY BUTTON (Domyślny) */
    QPushButton {
        background-color: #EBE5D2;
        color: #3E3529;
        border: 1px solid #DCCEA8;
        padding: 8px;
        border-radius: 8px;
        min-height: 30px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #F2ECD9;
    }
    QPushButton:pressed {
        background-color: #DCD6C3;
    }

    /* 5. PRZYCISKI - PRIMARY BUTTON (np. Otwórz archiwum) */
    /* Należy nadać przyciskowi objectName="PrimaryButton" w kodzie UI */
    QPushButton#PrimaryButton {
        background-color: #04E38A;
        color: #FFFFFF;
       border: 1px solid #DCCEA8;
    }
    QPushButton#PrimaryButton:hover {
        background-color: #02C978;
    }
    QPushButton#PrimaryButton:pressed {
        background-color: #00B86C;
    }
    QPushButton#PrimaryButton:disabled {
        background-color: #A7EFD2;
        color: #FFFFFFAA;
    }

    /* 5. PRZYCISKI - DANGER BUTTON (np. Zamknij) */
    /* Należy nadać przyciskowi objectName="DangerButton" w kodzie UI */
    QPushButton#DangerButton {
        background-color: #FF5A5F;
        color: #FFFFFF;
        border:1px solid #DCCEA8;
    }
    QPushButton#DangerButton:hover {
        background-color: #E0484D;
    }

    /* 6. POLA TEKSTOWE / INPUTY (QComboBox traktujemy jak input) */
    QComboBox {
        background-color: #EBE5D2;
        color: #3E3529;
        border: 1px solid #DCCEA8;
        padding: 5px;
        border-radius: 8px;
    }
    QComboBox:hover {
        border: 1px solid #C4B58E;
    }
    QComboBox:focus {
        border: 1px solid #04E38A;
    }
    QComboBox::drop-down {
        border: 0px;
    }
    QComboBox QAbstractItemView {
        background-color: #EBE5D2;
        color: #3E3529;
        selection-background-color: #DCD6C3; /* Selection */
        selection-color: #3E3529;
        border: 1px solid #DCCEA8;
    }

    /* 10. SCROLLBARY */
    QScrollBar:vertical {
        background: #F9F3E0;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #DCCEA8;
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background: #C4B58E;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }

    /* 8. PROGRESS BAR */
    QProgressBar {
        border: none;
        background-color: #E8DEC0;
        border-radius: 4px;
        text-align: center;
        color: #3E3529;
    }
    QProgressBar::chunk {
        background-color: #04E38A;
        border-radius: 4px;
    }

    /* 11. DRZEWO PLIKÓW */
    QTreeWidget {
        background-color: #FFFBEB;
        color: #3E3529;
        border: 1px solid #DCCEA8;
        border-radius: 8px;
    }
    QTreeWidget::item:selected {
        background-color: #F0E6C8;
        color: #3E3529;
    }
"""

DROP_ZONE = """
    QLabel {
        border: 2px dashed #DCCEA8;
        border-radius: 8px;
       color: #3E3529;
        font-size: 16px;
        background-color: #EBE5D2;
    }
"""