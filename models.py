from dataclasses import dataclass, field
from datetime import datetime



# data classes for the whole project

@dataclass
class Listing:
    source: str
    title: str
    seller: str
    price: float
    url: str


@dataclass
class Mention:
    source: str
    text: str
    url: str
    timestamp: datetime


@dataclass
class FlaggedListing:
    listing: Listing
    score: float
    reasons: list



@dataclass
class TrademarkReport:
    brand: str
    total_scanned: int
    flagged: list = field(default_factory=list)



@dataclass
class GenericideReport:
    brand: str
    generic_count: int
    branded_count: int
    examples_generic: list = field(default_factory=list)
    examples_branded: list = field(default_factory=list)


    @property
    def ratio(self):
        total = self.generic_count + self.branded_count
        if total == 0:
            return 0.0
        return self.generic_count / total
