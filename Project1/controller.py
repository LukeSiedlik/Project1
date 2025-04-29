from logic import VoteManager
from gui import VoteWindow


class Controller:
    """
    The Controller class manages the interaction between the logic (VoteManager)
    and the GUI (VoteWindow)
    """
    def __init__(self) -> None:
        """
        Initializes the Controller by creating instances of VoteManager and VoteWindow.
        Connects the vote casting action to the appropriate handler.
        """
        self.vote_manager: VoteManager = VoteManager()
        self.view: VoteWindow = VoteWindow(self.handle_vote)

    def handle_vote(self, candidate: str, voter_id: str) -> None:
        """
        Handles the voting action by calling the VoteManager to cast the vote.
        Args:
            candidate (str): The name of the candidate the user votes for.
            voter_id (str): The 8-digit voter ID of the person voting.
        """
        success, message = self.vote_manager.cast_vote(candidate, voter_id)
        self.view.result_label.setText(message)

    def run(self) -> None:
        """
        Starts the GUI window and begins the voting process.
        """
        self.view.show()
