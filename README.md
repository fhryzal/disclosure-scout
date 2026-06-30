# disclosure-scout

A categorized collection of search queries for finding responsible disclosure
policies, vulnerability disclosure programs (VDPs), and bug bounty pages — plus
adjacent recon queries for source-code leaks, cloud exposure, and API secrets.

The goal is discovery: who runs a program, where their policy lives, and whether
they pay. Most queries target programs that are **not** hosted on the big bounty
platforms, because direct programs tend to triage faster and see less duplicate
traffic.

## Layout

```
dorks/
  01-security-txt.txt         well-known security.txt contact files
  02-responsible-disclosure.txt  general VDP / policy landing pages
  03-monetary-reward.txt      programs that explicitly advertise payment
  04-crypto-web3.txt          DeFi / wallet / on-chain bounty pages
  05-regional.txt             EU-heavy regional disclosure (NL/UK/DE/BE/AU/BR/IN)
  06-gov-edu.txt              government and academic programs
  07-platform-leak.txt        programs hosted on big platforms but discoverable off-platform
  08-source-code-leak.txt     git/svn/env/backup exposure
  09-cloud-exposure.txt       S3 / GCS / Azure blob exposure
  10-api-secrets.txt          swagger / graphql / key material in public files
scout.py                      optional runner — reads the dork files and dispatches to a backend
docs/methodology.md           how to triage and what to do (and not do) with findings
```

## Usage

### By hand

Open any `dorks/*.txt`, pick a query, paste it into your search engine. Good
engines for dork syntax: Google, Bing, and [Exa](https://exa.ai) (semantic —
rephrase the dork as a natural sentence).

### With scout.py

```bash
# list ready-to-paste search URLs for every dork (no key needed)
python3 scout.py --backend links

# actually query Exa and filter out the big bounty platforms
EXA_API_KEY=your_key python3 scout.py --backend exa --num 10 --no-platforms

# one category, machine-readable
EXA_API_KEY=your_key python3 scout.py --backend exa --category 04-crypto-web3.txt --json
```

No keys are bundled. `scout.py` reads `EXA_API_KEY` or `BING_API_KEY` from the
environment and never stores them.

## Notes

- Dork syntax (`inurl:`, `intext:`, `site:`) is Google-flavored. Bing supports a
  subset. Exa is semantic — for Exa, treat each dork as a description of intent
  rather than a literal operator string.
- `--no-platforms` drops results whose domain matches HackerOne, Bugcrowd,
  Synack, Open Bug Bounty, Intigriti, YesWeHack, HackenProof, or Cobalt. Turn it
  off with `--platforms` if you want the full set.
- The leak/exposure categories (`08`–`10`) can surface live secrets or PII. If
  you hit something sensitive during recon, don't dig further — report the
  exposure to the owner and stop. See `docs/methodology.md`.

## Legal

Only test systems you are authorized to test. Read each program's policy and
rules of engagement before any active testing. Responsible disclosure is
cooperative: report privately, respect remediation windows, don't publish early.

## License

MIT — see [LICENSE](LICENSE).
