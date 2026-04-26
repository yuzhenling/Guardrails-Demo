from __future__ import annotations

import os
import re
from pathlib import Path

from dotenv import load_dotenv


def _replace_value(line: str, key: str, value: str) -> str:
    indent = re.match(r"^(\s*)", line).group(1)
    escaped = value.replace('"', '\\"')
    return f'{indent}{key}: "{escaped}"\n'


def parameterize_main_model(config_path: Path) -> None:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    lines = config_path.read_text(encoding="utf-8").splitlines(keepends=True)
    in_main_model = False

    main_engine = os.getenv("MAIN_MODEL_ENGINE")
    main_model = os.getenv("MAIN_MODEL_NAME") or os.getenv("MAIN_MODEL")
    main_base_url = os.getenv("MAIN_MODEL_BASE_URL")

    for i, line in enumerate(lines):
        if re.match(r"^\s*-\s*type:\s*main\s*$", line):
            in_main_model = True
            continue

        if in_main_model and re.match(r"^\s*-\s*type:\s*\w+", line):
            break

        if not in_main_model:
            continue

        if main_engine and re.match(r"^\s*engine:\s*", line):
            lines[i] = _replace_value(line, "engine", main_engine)
        elif main_model and re.match(r"^\s*model:\s*", line):
            lines[i] = _replace_value(line, "model", main_model)
        elif main_base_url and re.match(r"^\s*base_url:\s*", line):
            lines[i] = _replace_value(line, "base_url", main_base_url)

    config_path.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".env")

    config_path = project_root / "config" / "mybot" / "config.yml"
    parameterize_main_model(config_path)
    print(f"Main model config updated from environment: {config_path}")


if __name__ == "__main__":
    main()
