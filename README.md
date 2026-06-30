# disclosure-scout

A categorized collection of search queries for finding responsible disclosure
policies, vulnerability disclosure programs (VDPs), and bug bounty pages — plus
adjacent recon queries for source-code leaks, cloud exposure, and API secrets.

The goal is discovery: who runs a program, where their policy lives, and whether
they pay. Most queries target programs that are **not** hosted on the big bounty
platforms, because direct programs tend to triage faster and see less duplicate
traffic.

---

## Table of Contents

- [Dork Categories](#dork-categories)
- [Usage](#usage)
  - [By Hand](#by-hand)
  - [With scout.py](#with-scoutpy)
- [Backends](#backends)
- [Platform Filtering](#platform-filtering)
- [Methodology](#methodology)
- [Legal & Ethics](#legal--ethics)
- [License](#license)

---

## Dork Categories

| File | Focus | Queries |
|------|-------|---------|
| `01-security-txt.txt` | `/.well-known/security.txt` contact files | 10 |
| `02-responsible-disclosure.txt` | General VDP / policy landing pages | 14 |
| `03-monetary-reward.txt` | Programs that explicitly advertise payment | 42 |
| `04-crypto-web3.txt` | DeFi / wallet / on-chain bounty pages | 59 |
| `05-regional.txt` | Regional disclosure (NL/UK/DE/BE/AU/BR/IN/SG/JP/KR) | 32 |
| `06-gov-edu.txt` | Government and academic programs | 9 |
| `07-platform-leak.txt` | Platform-hosted but discoverable off-platform | 8 |
| `08-source-code-leak.txt` | git/svn/env/backup exposure | 14 |
| `09-cloud-exposure.txt` | S3 / GCS / Azure blob exposure | 9 |
| `10-api-secrets.txt` | swagger / graphql / key material in public files | 12 |
| `11-self-hosted.txt` | Self-hosted bounty programs (no platform middleman) | 36 |
| `12-platforms.txt` | Big bounty platform programs (H1/BC/Immunefi/etc.) | 54 |

Query counts are approximate — the library grows over time.

## Layout

```
dorks/
  01-security-txt.txt           well-known security.txt contact files
  02-responsible-disclosure.txt general VDP / policy landing pages
  03-monetary-reward.txt        programs that explicitly advertise payment
  04-crypto-web3.txt            DeFi / wallet / on-chain bounty pages
  05-regional.txt               regional disclosure (NL/UK/DE/BE/AU/BR/IN/SG/JP/KR)
  06-gov-edu.txt                government and academic programs
  07-platform-leak.txt          platform-hosted but discoverable off-platform
  08-source-code-leak.txt       git/svn/env/backup exposure
  09-cloud-exposure.txt         S3 / GCS / Azure blob exposure
  10-api-secrets.txt            swagger / graphql / key material in public files
  11-self-hosted.txt            self-hosted bounty programs (direct payouts)
  12-platforms.txt              big bounty platform programs (H1/BC/Immunefi/etc.)
scout.py                        optional runner — reads the dork files and dispatches to a backend
docs/methodology.md             how to triage and what to do (and not do) with findings
```

## Usage

### By Hand

Open any `dorks/*.txt`, pick a query, paste it into your search engine. Good
engines for dork syntax: Google, Bing, and [Exa](https://exa.ai) (semantic —
rephrase the dork as a natural sentence).

### With scout.py

```bash
# list available categories
python3 scout.py --list

# list ready-to-paste Google search URLs for every dork (no key needed)
python3 scout.py --backend links

# use Bing search URLs instead
python3 scout.py --backend links --engine bing

# query the free no-key Exa MCP endpoint via mcporter (needs mcporter + exa server)
python3 scout.py --backend exa-mcp --num 10 --no-platforms

# query the paid Exa REST API and filter out the big bounty platforms
EXA_API_KEY=*** python3 scout.py --backend exa --num 10 --no-platforms

# one category, machine-readable
python3 scout.py --backend exa-mcp --category 04-crypto-web3.txt --json

# focus on self-hosted direct programs
python3 scout.py --backend exa-mcp --category 11-self-hosted.txt --json

# enumerate programs on a specific big platform
python3 scout.py --backend exa-mcp --category 12-platforms.txt --platforms --json

# include platform-hosted results (disables the default platform filter)
python3 scout.py --backend exa --platforms
```

No keys are bundled. `scout.py` reads `EXA_API_KEY` or `BING_API_KEY` from the
environment and never stores them.

## Backends

| Backend | Key required | Description |
|---------|-------------|-------------|
| `links` | None | Emits ready-to-paste search URLs (Google or Bing) |
| `exa-mcp` | None | Free Exa semantic search via mcporter CLI |
| `exa` | `EXA_API_KEY` | Paid Exa REST API, neural semantic search |
| `bing` | `BING_API_KEY` | Bing Web Search API |

## Platform Filtering

`--no-platforms` (on by default) drops results whose domain matches:

- HackerOne
- Bugcrowd
- Synack
- Open Bug Bounty
- Intigriti
- YesWeHack
- HackenProof
- Cobalt
- Immunefi

Use `--platforms` to include them.

## Methodology

See [`docs/methodology.md`](docs/methodology.md) for the full triage guide:
how to rank discovered programs, what signals to weigh, and what to do (and not
do) with sensitive findings.

The leak/exposure categories (`08`–`10`) can surface live secrets or PII. If
you hit something sensitive during recon, don't dig further — report the
exposure to the owner and stop.

## Legal & Ethics

Only test systems you are authorized to test. Read each program's policy and
rules of engagement before any active testing. Responsible disclosure is
cooperative: report privately, respect remediation windows, don't publish early.

## License

MIT — see [LICENSE](LICENSE).
