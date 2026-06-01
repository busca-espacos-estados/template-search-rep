"""
Busca em Largura (BFS - Breadth-First Search)
==============================================
Implemente o algoritmo BFS para o 8-puzzle.

Propriedades esperadas:
  - Completo: sim
  - Ótimo: sim (custo uniforme = 1 por passo)
  - Complexidade de tempo: O(b^d)
  - Complexidade de espaço: O(b^d)

Dicas:
  - Use uma fila FIFO (collections.deque) como fronteira.
  - Mantenha um conjunto de estados visitados para evitar ciclos.
  - Atualize SearchResult com nodes_expanded, nodes_generated e max_frontier_size.
"""

from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        # TODO: implemente a BFS aqui
        raise NotImplementedError("Implemente o método search na classe BFS.")
