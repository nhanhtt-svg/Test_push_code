import argparse
import ast
import re
import sys
from pathlib import Path

import yaml


def load_cfg(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def is_match_any(path: str, patterns: list[str]) -> bool:
    return any(re.search(p, path) for p in (patterns or []))


class PrintCallVisitor(ast.NodeVisitor):

    def __init__(self):
        self.lines: list[int] = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.lines.append(getattr(node, "lineno", 0))
        self.generic_visit(node)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("files", nargs="*")
    args = ap.parse_args(argv)

    cfg = load_cfg(args.config)
    ignore = cfg.get("ignore", [])
    rule = cfg.get("no_print", {})
    if not rule.get("enabled", True):
        return 0
    allow_in = rule.get("allow_in", [])

    errors = []
    for f in args.files:
        rel = f.replace("\\", "/")
        if is_match_any(rel, ignore) or is_match_any(rel, allow_in):
            continue
        p = Path(f)
        if p.suffix != ".py" or not p.exists():
            continue

        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{rel}: parse error: {e}")
            continue

        v = PrintCallVisitor()
        v.visit(tree)
        for ln in v.lines:
            errors.append(f"{rel}:{ln}: print() is not allowed (use logging)")

    if errors:
        print("❌ custom rule failed: no_print")
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
