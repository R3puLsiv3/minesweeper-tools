from gymnasium.envs.registration import register

register(
    id="op_minesweeper",
    entry_point="environment.minesweeper_env:EnvOpenBoardMinesweeper"
)

register(
    id="op_minesweeper",
    entry_point="environment.minesweeper_env:EnvClosedBoardMinesweeper"
)
