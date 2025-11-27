import itertools
from hypothesis import given, example, strategies as st
from board_generation import generate_board, BoardTypes, ClosedBoard
from typing import Callable
from typing import Final
from config import MAX_LENGTH

# An Expert closed board for testing.
EXPERT_BOARD_CLOSED: Final[ClosedBoard] = generate_board(width=30, height=16, amount_mines=99,
                                                         board_type=BoardTypes.CLOSED)


@st.composite
def st_closed_board(
        draw: Callable[[st.SearchStrategy[int]], int]) -> ClosedBoard:
    """
    Creates a strategy for a closed board.
    """
    width: int = draw(st.integers(min_value=1, max_value=MAX_LENGTH))
    height: int = draw(st.integers(min_value=1, max_value=MAX_LENGTH))
    amount_mines: int = draw(st.integers(min_value=1, max_value=width * height))
    return generate_board(width, height, amount_mines, BoardTypes.CLOSED)


@given(st_closed_board())
@example(EXPERT_BOARD_CLOSED)
def test_amount_mines(closed_board: ClosedBoard) -> None:
    counted_mines = sum(
        closed_board.get_cell(x, y).is_mine for x in range(closed_board.width) for y in range(closed_board.height))
    assert counted_mines == closed_board.amount_mines


def check_values(closed_board: ClosedBoard):
    """
    Helper function that checks if all the values of the cells on a board are correct.
    """
    for x, y in itertools.product(range(closed_board.width), range(closed_board.height)):
        current_cell = closed_board.get_cell(x, y)
        if current_cell.is_mine:
            continue
        neighboring_mines: int = 0
        for neighbor_cell in closed_board.get_neighbors(current_cell):
            if neighbor_cell.is_mine:
                neighboring_mines += 1
        assert neighboring_mines == current_cell.value


@given(st_closed_board())
@example(EXPERT_BOARD_CLOSED)
def test_values(closed_board: ClosedBoard) -> None:
    check_values(closed_board)


@given(st_closed_board(), st.data())
def test_values_after_place_mine(closed_board: ClosedBoard, data) -> None:
    x: int = data.draw_cells(st.integers(min_value=0, max_value=closed_board.width - 1))
    y: int = data.draw_cells(st.integers(min_value=0, max_value=closed_board.height - 1))
    closed_board.place_mine(x, y)
    check_values(closed_board)


@given(st_closed_board(), st.data())
def test_values_after_remove_mine(closed_board: ClosedBoard, data) -> None:
    x: int = data.draw_cells(st.integers(min_value=0, max_value=closed_board.width - 1))
    y: int = data.draw_cells(st.integers(min_value=0, max_value=closed_board.height - 1))
    closed_board.remove_mine(x, y)
    check_values(closed_board)
