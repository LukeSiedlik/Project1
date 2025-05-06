#GUI file
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton,
    QRadioButton, QVBoxLayout, QHBoxLayout, QWidget, QButtonGroup
)
from PyQt6.QtCore import Qt

class VoteWindow(QMainWindow):
    def __init__(self, on_vote_func) -> None:
        super().__init__()
        self.result_label = None
        self.summary_label = None
        self.button_group = None
        self.jane_radio = None
        self.john_radio = None
        self.id_input = None
        self.on_vote_func = on_vote_func
        self.setWindowTitle("UNO Voting Ballot")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self) -> None:
        main_layout = QVBoxLayout()

        instruction_label = QLabel("Enter your UNO ID and select a candidate")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instruction_label)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter 8-digit UNO ID")
        self.id_input.setMaxLength(8)
        main_layout.addWidget(self.id_input)

        self.john_radio = QRadioButton("John")
        self.jane_radio = QRadioButton("Jane")
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.john_radio)
        radio_layout.addWidget(self.jane_radio)
        main_layout.addLayout(radio_layout)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.john_radio)
        self.button_group.addButton(self.jane_radio)

        vote_button = QPushButton("Vote")
        vote_button.clicked.connect(self.on_vote_clicked)
        main_layout.addWidget(vote_button)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.result_label)

        self.summary_label = QLabel("")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.summary_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def display_result(self, message: str, error: bool = False) -> None:
        """Display the result message with appropriate styling."""
        self.result_label.setText(message)
        color = "red" if error else "green"
        self.result_label.setStyleSheet(f"color: {color};")

    def on_vote_clicked(self) -> None:
        """Handles GUI submission and updates display based on result."""
        voter_id = self.id_input.text().strip()
        candidate = "John" if self.john_radio.isChecked() else "Jane"

        success, message, summary = self.on_vote_func(voter_id, candidate)

        self.display_result(message, error=not success)
        self.summary_label.setText(summary)

        if success:
            self.id_input.clear()
            self.button_group.setExclusive(False)
            self.john_radio.setChecked(False)
            self.jane_radio.setChecked(False)
            self.button_group.setExclusive(True)
