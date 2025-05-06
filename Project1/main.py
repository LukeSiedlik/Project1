import sys
from PyQt6.QtWidgets import QApplication
from controller import Controller

def main() -> None:
    """Entry point of the application."""
    app = QApplication(sys.argv)
    controller = Controller()
    controller.run()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
