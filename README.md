# OSS Repo Auditor

OSS Repo Auditor is a local repository hygiene checker for open-source
maintainers. It scans a project directory and produces a concise readiness
report for contribution, release, and security basics.

The first version checks for:

- README, license, contributing, and security policy files.
- CI workflow presence.
- Test directory presence.
- Package metadata for common ecosystems.
- Suspicious committed credential markers.
- Oversized or generated-looking files that may need review.

## Install

```bash
python -m pip install -e .
```

No runtime dependencies are required beyond Python 3.11+.

## Usage

```bash
python -m oss_repo_auditor .
python -m oss_repo_auditor . --format json
python -m oss_repo_auditor . --fail-under 80
```

`--fail-under` is useful in CI when a project wants to enforce a minimum
repository readiness score.

## Development

```bash
python -m unittest discover -s tests
python -m oss_repo_auditor examples/sample_project
```

## License

MIT
