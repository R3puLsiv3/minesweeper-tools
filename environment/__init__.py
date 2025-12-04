from gymnasium.envs.registration import register

register(
    id="minesweeper",
    entry_point="environment.minesweeper_env:EnvMinesweeper",
    kwargs={"width": 4, "height": 4, "amount_mines": 4}
)
