from typing import Any
from board_generation import BoardTypes, OpenedBoard
import gymnasium as gym
from gymnasium.core import ObsType
from gymnasium.spaces import Discrete
from game import Minesweeper
import numpy as np


# TODO: Textual for console board output


class EnvMinesweeperQLearning(gym.Env):
    metadata: dict[str, list[str]] = {"render_modes": ["human"]}

    def __init__(self, width: int, height: int, amount_mines: int, start_cell: tuple[int, int] = (0, 0),
                 board_type: BoardTypes = OpenedBoard,
                 render_mode: str | None = None):
        self.render_mode: str = render_mode
        self.width: int = width
        self.amount_mines: int = amount_mines
        self.height: int = height
        self.board_type: BoardTypes = board_type
        self.start_cell: tuple[int, int] = start_cell

        self.amount_actions: int = self.width * self.height

        self.action_space: Discrete = Discrete(self.amount_actions)
        self.observation_space: Discrete = Discrete(self.amount_actions)
        self.game = Minesweeper(self.width, self.height, self.amount_mines)
        self.state = np.zeros(self.width * self.height, dtype=np.int8) - 1
        self.state, *_ = self.step((0, 0))

    def step(self, action):
        x, y = action % self.width, action // self.width
        if (opening := self.game.board_model.open(x, y)) is None:
            done = True
            reward = 0
        else:
            reward = len(opening)
            for cell in opening:
                self.state[cell.x * self.width + cell.y * self.height] = cell.value
            done = self.game.board_model.finished()

        return self.state, reward, done, False, {}

    def reset(self, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        pass

    def render(self):
        pass

    def close(self):
        pass


class EnvClosedBoardMinesweeper(gym.Env):
    metadata: str = {"render_modes": ["human"]}

    def __init__(self):
        pass
