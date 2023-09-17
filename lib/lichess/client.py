from __future__ import annotations
from typing import Any, Dict

from .base import BaseClient
from .config import Config
from .tokens import Token
from lichess.play import (
    Board, Bot, Bulk, Challenge, Puzzle, Simuls
)
from lichess.query import (
    Account, Broadcast, Explorer, Game, Message, Relations, Study, Tablebase, Team, Tournament, TV, User
)

class LichessClient(BaseClient):
    _instance: LichessClient | None = None

    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        self.verbose = kwargs.get('verbose', True)

    def config(self) -> Config:
        return Config(self.verbose)

    def token(self) -> Token:
        return Token(self.verbose)
    
    def board(self) -> Board:
        return Board(self.verbose)
    
    def bot(self) -> Bot:
        return Bot(self.verbose)
    
    def bulk(self) -> Bulk:
        return Bulk(self.verbose)
    
    def challenge(self) -> Challenge:
        return Challenge(self.verbose)
    
    def puzzle(self) -> Puzzle:
        return Puzzle(self.verbose)
    
    def simuls(self) -> Simuls:
        return Simuls(self.verbose)
    
    def account(self) -> Account:
        return Account(self.verbose)
    
    def broadcast(self) -> Broadcast:
        return Broadcast(self.verbose)
    
    def explorer(self) -> Explorer:
        return Explorer(self.verbose)
    
    def game(self) -> Game:
        return Game(self.verbose)
    
    def message(self) -> Message:
        return Message(self.verbose)
    
    def relations(self) -> Relations:
        return Relations(self.verbose)
    
    def study(self) -> Study:
        return Study(self.verbose)
    
    def tablebase(self) -> Tablebase:
        return Tablebase(self.verbose)
    
    def team(self) -> Team:
        return Team(self.verbose)
    
    def tournament(self) -> Tournament:
        return Tournament(self.verbose)
    
    def tv(self) -> TV:
        return TV(self.verbose)
    
    def user(self) -> User:
        return User(self.verbose)
