import csv

class VoteManager:
    def __init__(self, votes_filename: str = "votes.csv", voters_filename: str = "voters.csv") -> None:
        """Initializes the vote manager with candidate list and loads existing votes."""
        self.votes_filename = votes_filename
        self.voters_filename = voters_filename
        self.candidates = ["John", "Jane"]
        self.votes = {candidate: 0 for candidate in self.candidates}
        self._load_votes()

    def _load_votes(self) -> None:
        """Loads vote counts from the votes file if it exists, otherwise creates a new file."""
        try:
            with open(self.votes_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] in self.votes:
                        self.votes[row[0]] = int(row[1])
        except FileNotFoundError:
            self._save_votes()
        except Exception as e:
            print(f"Error loading votes: {e}")

    def _save_votes(self) -> None:
        """Saves the current vote counts to the votes file."""
        try:
            with open(self.votes_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                for candidate, count in self.votes.items():
                    writer.writerow([candidate, count])
        except Exception as e:
            print(f"Error saving votes: {e}")

    def cast_vote(self, candidate: str, voter_id: str) -> tuple[bool, str]:
        """
        Casts a vote for a candidate if the voter ID is valid and has not voted yet.

        Args:
            candidate: The candidate's name to vote for.
            voter_id: The voter's UNO ID, must be 8 digits.

        Returns:
            A tuple of success status and message.
        """
        if candidate not in self.votes:
            return False, "Invalid candidate."

        if not voter_id.isdigit() or len(voter_id) != 8:
            return False, "UNO ID must be an 8-digit number."

        if self._has_voted(voter_id):
            return False, "Already Voted"

        self.votes[candidate] += 1
        self._save_votes()
        self._record_voter(voter_id, candidate)
        return True, f"Thank you for voting for {candidate}!"

    def _record_voter(self, voter_id: str, candidate: str) -> None:
        """
        Records the voter's ID and selected candidate to the voters file.

        Args:
            voter_id: The voter's UNO ID.
            candidate: The candidate's name.
        """
        try:
            file_exists = False
            try:
                with open(self.voters_filename, 'r', newline='') as f:
                    file_exists = True
            except FileNotFoundError:
                pass

            with open(self.voters_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["voter_id", "candidate"])
                writer.writerow([voter_id, candidate])
        except Exception as e:
            print(f"Error recording voter: {e}")

    def _has_voted(self, voter_id: str) -> bool:
        """
        Checks if a voter has already voted.
        Params:
            voter_id: The voter's UNO ID.
        Returns:
            True if the voter has already voted, False otherwise.
        """
        try:
            with open(self.voters_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if row and row[0] == voter_id:
                        return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error checking voter: {e}")
        return False

    def get_votes(self) -> dict:
        """
        Returns a copy of the current vote tally.
        Returns:
            A dictionary of candidate names and their respective vote counts.
        """
        return self.votes.copy()
