from dataclasses import dataclass


@dataclass
class Team:
    id_: int | None = None
    name: str | None = None
    points: int | None = 0


@dataclass
class Player:
    id_: int | None = None
    name: str | None = None
    goals: int | None = 0
    team_id: int | None = None


@dataclass
class Stadium:
    id_: int | None = None
    name: str | None = None
    team_id: int | None = None
