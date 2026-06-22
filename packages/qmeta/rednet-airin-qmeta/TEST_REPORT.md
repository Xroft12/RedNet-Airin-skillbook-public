# Test report

Command:

```powershell
uv run --with pytest python -m pytest -q
```

Result:

```text
8 passed
```

Smoke examples checked:

```powershell
uv run python examples/demo_answer.py
uv run python examples/demo_skill.py
```

Packaging checks:

```powershell
uv run --with build python -m build . --outdir dist
```

The wheel and sdist are expected to include:

- `manifest.json`
- `CHANGELOG.md`
- `TEST_REPORT.md`
- `docs/*.md`
- `skills/*.yaml`
- `config/*.json`
- `examples/*.py`
- `src/hermes_airin/skill_cards/*.json`
