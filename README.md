<div align="center">

# disclosure-scout

**Categorized search queries for finding bug bounty programs, VDPs, and disclosure policies — plus adjacent recon dorks for source-code leaks, cloud exposure, and API secrets.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Queries: 299](https://img.shields.io/badge/Dork%20Queries-299-green.svg)](#dork-categories)
[![Categories: 12](https://img.shields.io/badge/Categories-12-orange.svg)](#dork-categories)
[![No Keys Bundled](https://img.shields.io/badge/Keys-None%20Bundled-success.svg)](#backends)

</div>

---

> **The goal is discovery:** who runs a program, where their policy lives, and whether they pay.
>
> Most queries target programs that are **not** hosted on the big bounty platforms, because direct programs tend to triage faster and see less duplicate traffic.

---

## Table of Contents

- [Dork Categories](#dork-categories)
- [Repository Layout](#repository-layout)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Backends](#backends)
- [Platform Filtering](#platform-filtering)
- [Methodology](#methodology)
- [Legal & Ethics](#legal--ethics)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Dork Categories

| # | File | Focus | Queries |
|:---:|------|-------|:---:|
| 01 | [`01-security-txt.txt`](dorks/01-security-txt.txt) | `/.well-known/security.txt` contact files | 10 |
| 02 | [`02-responsible-disclosure.txt`](dorks/02-responsible-disclosure.txt) | General VDP / policy landing pages | 14 |
| 03 | [`03-monetary-reward.txt`](dorks/03-monetary-reward.txt) | Programs that explicitly advertise payment | 42 |
| 04 | [`04-crypto-web3.txt`](dorks/04-crypto-web3.txt) | DeFi / wallet / on-chain bounty pages | 59 |
| 05 | [`05-regional.txt`](dorks/05-regional.txt) | Regional disclosure (NL/UK/DE/BE/AU/BR/IN/SG/JP/KR) | 32 |
| 06 | [`06-gov-edu.txt`](dorks/06-gov-edu.txt) | Government and academic programs | 9 |
| 07 | [`07-platform-leak.txt`](dorks/07-platform-leak.txt) | Platform-hosted but discoverable off-platform | 8 |
| 08 | [`08-source-code-leak.txt`](dorks/08-source-code-leak.txt) | git/svn/env/backup exposure | 14 |
| 09 | [`09-cloud-exposure.txt`](dorks/09-cloud-exposure.txt) | S3 / GCS / Azure blob exposure | 9 |
| 10 | [`10-api-secrets.txt`](dorks/10-api-secrets.txt) | swagger / graphql / key material in public files | 12 |
| 11 | [`11-self-hosted.txt`](dorks/11-self-hosted.txt) | Self-hosted bounty programs (no platform middleman) | 36 |
| 12 | [`12-platforms.txt`](dorks/12-platforms.txt) | Big bounty platform programs (H1/BC/Immunefi/etc.) | 54 |
| | | **Total** | **299** |

> [!NOTE]
> Query counts grow over time. Run `python3 scout.py --list` for live counts.

---

## Repository Layout

```
disclosure-scout/
├── dorks/
│   ├── 01-security-txt.txt
│   ├── 02-responsible-disclosure.txt
│   ├── 03-monetary-reward.txt
│   ├── 04-crypto-web3.txt
│   ├── 05-regional.txt
│   ├── 06-gov-edu.txt
│   ├── 07-platform-leak.txt
│   ├── 08-source-code-leak.txt
│   ├── 09-cloud-exposure.txt
│   ├── 10-api-secrets.txt
│   ├── 11-self-hosted.txt
│   └── 12-platforms.txt
├── docs/
│   └── methodology.md
├── scout.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## Quick Start

```bash
git clone https://github.com/fhryzal/disclosure-scout.git
cd disclosure-scout

# list all categories
python3 scout.py --list

# generate ready-to-paste Google search URLs (no key needed)
python3 scout.py --backend links

# focus on self-hosted direct programs
python3 scout.py --backend links --category 11-self-hosted.txt
```

---

## Usage

### By Hand

Open any [`dorks/*.txt`](dorks) file, pick a query, paste it into your search engine.

Recommended engines for dork syntax:

| Engine | Syntax Support | Notes |
|--------|:---:|-------|
| Google | Full | Best for `inurl:`, `intext:`, `site:`, `filetype:` |
| Bing | Partial | Supports `site:`, `filetype:`, limited `inurl:` |
| [Exa](https://exa.ai) | Semantic | Rephrase the dork as a natural sentence |

### With scout.py

<details>
<summary><b>Click to expand usage examples</b></summary>

```bash
# list available categories
python3 scout.py --list

# list ready-to-paste Google search URLs for every dork (no key needed)
python3 scout.py --backend links

# use Bing search URLs instead
python3 scout.py --backend links --engine bing

# query the free no-key Exa MCP endpoint via mcporter
# (requires mcporter installed + exa server configured)
python3 scout.py --backend exa-mcp --num 10 --no-platforms

# query the paid Exa REST API and filter out big bounty platforms
EXA_API_KEY=xxx python3 scout.py --backend exa --num 10 --no-platforms

# one category, machine-readable JSON
python3 scout.py --backend exa-mcp --category 04-crypto-web3.txt --json

# focus on self-hosted direct programs
python3 scout.py --backend exa-mcp --category 11-self-hosted.txt --json

# enumerate programs on a specific big platform
python3 scout.py --backend exa-mcp --category 12-platforms.txt --platforms --json

# include platform-hosted results (disables the default platform filter)
python3 scout.py --backend exa --platforms
```

</details>

> [!IMPORTANT]
> No keys are bundled. `scout.py` reads `EXA_API_KEY` or `BING_API_KEY` from the environment and never stores them.

### CLI Flags

| Flag | Description | Default |
|------|-------------|:---:|
| `--list` | List available dork categories and exit | |
| `--backend` | Search backend: `links`, `exa`, `exa-mcp`, `bing` | `links` |
| `--engine` | Search engine for `links` backend: `google`, `bing` | `google` |
| `--category` | Dork file to use (default: all) | all |
| `--num` | Results per dork | `10` |
| `--no-platforms` | Filter known bounty platforms | on |
| `--platforms` | Include platform-hosted results | off |
| `--json` | Emit machine-readable JSON | off |

---

## Backends

| Backend | Key Required | Description |
|---------|:---:|-------------|
| `links` | — | Emits ready-to-paste search URLs (Google or Bing) |
| `exa-mcp` | — | Free Exa semantic search via mcporter CLI |
| `exa` | `EXA_API_KEY` | Paid Exa REST API, neural semantic search |
| `bing` | `BING_API_KEY` | Bing Web Search API |

<details>
<summary><b>Backend setup details</b></summary>

**`links`** — No setup required. Generates search URLs you can click or paste.

**`exa-mcp`** — Requires [mcporter](https://github.com/stainless-sdks/mcporter) installed and the Exa MCP server configured:

```bash
pip install mcporter
mcporter add exa
```

Set `MCPORTER_CONFIG` (defaults to `~/.mcporter/mcporter.json`).

**`exa`** — Get an API key at [exa.ai](https://exa.ai), then:

```bash
export EXA_API_KEY="your-key-here"
python3 scout.py --backend exa --num 10
```

**`bing`** — Get a key from the [Azure Portal](https://portal.azure.com/), then:

```bash
export BING_API_KEY="your-key-here"
python3 scout.py --backend bing --num 10
```

</details>

---

## Platform Filtering

`--no-platforms` is **on by default** and drops results whose domain matches:

<details>
<summary><b>Filtered platforms (click to expand)</b></summary>

| Platform | Domain |
|----------|--------|
| HackerOne | `hackerone.com` |
| Bugcrowd | `bugcrowd.com` |
| Synack | `synack.com` |
| Open Bug Bounty | `openbugbounty.org` |
| Intigriti | `intigriti.com` |
| YesWeHack | `yeswehack.com` |
| HackenProof | `hackenproof.com` |
| Cobalt | `cobalt.io` |
| Immunefi | `immunefi.com` |

</details>

Use `--platforms` to include them.

---

## Methodology

See [`docs/methodology.md`](docs/methodology.md) for the full triage guide:

- How to rank discovered programs
- What signals to weigh (direct vs hosted, reward clarity, scope, freshness)
- Self-hosted program discovery tactics
- What to do (and not do) with sensitive findings

> [!WARNING]
> The leak/exposure categories (`08`–`10`) can surface live secrets or PII. If you hit something sensitive during recon, **do not dig further** — report the exposure to the owner and stop.

---

## Legal & Ethics

Only test systems you are authorized to test. Read each program's policy and rules of engagement before any active testing. Responsible disclosure is cooperative:

- Report privately
- Respect remediation windows
- Don't publish before the program's disclosure window closes
- If a page has no policy, treat the target as off-limits for active testing

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on adding dork queries, new categories, and improving `scout.py`.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for version history.

---

## License

MIT — see [LICENSE](LICENSE).
