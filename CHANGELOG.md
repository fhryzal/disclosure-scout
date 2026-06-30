# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [1.1.0] - 2026-06-30

### Added
- New category: `11-self-hosted.txt` — self-hosted bounty programs (36 queries)
- New category: `12-platforms.txt` — big bounty platform programs (54 queries)
- `--list` flag to enumerate categories with query counts
- `--engine` flag for `links` backend (Google or Bing)
- `--platforms` flag to include platform-hosted results (disables default filter)
- Immunefi added to platform deny-list
- CONTRIBUTING.md
- Expanded `04-crypto-web3.txt`: 24 → 59 queries (new chains, DeFi primitives, audit firms)
- Expanded `03-monetary-reward.txt`: 18 → 42 queries (crypto payouts, reward tiers, payment language)
- Expanded `05-regional.txt`: 16 → 32 queries (SG/JP/KR/ID/TH/MX, local-language queries)

### Changed
- README redesigned: badges, collapsible sections, GitHub alerts, CLI flags table
- LICENSE copyright updated to GitHub handle
- `.gitignore` expanded: env/secrets/venv/editor patterns
- `docs/methodology.md`: added self-hosted programs section

### Fixed
- Removed 7 cross-file duplicate queries
- README query counts now match actual file contents
- `scout.py` docstring cleaned (removed personal attribution)
- `scout.py` gracefully handles nonexistent category files

## [1.0.0] - 2026-06-30

### Added
- Initial release
- 10 dork categories (268 queries total)
- `scout.py` runner with 4 backends: `links`, `exa`, `exa-mcp`, `bing`
- `docs/methodology.md` triage guide
- Platform deny-list: HackerOne, Bugcrowd, Synack, Open Bug Bounty, Intigriti, YesWeHack, HackenProof, Cobalt
- `--no-platforms` filter (on by default)
- `--json` output mode
- MIT license

[Unreleased]: https://github.com/fhryzal/disclosure-scout/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/fhryzal/disclosure-scout/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/fhryzal/disclosure-scout/releases/tag/v1.0.0
