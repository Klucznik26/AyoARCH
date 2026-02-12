STYLE = """
    /* 1. GLOBALNE TŁO APLIKACJI */
    QMainWindow, QWidget#SettingsWindow {
        background-color: #3B332B;
    }

    /* 2. GŁÓWNE POWIERZCHNIE / PANELS */
    QWidget#Sidebar {
        background-color: #3B332B;
        border: 1px solid #2E3947;
        border-radius: 8px;
    }

    /* 3. TYPOGRAFIA */
    QLabel {
        color: #E6EDF3;
        font-size: 14px;
    }

    /* 5. PRZYCISKI - SECONDARY BUTTON (Domyślny) */
    QPushButton {
        background-color: #4E4439;
        color: #E6EDF3;
        border: 1px solid #666666;
        padding: 8px;
        border-radius: 8px;
        min-height: 30px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #5C5144;
    }
    QPushButton:pressed {
        background-color: #3B332B;
    }

    /* 5. PRZYCISKI - PRIMARY BUTTON */
    QPushButton#PrimaryButton {
        background-color: #04E38A;
        color: #00261A;
        border: none;
    }
    QPushButton#PrimaryButton:hover {
        background-color: #02C978;
    }
    QPushButton#PrimaryButton:pressed {
        background-color: #00B86C;
    }
    QPushButton#PrimaryButton:disabled {
        background-color: #0C3B2C;
        color: #E6EDF3AA;
    }

    /* 5. PRZYCISKI - DANGER BUTTON */
    QPushButton#DangerButton {
        background-color: #FF5A5F;
        color: #FFFFFF;
        border: none;
    }
    QPushButton#DangerButton:hover {
        background-color: #E0484D;
    }

    /* 6. POLA TEKSTOWE / INPUTY */
    QComboBox {
        background-color: #4E4439;
        color: #E6EDF3;
        border: 1px solid #666666;
        padding: 5px;
        border-radius: 8px;
    }
    QComboBox:hover {
        border: 1px solid #7F8A96;
    }
    QComboBox:focus {
        border: 1px solid #04E38A;
    }
    QComboBox::drop-down {
        border: 0px;
    }
    QComboBox QAbstractItemView {
        background-color: #4E4439;
        color: #E6EDF3;
        selection-background-color: #044D33;
        selection-color: #E6EDF3;
        border: 1px solid #666666;
    }

    /* 10. SCROLLBARY */
    QScrollBar:vertical {
        background: #151B22;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #2E3947;
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background: #3A4656;
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
        background-color: #2A3440;
        border-radius: 4px;
        text-align: center;
        color: #E6EDF3;
    }
    QProgressBar::chunk {
        background-color: #04E38A;
        border-radius: 4px;
    }

    /* 11. DRZEWO PLIKÓW */
    QTreeWidget {
        background-color: #4E4439;
        color: #E6EDF3;
        border: 1px solid #666666;
        border-radius: 8px;
    }
    QTreeWidget::item:selected {
        background-color: #044D33;
        color: #E6EDF3;
    }
"""

DROP_ZONE = """
    QLabel {
        border: 2px dashed #666666;
        border-radius: 8px;
        color: #E6EDF3;
       font-size: 16px;
        background-color: #4E4439;
    }
"""