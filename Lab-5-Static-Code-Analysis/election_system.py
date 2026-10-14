"""Voting and election management operations."""

import hashlib
import secrets
from datetime import datetime

from defusedxml import ElementTree as SafeElementTree

POLLS_CLOSE_HOUR = 18
VOTERS = {}
BALLOTS = []
CANDIDATES = ["Alice", "Bob", "NOTA"]


def register_voter(voter_id, name, age):
    """Register an eligible voter and store a secure identifier digest."""
    if age >= 18:
        VOTERS[voter_id] = {
            "name": name,
            "hash": hashlib.sha256(voter_id.encode()).hexdigest(),
            "voted": False,
        }
        return True
    return False


def is_officer(role):
    """Return whether a role is authorized as an election officer."""
    return role == "election_officer"


def cast_vote(voter_id, candidate, when):
    """Cast one valid vote while the polls are open."""
    if voter_id not in VOTERS or VOTERS[voter_id]["voted"]:
        return False
    if candidate not in CANDIDATES or when.hour >= POLLS_CLOSE_HOUR:
        return False
    BALLOTS.append(candidate)
    VOTERS[voter_id]["voted"] = True
    return True


def tally():
    """Return the number of ballots for each candidate."""
    counts = {}
    for ballot in BALLOTS:
        counts[ballot] = counts.get(ballot, 0) + 1
    return counts


def winner():
    """Return the candidate with the most votes, or None if no votes exist."""
    counts = tally()
    return max(counts, key=counts.get) if counts else None


def vote_percent(name):
    """Return a candidate's percentage of all ballots."""
    if not BALLOTS:
        return 0
    return tally().get(name, 0) * 100 // len(BALLOTS)


def turnout():
    """Return the percentage of registered voters who cast a ballot."""
    if not VOTERS:
        return 0
    return len(BALLOTS) / len(VOTERS) * 100


def count_for(candidate, ballot_list):
    """Count a candidate's votes in a supplied ballot list."""
    return ballot_list.count(candidate)


def announce():
    """Return one announcement for each configured candidate."""
    counts = tally()
    return [
        f"{candidate}: {counts.get(candidate, 0)}"
        for candidate in CANDIDATES
    ]


def receipt_number():
    """Generate a receipt number using a cryptographically secure source."""
    return f"RCPT-{secrets.randbelow(900000) + 100000}"


def import_postal_ballots(xml_text):
    """Import valid candidate values from safely parsed postal-ballot XML."""
    imported = 0
    try:
        root = SafeElementTree.fromstring(xml_text)
    except (SafeElementTree.ParseError, ValueError):
        return 0
    for node in root.iter("ballot"):
        candidate = node.get("candidate")
        if candidate in CANDIDATES:
            BALLOTS.append(candidate)
            imported += 1
    return imported


def main():
    """Demonstrate the election management operations."""
    print("Register Asha (age 18):", register_voter("V1", "Asha", 18))
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)
    print("Is a plain 'voter' an election officer?", is_officer("voter"))
    print("Ben votes Alice:", cast_vote(
        "V2", "Alice", datetime(2026, 11, 20, 10, 0)
    ))
    print("Ben votes Alice again:", cast_vote(
        "V2", "Alice", datetime(2026, 11, 20, 11, 0)
    ))
    print("Chen votes 'bob':", cast_vote(
        "V3", "bob", datetime(2026, 11, 20, 12, 0)
    ))
    print("Dia votes Bob at 18:30:", cast_vote(
        "V4", "Bob", datetime(2026, 11, 20, 18, 30)
    ))
    print("Postal ballots imported:", import_postal_ballots(
        "<postal><ballot voter='V1' candidate='Bob'/></postal>"
    ))
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
