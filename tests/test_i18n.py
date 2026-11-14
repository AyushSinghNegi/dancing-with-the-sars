"""Every on-screen string has a German version with the same {placeholders}. Reads the source files only, so it
runs without Streamlit installed."""
import ast
import glob
import re
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app"


def _assigned(path, name):
    for node in ast.parse((APP / path).read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)


DE, DE_T, DE_E = (_assigned("lib/i18n_de.py", n) for n in ("DE", "DE_T", "DE_E"))
T, E = _assigned("lib/ui.py", "T"), _assigned("lib/evidence.py", "E")


def _ph(s):
    return sorted(set(re.findall(r"\{(\w+)", s)))


def test_every_tr_string_has_german():
    missing = []
    for f in glob.glob(str(APP / "**" / "*.py"), recursive=True):
        for n in ast.walk(ast.parse(Path(f).read_text(encoding="utf-8"))):
            if isinstance(n, ast.Call) and (getattr(n.func, "attr", None) or getattr(n.func, "id", None)) == "tr" \
                    and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                if n.args[0].value not in DE:
                    missing.append((Path(f).name, n.lineno, n.args[0].value[:60]))
    assert not missing, missing


def test_keyed_strings_have_german():
    assert not [k for k in T if k not in DE_T]
    assert not [k for k in E if k not in DE_E]


def test_placeholders_match():
    bad = [k for k, v in DE.items() if _ph(k) != _ph(v)]
    bad += [k for k, v in DE_T.items() if k in T and _ph(T[k]["en"]) != _ph(v)]
    bad += [k for k, v in DE_E.items() if k in E and _ph(E[k]["en"]) != _ph(v)]
    assert not bad, bad


def test_german_story_has_same_steps_and_placeholders():
    content = APP.parent / "content"
    strip = lambda p: re.sub(r"<!--.*?-->", "", p.read_text(encoding="utf-8"), flags=re.S)
    en, de = strip(content / "story.md"), strip(content / "story.de.md")
    assert len(re.findall(r"^## ", en, re.M)) == len(re.findall(r"^## ", de, re.M))
    assert _ph(en) == _ph(de)
