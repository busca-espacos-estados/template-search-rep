"""Testes para a classe State — não devem ser modificados pelos alunos."""

import pytest
from puzzle.state import State, GOAL_STATE


EASY = (1, 2, 3, 4, 5, 6, 7, 0, 8)   # 1 passo da solução
MED  = (1, 2, 3, 4, 5, 6, 0, 7, 8)   # 2 passos


class TestStateBasics:
    def test_goal_is_goal(self):
        assert State(GOAL_STATE).is_goal

    def test_non_goal(self):
        assert not State(EASY).is_goal

    def test_blank_index(self):
        assert State(EASY).blank_index == 7

    def test_invalid_state_raises(self):
        with pytest.raises(ValueError):
            State((1, 2, 3, 4, 5, 6, 7, 8, 9))

    def test_hash_equality(self):
        a = State(EASY)
        b = State(EASY, parent=State(GOAL_STATE))
        assert a == b
        assert hash(a) == hash(b)


class TestNeighbors:
    def test_corner_has_two_neighbors(self):
        s = State((0, 1, 2, 3, 4, 5, 6, 7, 8))
        assert len(s.neighbors()) == 2

    def test_center_has_four_neighbors(self):
        s = State((1, 2, 3, 4, 0, 5, 6, 7, 8))
        assert len(s.neighbors()) == 4

    def test_edge_has_three_neighbors(self):
        s = State((1, 0, 2, 3, 4, 5, 6, 7, 8))
        assert len(s.neighbors()) == 3

    def test_neighbor_differs_by_one_swap(self):
        for n in State(EASY).neighbors():
            diffs = sum(1 for a, b in zip(State(EASY).tiles, n.tiles) if a != b)
            assert diffs == 2

    def test_neighbor_has_parent(self):
        s = State(EASY)
        for n in s.neighbors():
            assert n.parent == s

    def test_neighbor_cost_incremented(self):
        for n in State(EASY).neighbors():
            assert n.cost == 1


class TestPath:
    def test_path_root_only(self):
        s = State(GOAL_STATE)
        assert s.path() == [s]

    def test_path_includes_initial(self):
        s = State(EASY)
        child = s.neighbors()[0]
        path = child.path()
        assert path[0] == s
        assert path[-1] == child

    def test_path_length_matches_cost(self):
        child = State(EASY).neighbors()[0]
        assert len(child.path()) == child.cost + 1

    def test_actions_empty_at_root(self):
        assert State(GOAL_STATE).actions() == []

    def test_actions_length_matches_cost(self):
        child = State(EASY).neighbors()[0]
        assert len(child.actions()) == child.cost
