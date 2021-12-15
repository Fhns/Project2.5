# networked multiplayer game
from dataclasses import dataclass
import datetime
import json
from typing import Dict
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960


@dataclass
class Player:
    x_location: int
    y_location: int
    points: int
    last_update: datetime.datetime

    def to_json(self):
        return json.dumps({"x_location": self.x_location, "y_location": self.y_location, "points": self.points})


@dataclass
class GameState:
    player_states: Dict[str, Player]

    def from_json(self, data):
        json_data = json.loads(data)
        for location, player in enumerate(json_data['player_states']):
            self.player_states[location] = Player(**player)

    def to_json(self):
        pass
