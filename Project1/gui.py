from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton,
    QRadioButton, QVBoxLayout, QHBoxLayout, QWidget, QButtonGroup
)
from PyQt6.QtCore import Qt
from PyQt6 import uic
import csv


class VoteWindow(QMainWindow):
    def __init__(self, cast_vote_func) -> None:
        super().__init__()
        #uic.loadUi("vote_window.ui", self)
        self.result_label = None
        self.button_group = None
        self.jane_radio = None
        self.john_radio = None
        self.id_input = None
        self.cast_vote_func = cast_vote_func
        self.setWindowTitle("UNO Voting Ballot")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self) -> None:
        # Main layout
        main_layout = QVBoxLayout()

        # Instruction Label
        instruction_label = QLabel("Enter your UNO ID and select a candidate")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instruction_label)

        # ID Input
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter 8-digit UNO ID")
        self.id_input.setMaxLength(8)
        main_layout.addWidget(self.id_input)

        # Radio buttons
        self.john_radio = QRadioButton("John")
        self.jane_radio = QRadioButton("Jane")
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.john_radio)
        radio_layout.addWidget(self.jane_radio)
        main_layout.addLayout(radio_layout)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.john_radio)
        self.button_group.addButton(self.jane_radio)

        # Vote button
        vote_button = QPushButton("Vote")
        vote_button.clicked.connect(self.on_vote)
        main_layout.addWidget(vote_button)

        # Result label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.result_label)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def on_vote(self) -> None:
        """
        Handle vote submission logic, including validation and calling the voting function.
        """
        voter_id = self.id_input.text().strip()

        if not voter_id:
            self.result_label.setText("Please enter a valid voter ID.")
            self.result_label.setStyleSheet("color: red;")
            return

        if not voter_id.isdigit() or len(voter_id) != 8:
            self.result_label.setText("UNO ID must be an 8-digit number.")
            self.result_label.setStyleSheet("color: red;")
            return

        if not self.john_radio.isChecked() and not self.jane_radio.isChecked():
            self.result_label.setText("Please select a candidate.")
            self.result_label.setStyleSheet("color: red;")
            return

        candidate = "John" if self.john_radio.isChecked() else "Jane"

        if self.has_already_voted(voter_id):
            self.result_label.setText("Already Voted")
            self.result_label.setStyleSheet("color: red;")
            return

        success, message = self.cast_vote_func(candidate, voter_id)

        self.result_label.setText(message)
        if success:
            self.result_label.setStyleSheet("color: green;")
            self.id_input.clear()

            self.button_group.setExclusive(False)
            self.john_radio.setChecked(False)
            self.jane_radio.setChecked(False)
            self.button_group.setExclusive(True)
        else:
            self.result_label.setStyleSheet("color: red;")

    def has_already_voted(self, voter_id: str) -> bool:
        """
        Check if the voter has already voted based on their ID.
        Params:
            voter_id (str): The voter ID.
        Returns:
            bool: True if the voter has already voted, False otherwise.
        """
        try:
            with open("voters.csv", mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header if present
                for row in reader:
                    if row[0] == voter_id:
                        return True
        except FileNotFoundError:
            return False
        return False
