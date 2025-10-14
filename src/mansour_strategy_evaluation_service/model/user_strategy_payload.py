from dataclasses import dataclass
from typing import Dict

@dataclass
class UserStrategyActivatedEventPayload:
    userStrategyId: int
    userId: int
    strategyId: str
    symbol: str
    parameters: Dict[str, str]

@dataclass
class UserStrategyDeactivatedEventPayload:
    userStrategyId: int
    userId: int
    strategyId: str
    symbol: str