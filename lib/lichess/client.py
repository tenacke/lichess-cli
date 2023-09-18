from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseClient
from .config import ConfigClient
from .tokens import TokenClient
from lichess.play import (
    BoardClient, BotClient, BulkClient, ChallengeClient, PuzzleClient, SimulsClient
)
from lichess.query import (
    AccountClient, BroadcastClient, ExplorerClient, GameClient, MessageClient, RelationsClient, StudyClient, TablebaseClient, TeamClient, TournamentClient, TVClient, UserClient
)

class LichessClient(BaseClient):
    _instance: LichessClient | None = None

    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        pass

    def config(self) -> ConfigClient:
        return ConfigClient()

    def token(self) -> TokenClient:
        return TokenClient()
    
    def board(self) -> BoardClient:
        return BoardClient()
    
    def bot(self) -> BotClient:
        return BotClient()
    
    def bulk(self) -> BulkClient:
        return BulkClient()
    
    def challenge(self) -> ChallengeClient:
        return ChallengeClient()
    
    def puzzle(self) -> PuzzleClient:
        return PuzzleClient()
    
    def simuls(self) -> SimulsClient:
        return SimulsClient()
    
    def account(self, key: List | None) -> AccountClient:
        if key is not None:
            key = key[0]
        return AccountClient(token_key=key)
    
    def broadcast(self) -> BroadcastClient:
        return BroadcastClient()
    
    def explorer(self) -> ExplorerClient:
        return ExplorerClient()
    
    def game(self) -> GameClient:
        return GameClient()
    
    def message(self) -> MessageClient:
        return MessageClient()
    
    def relations(self) -> RelationsClient:
        return RelationsClient()
    
    def study(self) -> StudyClient:
        return StudyClient()
    
    def tablebase(self) -> TablebaseClient:
        return TablebaseClient()
    
    def team(self) -> TeamClient:
        return TeamClient()
    
    def tournament(self) -> TournamentClient:
        return TournamentClient()
    
    def tv(self) -> TVClient:
        return TVClient()
    
    def user(self) -> UserClient:
        return UserClient()
