"""Exibe e valida os parâmetros do pipeline customizado e grava params.json."""

import json
import os
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
IGNORED_DIRS = {"venv", ".venv", "__pycache__"}


def parse_density(raw):
    value = float(raw)
    return int(value) if value.is_integer() else value


def discover_tests():
    return sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*_test.py")
        if not any(part in IGNORED_DIRS or part.startswith(".")
                   for part in path.relative_to(ROOT).parts[:-1])
    )


def invalid_tests(test_files):
    invalid = []
    for test in test_files:
        path = (ROOT / test.split("::")[0]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            invalid.append(test)
    return invalid


if __name__ == '__main__':

    test_files = os.environ.get("TEST_FILES", "").split()

    params = {
        "density": parse_density(os.environ.get("DENSITY", "254")),
        "mode": os.environ.get("MODE", "automatico"),
        "test_files": test_files,
        "branch": os.environ.get("CI_COMMIT_REF_NAME", "local"),
        "commit": os.environ.get("CI_COMMIT_SHORT_SHA", "local"),
        "triggered_by": os.environ.get("GITLAB_USER_LOGIN", os.environ.get("USER", "local")),
        "source": os.environ.get("CI_PIPELINE_SOURCE", "local"),
    }

    shown_tests = test_files or [f"{t} (auto)" for t in discover_tests()]

    print("=" * 50)
    print(" Parâmetros selecionados")
    print("=" * 50)
    print(f" Branch        : {params['branch']}")
    print(f" Commit        : {params['commit']}")
    print(f" Disparado por : {params['triggered_by']} ({params['source']})")
    print(f" Density       : {params['density']}")
    print(f" Mode          : {params['mode']}")
    print(" Test files    :")
    for test in shown_tests:
        print(f"   - {test}")
    print("=" * 50)

    invalid = invalid_tests(test_files)
    if invalid:
        print(f"ERRO: teste(s) não encontrado(s) na branch '{params['branch']}':")
        for test in invalid:
            print(f"   - {test}")
        sys.exit(1)

    Path("params.json").write_text(json.dumps(params, indent=2, ensure_ascii=False) + "\n")
    print("params.json gerado")
