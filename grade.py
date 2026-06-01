"""
Avaliador automático — 8-Puzzle (26 pontos)
===========================================
Uso: python3 grade.py
"""

import subprocess
import json
import sys
import re

# ---------------------------------------------------------------------------
# Rubrica: cada entrada é (nome_exibição, id_teste_pytest, pontos)
# ---------------------------------------------------------------------------

RUBRIC = [
    # State — 4 pts
    ("State: neighbors() gera filhos válidos",          "tests/test_state.py::TestNeighbors::test_neighbor_differs_by_one_swap",   1),
    ("State: número correto de vizinhos por posição",   "tests/test_state.py::TestNeighbors::test_corner_has_two_neighbors",       1),
    ("State: path() reconstrói caminho",                "tests/test_state.py::TestPath::test_path_includes_initial",               1),
    ("State: actions() retorna ações corretas",         "tests/test_state.py::TestPath::test_actions_length_matches_cost",         1),

    # BFS — 7 pts
    ("BFS: encontra solução trivial (0 passos)",        "tests/test_algorithms.py::TestBFS::test_trivial",                         1),
    ("BFS: solução correta (caminho válido)",           "tests/test_algorithms.py::TestBFS::test_one_step_correct",                1),
    ("BFS: solução ótima — 1 passo",                   "tests/test_algorithms.py::TestBFS::test_one_step_optimal",                1),
    ("BFS: solução ótima — 2 passos",                  "tests/test_algorithms.py::TestBFS::test_two_step_optimal",                1),
    ("BFS: solução ótima — caso médio",                "tests/test_algorithms.py::TestBFS::test_medium_optimal",                  1),
    ("BFS: detecta estado insolúvel",                  "tests/test_algorithms.py::TestBFS::test_unsolvable",                      1),
    ("BFS: métricas coerentes",                        "tests/test_algorithms.py::TestBFS::test_metrics_generated_ge_expanded",   1),

    # DFS — 6 pts
    ("DFS: encontra solução trivial (0 passos)",        "tests/test_algorithms.py::TestDFS::test_trivial",                         1),
    ("DFS: solução correta — 1 passo",                 "tests/test_algorithms.py::TestDFS::test_one_step_finds_solution",         1),
    ("DFS: solução correta — 2 passos",                "tests/test_algorithms.py::TestDFS::test_two_step_finds_solution",         1),
    ("DFS: detecta estado insolúvel dentro do limite", "tests/test_algorithms.py::TestDFS::test_unsolvable_within_limit",         1),
    ("DFS: respeita depth_limit",                      "tests/test_algorithms.py::TestDFS::test_depth_limit_respected",           1),
    ("DFS: métricas coerentes",                        "tests/test_algorithms.py::TestDFS::test_metrics_nodes_expanded_positive", 1),

    # A* — 9 pts
    ("A*: encontra solução trivial (0 passos)",         "tests/test_algorithms.py::TestAStar::test_trivial",                       1),
    ("A*: solução correta (caminho válido)",            "tests/test_algorithms.py::TestAStar::test_one_step_correct",              1),
    ("A*: solução ótima — 1 passo",                    "tests/test_algorithms.py::TestAStar::test_one_step_optimal",              1),
    ("A*: solução ótima — 2 passos",                   "tests/test_algorithms.py::TestAStar::test_two_step_optimal",              1),
    ("A*: solução ótima — caso médio",                 "tests/test_algorithms.py::TestAStar::test_medium_optimal",                1),
    ("A*: detecta estado insolúvel",                   "tests/test_algorithms.py::TestAStar::test_unsolvable",                    1),
    ("A*: concordância com BFS no custo ótimo",        "tests/test_algorithms.py::TestAStar::test_astar_optimal_equals_bfs",      1),
    ("A*: heurística admissível (expande menos)",      "tests/test_algorithms.py::TestAStar::test_astar_expands_fewer_nodes_than_bfs", 1),
    ("A*: métricas coerentes",                         "tests/test_algorithms.py::TestAStar::test_actions_match_depth",           1),
]

TOTAL = sum(pts for _, _, pts in RUBRIC)
assert TOTAL == 26, f"Rubrica soma {TOTAL}, esperado 26"

# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------

def run_test(test_id: str) -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_id, "--tb=no", "-q"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def main():
    print(f"\n{'='*60}")
    print(f"  AVALIAÇÃO AUTOMÁTICA — 8-Puzzle")
    print(f"{'='*60}\n")

    score = 0
    sections = {"State": [], "BFS": [], "DFS": [], "A*": []}

    for label, test_id, pts in RUBRIC:
        passed = run_test(test_id)
        earned = pts if passed else 0
        score += earned
        status = "✔" if passed else "✘"
        section = label.split(":")[0]
        sections[section].append((label, status, earned, pts))

    for section, items in sections.items():
        sec_earned = sum(e for _, _, e, _ in items)
        sec_total  = sum(t for _, _, _, t in items)
        print(f"── {section} ({sec_earned}/{sec_total} pts) " + "─"*30)
        for label, status, earned, pts in items:
            name = label.split(": ", 1)[1]
            print(f"  {status}  {name:<50}  {earned}/{pts}")
        print()

    pct = score / TOTAL * 100
    print(f"{'='*60}")
    print(f"  NOTA FINAL: {score}/{TOTAL} pts  ({pct:.0f}%)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
