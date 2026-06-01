from pathlib import Path

from scripts.run_review import build_review_prompt, resolve_target

ROOT = Path(__file__).resolve().parents[1]


def test_resolve_target_accepts_existing_local_path():
    target = resolve_target(str(ROOT / "examples" / "vulnerable-python-api"))

    assert target.kind == "local"
    assert target.path.name == "vulnerable-python-api"


def test_build_review_prompt_mentions_authorized_static_review_and_target():
    target = resolve_target(str(ROOT / "examples" / "vulnerable-python-api"))

    prompt = build_review_prompt(target=target, agent="codex", authorized=True)

    assert "authorized static security review" in prompt
    assert "Do not perform live exploitation" in prompt
    assert "vulnerable-python-api" in prompt
    assert "Markdown and JSON" in prompt
