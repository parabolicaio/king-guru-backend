"""Level 3 (Intermediate, B1) lesson content, as data. See dsl.py and build.py."""
import importlib

LESSON_MODULES = [f"lesson{n:02d}" for n in range(1, 11)]


def load_lessons() -> list[dict]:
    """Every lesson spec that exists so far, in lesson order."""
    out = []
    for name in LESSON_MODULES:
        try:
            mod = importlib.import_module(f"{__name__}.{name}")
        except ModuleNotFoundError as e:
            if e.name == f"{__name__}.{name}":
                continue
            raise
        out.append(mod.LESSON)
    return sorted(out, key=lambda l: l["order"])
