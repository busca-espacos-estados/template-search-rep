"""
Busca A* (A-estrela)
====================
Implemente o algoritmo A* e a heurística utilizada.

Propriedades esperadas:
  - Completo: sim
  - Ótimo: sim (se a heurística for admissível)

Uma heurística h(n) é admissível se nunca superestima o custo real
até o objetivo. Implemente-a como método desta classe e use dentro de search().

Dicas:
  - Use heapq para manter a fronteira ordenada por f(n) = g(n) + h(n).
  - g(n) = state.cost  (custo acumulado do caminho)
  - h(n) = resultado da sua heurística
"""

import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        # TODO: implemente a heurística aqui
        raise NotImplementedError

    def search(self, initial: State) -> SearchResult:
        # TODO: implemente o A* aqui
        raise NotImplementedError
