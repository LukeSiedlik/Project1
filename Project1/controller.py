from logic import VoteManager
from gui import VoteWindow

class Controller:
    """Handles the interaction between the logic and the GUI."""
    def __init__(self) -> None:
        self.vote_manager = VoteManager()
        self.view = VoteWindow(self.handle_vote)

    def handle_vote(self, voter_id: str, candidate: str) -> tuple[bool, str, str]:
        """Handles the voting action by calling the VoteManager to cast the vote."""
        return self.vote_manager.on_vote_clicked(voter_id, candidate)

    def run(self) -> None:
        """Starts the GUI window and begins the voting process."""
        self.view.show()
