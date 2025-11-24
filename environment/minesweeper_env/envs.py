from typing import Any

import gymnasium as gym
from gymnasium.core import ObsType
from gymnasium.spaces import Discrete


# TODO: Textual for console board output


class EnvOpenBoardMinesweeper(gym.Env):
    metadata: dict[str, list[str]] = {"render_modes": ["human"]}

    def __init__(self, width: int, height: int, start_cell: tuple[int, int] = (0, 0), render_mode: str | None = None):
        self.render_mode: str = render_mode
        self.width: int = width
        self.height: int = height
        self.start_cell: tuple[int, int] = start_cell

        self.actions: int = self.width * self.height

        self.action_space: Discrete = Discrete(self.actions)
        self.observation_space: Discrete = Discrete(self.actions)

    def step(self, action):
        pass

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
