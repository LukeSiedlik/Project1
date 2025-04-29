import sys
from PyQt6.QtWidgets import QApplication
from gui import VoteWindow
from logic import VoteManager

def main() -> None:
    """
    Initializes the VoteManager, sets up the QApplication, and opens the VoteWindow.
    This function serves as the entry point of the application.
    """
    vote_manager: VoteManager = VoteManager("votes.csv", "voters.csv")

    app: QApplication = QApplication(sys.argv)
    window: VoteWindow = VoteWindow(vote_manager.cast_vote)
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()