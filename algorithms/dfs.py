"""
Busca em Profundidade (DFS - Depth-First Search)
=================================================
Implemente o algoritmo DFS para o 8-puzzle.

Propriedades esperadas:
  - Completo: não (pode entrar em ciclos sem controle de visitados)
  - Ótimo: não
  - Complexidade de tempo: O(b^m)
  - Complexidade de espaço: O(b*m)  ← vantagem sobre BFS

Dicas:
  - Use uma pilha LIFO (list ou collections.deque com appendleft) como fronteira.
  - Use um limite de profundidade (depth_limit) para evitar loops infinitos.
  - Considere controle de visitados por ramo (não globalmente) para manter
    a propriedade de espaço linear.
"""

from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        # TODO: implemente a DFS aqui
        raise NotImplementedError("Implemente o método search na classe DFS.")
