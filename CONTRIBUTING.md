# Contributing to Yankı

Thank you for contributing to **Yankı** (`yanki`), our deterministic citation verification and multilingual quote-grounding engine for generative AI pipelines.

## Development Setup

```bash
git clone https://github.com/mevlanayalcin/yanki.git
cd yanki
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests & Verification Benchmarks

Every pull request must pass the unit test suite and the 24-case deterministic offline evaluation harness:

```bash
pytest -q
python3 -m yanki.eval --offline --strict-thresholds
```

## Pull Request Guidelines

- Keep the core `yanki` package dependency-light (standard library Python 3.10+).
- Preserve 1:1 Unicode character offset invariants when modifying normalization (`src/yanki/normalize.py`) or alignment (`src/yanki/verify.py`).
- Add regression test cases under `tests/` for any new edge case in quote span matching, multi-source attribution, or abstention logic.
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Contact

For security disclosures or maintainer questions, email `info@mevlanayalcin.com.tr`.
