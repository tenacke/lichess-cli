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

    def config(self, **kwargs: Dict[str, Any]) -> ConfigClient:
        return ConfigClient()

    def token(self, **kwargs: Dict[str, Any]) -> TokenClient:
        return TokenClient()
    
    def board(self, **kwargs: Dict[str, Any]) -> BoardClient:
        return BoardClient()
    
    def bot(self, **kwargs: Dict[str, Any]) -> BotClient:
        return BotClient()
    
    def bulk(self, **kwargs: Dict[str, Any]) -> BulkClient:
        return BulkClient()
    
    def challenge(self, **kwargs: Dict[str, Any]) -> ChallengeClient:
        return ChallengeClient()
    
    def puzzle(self, **kwargs: Dict[str, Any]) -> PuzzleClient:
        return PuzzleClient()
    
    def simuls(self, **kwargs: Dict[str, Any]) -> SimulsClient:
        return SimulsClient()
    
    def account(self, key: List | None, **kwargs: Dict[str, Any]) -> AccountClient:
        if key is not None:
            key = key[0]
        return AccountClient(token_key=key)
    
    def broadcast(self, **kwargs: Dict[str, Any]) -> BroadcastClient:
        return BroadcastClient()
    
    def explorer(self, **kwargs: Dict[str, Any]) -> ExplorerClient:
        return ExplorerClient()
    
    def game(self, **kwargs: Dict[str, Any]) -> GameClient:
        return GameClient()
    
    def message(self, **kwargs: Dict[str, Any]) -> MessageClient:
        return MessageClient()
    
    def relations(self, **kwargs: Dict[str, Any]) -> RelationsClient:
        return RelationsClient()
    
    def study(self, **kwargs: Dict[str, Any]) -> StudyClient:
        return StudyClient()
    
    def tablebase(self, **kwargs: Dict[str, Any]) -> TablebaseClient:
        return TablebaseClient()
    
    def team(self, **kwargs: Dict[str, Any]) -> TeamClient:
        return TeamClient()
    
    def tournament(self, **kwargs: Dict[str, Any]) -> TournamentClient:
        return TournamentClient()
    
    def tv(self, **kwargs: Dict[str, Any]) -> TVClient:
        return TVClient()
    
    def user(self, **kwargs: Dict[str, Any]) -> UserClient:
        return UserClient()
