from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import date

@dataclass
class Member:
    """
    Represents a family member participating in the contribution tracker.
    """
    name: str
    monthly_amount: float = 0.0  # Optional monthly plan for reference


@dataclass
class Contribution:
    """
    Represents a single contribution by a member.
    Store dates as ISO strings (YYYY-MM-DD) for simple CSV compatibility.
    """
    member: str
    date: str  # e.g., "2025-09-15"
    amount: float


class Tracker:
    """
    In-memory tracker for members and contributions with simple summaries.
    Keeps data as lists/dicts to align with beginner course content.
    """
    def __init__(self) -> None:
        self.members: Dict[str, Member] = {}
        self.contributions: List[Contribution] = []

    # Member management
    def add_member(self, name: str, monthly_amount: float = 0.0) -> bool:
        """
        Add a new member if not already present.
        Returns True if created, False if duplicate.
        """
        key = name.strip()
        if not key:
            return False
        if key in self.members:
            return False
        self.members[key] = Member(name=key, monthly_amount=monthly_amount)
        return True

    def get_member(self, name: str) -> Optional[Member]:
        """
        Retrieve a member by name or None if not found.
        """
        return self.members.get(name)

    def all_members(self) -> List[Member]:
        """
        Return all members as a list for display/export.
        """
        return list(self.members.values())

    # Contributions
    def record_contribution(self, member: str, amount: float, when: Optional[str] = None) -> bool:
        """
        Record a contribution for an existing member.
        Returns True if recorded, False if member not found or invalid amount.
        """
        if member not in self.members:
            return False
        if amount <= 0:
            return False
        when_iso = when if when else date.today().isoformat()
        self.contributions.append(Contribution(member=member, date=when_iso, amount=amount))
        return True

    def history(self, member: Optional[str] = None) -> List[Contribution]:
        """
        Return all contributions, optionally filtered by member.
        """
        if member is None:
            return list(self.contributions)
        return [c for c in self.contributions if c.member == member]

    # Summaries
    def total_for_member(self, member: str) -> float:
        """
        Compute the total contributed by a single member.
        """
        return sum(c.amount for c in self.contributions if c.member == member)

    def totals_by_member(self) -> Dict[str, float]:
        """
        Compute totals per member across all contributions.
        """
        totals: Dict[str, float] = {name: 0.0 for name in self.members}
        for c in self.contributions:
            if c.member in totals:
                totals[c.member] += c.amount
        return totals
