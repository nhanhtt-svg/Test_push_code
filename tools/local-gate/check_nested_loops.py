import argparse
import ast
import re
import sys
from pathlib import Path

import yaml


def load_cfg(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def is_ignored(relpath: str, ignore_patterns: list[str]) -> bool:
    return any(re.search(p, relpath) for p in (ignore_patterns or []))


class LoopDepthVisitor(ast.NodeVisitor):

    def __init__(self, include_while: bool):
        self.include_while = include_while
        self.depth = 0
        self.violations: list[tuple[int, int]] = []  # (line, depth)

    def _enter(self, lineno: int):
        self.depth += 1
        self.violations.append((lineno, self.depth))

    def _exit(self):
        self.depth -= 1

    def visit_For(self, node: ast.For):
        self._enter(getattr(node, "lineno", 0))
        self.generic_visit(node)
        self._exit()

    def visit_While(self, node: ast.While):
        if self.include_while:
            self._enter(getattr(node, "lineno", 0))
            self.generic_visit(node)
            self._exit()
        else:
            self.generic_visit(node)


def check_file(path: Path, max_depth: int, include_while: bool) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{path}: parse error: {e}"]

    v = LoopDepthVisitor(include_while=include_while)
    v.visit(tree)

    errors = []
    for lineno, depth in v.violations:
        if depth > max_depth:
            errors.append(
                f"{path}:{lineno}: nested loop depth={depth} exceeds max_depth={max_depth}")
    return errors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("files", nargs="*")  # pre-commit sẽ truyền staged files
    args = ap.parse_args(argv)

    cfg = load_cfg(args.config)
    ignore = cfg.get("ignore", [])
    rule = cfg.get("nested_loops", {})
    max_depth = int(rule.get("max_depth", 2))
    include_while = bool(rule.get("include_while", True))

    all_errors: list[str] = []
    for f in args.files:
        rel = f.replace("\\", "/")
        if is_ignored(rel, ignore):
            continue
        p = Path(f)
        if p.suffix != ".py" or not p.exists():
            continue
        all_errors.extend(check_file(p, max_depth, include_while))

    if all_errors:
        print("❌ custom rule failed: nested_loops")
        print("\n".join(all_errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
