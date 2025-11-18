import itertools
from hypothesis import given, example, strategies as st
from board_generation import generate_board, BoardTypes, OpenedBoard, MAX_LENGTH
from typing import Final, Callable

__EXPERT_BOARD: Final[OpenedBoard] = generate_board(width=30, height=16, amount_mines=99,
                                                    board_type=BoardTypes.OPENED,
                                                    start_cell=(0, 0))


@st.composite
def st_opened_board(
        draw: Callable[[st.SearchStrategy[int | tuple[int, int]]], int | tuple[int, int]]) -> OpenedBoard:
    width: int = draw(st.integers(min_value=1, max_value=MAX_LENGTH))
    height: int = draw(st.integers(min_value=1, max_value=MAX_LENGTH))
    amount_mines: int = draw(st.integers(min_value=1, max_value=width * height))
    start_cell: tuple[int, int] = draw(st.tuples(st.integers(0, width - 1), st.integers(0, height - 1)))
    return generate_board(width, height, amount_mines, BoardTypes.OPENED, start_cell)


@given(st_opened_board())
@example(__EXPERT_BOARD)
def test_amount_mines(opened_board):
    counted_mines = sum(
        opened_board.get_cell(x, y).is_mine for x in range(opened_board.width) for y in range(opened_board.height))
    assert counted_mines == opened_board.amount_mines


@given(st_opened_board())
@example(__EXPERT_BOARD)
def test_start_cell_not_mine(opened_board):
    x, y = opened_board.start_cell
    assert not opened_board.get_cell(x, y).is_mine


@given(st_opened_board())
@example(__EXPERT_BOARD)
def test_values(opened_board):
    offsets: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for x, y in itertools.product(range(opened_board.width), range(opened_board.height)):
        current_cell = opened_board.get_cell(x, y)
        if current_cell.is_mine:
            continue
        neighboring_mines: int = 0
        for x_offset, y_offset in offsets:
            neighbor_x, neighbor_y = x + x_offset, y + y_offset
            if (0 <= neighbor_x < opened_board.width and 0 <= neighbor_y < opened_board.height
                    and opened_board.get_cell(neighbor_x, neighbor_y).is_mine):
                neighboring_mines += 1
        assert neighboring_mines == current_cell.value
