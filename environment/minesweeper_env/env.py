from typing import Any
import gymnasium as gym
from gymnasium.core import ObsType
from gymnasium.spaces import Discrete
from game import Minesweeper
import numpy as np


# TODO: Textual for console board output


class EnvMinesweeper(gym.Env):
    metadata: dict[str, list[str]] = {"render_modes": ["human"]}

    def __init__(self, width, height, amount_mines):
        self.width: int = width
        self.height: int = height
        self.amount_mines: int = amount_mines

        self.amount_actions: int = self.width * self.height

        self.action_space: Discrete = Discrete(self.amount_actions)
        self.observation_space: Discrete = Discrete(self.amount_actions)
        self.game = Minesweeper(self.width, self.height, self.amount_mines)
        self.state = None
        self.mask = np.zeros(self.width * self.height, dtype=np.int8)

    def step(self, action):
        x, y = action % self.width, action // self.width
        if (opening := self.game.board_model.open(x, y)) is None:
            terminated = True
            reward = 0
        else:
            reward = len(opening)
            for cell in opening:
                self.state[cell.x * self.width + cell.y * self.height] = cell.value
                self.mask[cell.x * self.width + cell.y * self.height] = 1
            terminated = self.game.board_model.finished()

        return self.state, reward, terminated, False, {"mask": self.mask}

    def reset(self, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        self.game.reset_board(self.width, self.height, amount_mines=self.amount_mines)
        self.state = np.zeros(self.width * self.height, dtype=np.int8) - 2
        return self.state

    def render(self):
        pass

    def close(self):
        pass
