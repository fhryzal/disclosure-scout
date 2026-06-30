# Methodology

## How to use this kit

1. **Pick a category** that matches your goal.
   - Paid programs → `03-monetary-reward.txt`, `04-crypto-web3.txt`
   - Direct/self-hosted programs → `11-self-hosted.txt`
   - Breadth → `01-security-txt.txt`
   - Regional → `05-regional.txt`
   - Government/academic → `06-gov-edu.txt`
2. **Run the dorks** either by hand (paste into Google / your search engine of
   choice) or via `scout.py` with a backend.
3. **Filter the noise.** `scout.py --no-platforms` drops results pointing at the
   big bounty platforms so you see *direct* programs first. Direct programs are
   usually less saturated and triage faster.
4. **Read the policy page** before touching anything. Scope, reward table, and
   rules of engagement vary per program. Out-of-scope = no payout + possible
   bad blood.
5. **Stay passive until authorized.** Discovery (reading public pages) is fine.
   Active testing starts only after you confirm the target is in-scope and you
   understand the ROE.

## Triage signals

When ranking discovered programs, weigh:

- **Direct vs platform-hosted** — direct programs triage faster, less queue.
- **Self-hosted** — programs running their own bounty infrastructure
  (Bugheist, Flawd, in-house forms) often have lower duplicate density and
  more flexible reward negotiation.
- **Reward clarity** — pages that publish a reward table tend to actually pay.
- **Scope specificity** — narrow scope (one app, one API) is easier to exhaust
  than "all *.company.com".
- **Freshness** — a recently launched program has lower duplicate density. Look
  for a "launched" date or recent hall-of-fame entries.
- **Asset type** — transactional / financial / on-chain assets produce
  higher-impact findings than marketing sites.

## Self-hosted programs

Category `11-self-hosted.txt` targets programs that run their own disclosure
infrastructure without a platform middleman. These are valuable because:

- **Faster triage** — your report goes straight to the internal team.
- **Fewer duplicates** — less traffic than HackerOne/Bugcrowd programs.
- **Flexible rewards** — direct programs sometimes pay more for high-impact
  findings, especially in crypto/web3.

Look for:
- In-house submission forms (`/submit-vulnerability`, `/report-bug`)
- security.txt pointing to a direct email (not a platform URL)
- "Powered by" footers for open-source bounty platforms (Bugheist, Flawd, etc.)
- Language like "we run our own" or "in-house bug bounty"

## Legal & ethics

Only test systems you are authorized to test. Responsible disclosure is a
cooperative process: report privately, allow remediation time, never publish
before the program's disclosure window closes. If a page has no policy, treat
the target as off-limits for active testing — you can still note it for later.

Dorks in `08-source-code-leak.txt`, `09-cloud-exposure.txt`, and
`10-api-secrets.txt` can surface sensitive data. If you find live secrets or
exposed PII during recon, **do not download or explore further** — report the
exposure to the owner immediately and stop.
