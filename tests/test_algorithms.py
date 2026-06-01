"""
Testes dos algoritmos de busca.
================================
Os alunos NÃO devem modificar este arquivo.
Os testes verificam:
  1. Correção  — a solução encontrada realmente chega ao estado objetivo.
  2. Otimalidade — BFS e A* devem retornar a solução de menor custo.
  3. Métricas  — nodes_expanded, nodes_generated e depth devem ser coerentes.
  4. Caso sem solução — estado insolúvel deve retornar found=False.
"""

import pytest
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


# ---------------------------------------------------------------------------
# Estados de teste
# ---------------------------------------------------------------------------

TRIVIAL  = GOAL_STATE                        # 0 passos
ONE_STEP = (1, 2, 3, 4, 5, 6, 7, 0, 8)      # 1 passo
TWO_STEP = (1, 2, 3, 4, 5, 6, 0, 7, 8)      # 2 passos
MEDIUM   = (1, 2, 3, 0, 4, 6, 7, 5, 8)      # alguns passos
HARD     = (1, 2, 3, 4, 5, 6, 7, 8, 0)      # já é o goal — espera 0 passos? não, é GOAL mesmo

# Estado insolúvel (inversões ímpares)
UNSOLVABLE = (1, 2, 3, 4, 5, 6, 8, 7, 0)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def verify_solution(result: SearchResult, initial_tiles):
    """Verifica que a solução é um caminho válido do inicial ao objetivo."""
    assert result.found
    path = result.solution.path()
    assert State(initial_tiles) == path[0]
    assert path[-1].is_goal
    for i in range(len(path) - 1):
        neighbors = [n.tiles for n in path[i].neighbors()]
        assert path[i + 1].tiles in neighbors, f"Transição inválida no passo {i}"
    assert result.depth == result.solution.cost


# ---------------------------------------------------------------------------
# BFS
# ---------------------------------------------------------------------------

class TestBFS:
    def _run(self, tiles):
        return BFS().search(State(tiles))

    def test_trivial(self):
        r = self._run(TRIVIAL)
        assert r.found
        assert r.path_cost == 0

    def test_one_step_correct(self):
        r = self._run(ONE_STEP)
        verify_solution(r, ONE_STEP)

    def test_one_step_optimal(self):
        assert self._run(ONE_STEP).path_cost == 1

    def test_two_step_optimal(self):
        assert self._run(TWO_STEP).path_cost == 2

    def test_medium_optimal(self):
        r = self._run(MEDIUM)
        verify_solution(r, MEDIUM)
        # solução ótima deve existir
        assert r.path_cost >= 1

    def test_unsolvable(self):
        r = self._run(UNSOLVABLE)
        assert not r.found

    def test_metrics_nodes_expanded_positive(self):
        r = self._run(TWO_STEP)
        assert r.nodes_expanded >= 1

    def test_metrics_generated_ge_expanded(self):
        r = self._run(TWO_STEP)
        assert r.nodes_generated >= r.nodes_expanded

    def test_actions_match_depth(self):
        r = self._run(TWO_STEP)
        assert len(r.actions) == r.depth


# ---------------------------------------------------------------------------
# DFS
# ---------------------------------------------------------------------------

class TestDFS:
    def _run(self, tiles, depth_limit=50):
        return DFS(depth_limit=depth_limit).search(State(tiles))

    def test_trivial(self):
        r = self._run(TRIVIAL)
        assert r.found
        assert r.path_cost == 0

    def test_one_step_finds_solution(self):
        r = self._run(ONE_STEP)
        verify_solution(r, ONE_STEP)

    def test_two_step_finds_solution(self):
        r = self._run(TWO_STEP)
        verify_solution(r, TWO_STEP)

    def test_unsolvable_within_limit(self):
        # Com depth_limit suficiente e sem solução, deve retornar found=False
        r = self._run(UNSOLVABLE, depth_limit=30)
        assert not r.found

    def test_depth_limit_respected(self):
        r = self._run(ONE_STEP, depth_limit=5)
        # Com limite 5 e solução a 1 passo, deve encontrar
        assert r.found

    def test_metrics_nodes_expanded_positive(self):
        r = self._run(TWO_STEP)
        assert r.nodes_expanded >= 1

    def test_solution_path_valid(self):
        r = self._run(ONE_STEP)
        verify_solution(r, ONE_STEP)


# ---------------------------------------------------------------------------
# A*
# ---------------------------------------------------------------------------

class TestAStar:
    def _run(self, tiles):
        return AStar().search(State(tiles))

    def test_trivial(self):
        r = self._run(TRIVIAL)
        assert r.found
        assert r.path_cost == 0

    def test_one_step_correct(self):
        r = self._run(ONE_STEP)
        verify_solution(r, ONE_STEP)

    def test_one_step_optimal(self):
        assert self._run(ONE_STEP).path_cost == 1

    def test_two_step_optimal(self):
        assert self._run(TWO_STEP).path_cost == 2

    def test_medium_optimal(self):
        r = self._run(MEDIUM)
        verify_solution(r, MEDIUM)

    def test_unsolvable(self):
        r = self._run(UNSOLVABLE)
        assert not r.found

    def test_astar_optimal_equals_bfs(self):
        """A* e BFS devem concordar no custo ótimo."""
        bfs_cost = BFS().search(State(MEDIUM)).path_cost
        astar_cost = self._run(MEDIUM).path_cost
        assert astar_cost == bfs_cost

    def test_astar_expands_fewer_nodes_than_bfs(self):
        """A* com heurística admissível deve expandir menos nós que BFS."""
        tiles = (1, 2, 3, 4, 5, 0, 7, 8, 6)
        bfs_expanded = BFS().search(State(tiles)).nodes_expanded
        astar_expanded = self._run(tiles).nodes_expanded
        assert astar_expanded <= bfs_expanded

    def test_metrics_nodes_expanded_positive(self):
        r = self._run(TWO_STEP)
        assert r.nodes_expanded >= 1

    def test_actions_match_depth(self):
        r = self._run(TWO_STEP)
        assert len(r.actions) == r.depth
