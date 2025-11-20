import itertools
from hypothesis import given, example, strategies as st
from board_generation import generate_board, BoardTypes, OpenedBoard, MAX_LENGTH, OFFSETS
from typing import Final, Callable

EXPERT_BOARD: Final[OpenedBoard] = generate_board(width=30, height=16, amount_mines=99,
                                                  board_type=BoardTypes.OPENED,
                                                  start_cell=(0, 0))


@st.composite
def st_opened_board(draw: Callable[[st.SearchStrategy[int]], int]) -> OpenedBoard:
    """
    Creates a strategy for an opened board.
    """
    width: int = draw(st.integers(min_value=1, max_value=MAX_LENGTH))
    height: int = draw(st.integers(min_value=1, max_value=MAX_LENGTH))
    amount_mines: int = draw(st.integers(min_value=1, max_value=width * height))
    start_x: int = draw(st.integers(min_value=0, max_value=width - 1))
    start_y: int = draw(st.integers(min_value=0, max_value=height - 1))
    return generate_board(width, height, amount_mines, BoardTypes.OPENED, (start_x, start_y))


@given(st_opened_board())
@example(EXPERT_BOARD)
def test_amount_mines(opened_board: OpenedBoard) -> None:
    counted_mines = sum(
        opened_board.get_cell(x, y).is_mine for x in range(opened_board.width) for y in range(opened_board.height))
    assert counted_mines == opened_board.amount_mines


@given(st_opened_board())
@example(EXPERT_BOARD)
def test_start_cell_not_mine(opened_board: OpenedBoard) -> None:
    x, y = opened_board.start_cell
    assert not opened_board.get_cell(x, y).is_mine


def check_values(opened_board: OpenedBoard):
    """
    Helper function that checks if all the values of the cells on a board are correct.
    """
    for x, y in itertools.product(range(opened_board.width), range(opened_board.height)):
        current_cell = opened_board.get_cell(x, y)
        if current_cell.is_mine:
            continue
        neighboring_mines: int = 0
        for x_offset, y_offset in OFFSETS:
            neighbor_x, neighbor_y = x + x_offset, y + y_offset
            if (0 <= neighbor_x < opened_board.width and 0 <= neighbor_y < opened_board.height
                    and opened_board.get_cell(neighbor_x, neighbor_y).is_mine):
                neighboring_mines += 1
        assert neighboring_mines == current_cell.value


@given(st_opened_board())
@example(EXPERT_BOARD)
def test_values(opened_board: OpenedBoard) -> None:
    check_values(opened_board)


@given(st_opened_board(), st.data())
def test_values_after_place_mine(opened_board: OpenedBoard, data) -> None:
    x: int = data.draw(st.integers(min_value=0, max_value=opened_board.width - 1))
    y: int = data.draw(st.integers(min_value=0, max_value=opened_board.height - 1))
    opened_board.place_mine(x, y)
    check_values(opened_board)


@given(st_opened_board(), st.data())
def test_values_after_remove_mine(opened_board: OpenedBoard, data) -> None:
    x: int = data.draw(st.integers(min_value=0, max_value=opened_board.width - 1))
    y: int = data.draw(st.integers(min_value=0, max_value=opened_board.height - 1))
    opened_board.remove_mine(x, y)
    check_values(opened_board)
