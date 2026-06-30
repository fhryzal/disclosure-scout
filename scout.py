#!/usr/bin/env python3
"""disclosure-scout — read categorized dork files and dispatch to a search backend.

Credited by Bores. MIT license.

No keys are hardcoded anywhere. Pick a backend and supply its key via env:
  EXA_API_KEY   -> query Exa (https://exa.ai) REST API, neural semantic search
  BING_API_KEY  -> query Bing Web Search API
  (no key)      -> --backend exa-mcp uses the free no-key Exa MCP endpoint via
                   the mcporter CLI (requires mcporter installed + exa server
                   configured; MCPORTER_CONFIG defaults to ~/.mcporter/mcporter.json)
With no key and no mcporter, --backend links emits ready-to-paste search URLs.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import pathlib

PLATFORM_DENY = (
    "hackerone.com", "bugcrowd.com", "synack.com", "openbugbounty.org",
    "intigriti.com", "yeswehack.com", "hackenproof.com", "cobalt.io",
    "responsibledisclosure.com",
)


class DorkLibrary:
    """Loads dork query strings from dorks/*.txt, skipping comment lines."""

    def __init__(self, root):
        self.root = pathlib.Path(root)
        self.dir = self.root / "dorks"

    def categories(self):
        return sorted(p.name for p in self.dir.glob("*.txt"))

    def load(self, name=None):
        out = {}
        files = [self.dir / name] if name else sorted(self.dir.glob("*.txt"))
        for f in files:
            queries = []
            for raw in f.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                queries.append(line)
            out[f.name] = queries
        return out


def google_url(q):
    return "https://www.google.com/search?q=" + urllib.parse.quote(q)


def domain_of(url):
    m = re.match(r"https?://([^/]+)/", url)
    return (m.group(1) if m else url).replace("www.", "").lower()


def is_platform(domain):
    return any(p in domain for p in PLATFORM_DENY)


def run_exa(query, n, key):
    import requests
    r = requests.post(
        "https://api.exa.ai/search",
        headers={"x-api-key": key, "Content-Type": "application/json"},
        json={"query": query, "numResults": n, "type": "neural"},
        timeout=30,
    )
    r.raise_for_status()
    return [{"title": x.get("title", ""), "url": x.get("url", "")}
            for x in r.json().get("results", [])]


def run_bing(query, n, key):
    import requests
    r = requests.get(
        "https://api.bing.microsoft.com/v7.0/search",
        headers={"Ocp-Apim-Subscription-Key": key},
        params={"q": query, "count": n},
        timeout=30,
    )
    r.raise_for_status()
    return [{"title": x.get("name", ""), "url": x.get("url", "")}
            for x in r.json().get("webPages", {}).get("value", [])]


def run_exa_mcp(query, n, _key):
    """Query Exa via the free no-key MCP endpoint using the mcporter CLI.

    Requires mcporter installed and the exa server configured
    (set MCPORTER_CONFIG, defaults to ~/.mcporter/mcporter.json).
    """
    import subprocess
    env = dict(os.environ)
    env.setdefault("MCPORTER_CONFIG", str(pathlib.Path.home() / ".mcporter" / "mcporter.json"))
    proc = subprocess.run(
        ["mcporter", "call", "exa.web_search_exa", f"query={query}", f"numResults={str(n)}"],
        capture_output=True, text=True, env=env, timeout=45,
    )
    hits = []
    cur = {}
    for line in proc.stdout.splitlines():
        if line.startswith("Title: "):
            if "url" in cur:
                hits.append(cur)
            cur = {"title": line[7:].strip()}
        elif line.startswith("URL: "):
            cur["url"] = line[5:].strip()
    if "url" in cur:
        hits.append(cur)
    return hits


BACKENDS = {"exa": run_exa, "bing": run_bing, "exa-mcp": run_exa_mcp}


def main():
    ap = argparse.ArgumentParser(description="dispatch disclosure dorks to a search backend")
    ap.add_argument("--category", help="dork file in dorks/ (default: all)")
    ap.add_argument("--backend", choices=["links", "exa", "exa-mcp", "bing"], default="links")
    ap.add_argument("--num", type=int, default=10, help="results per dork")
    ap.add_argument("--no-platforms", action="store_true", help="filter known bounty platforms (default on)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    here = pathlib.Path(__file__).resolve().parent
    library = DorkLibrary(here).load(args.category)

    key = ""
    if args.backend in ("exa", "bing"):
        env_var = "EXA_API_KEY" if args.backend == "exa" else "BING_API_KEY"
        key = os.environ.get(env_var, "")
        if not key:
            print(f"set {env_var} env var to use --backend {args.backend}", file=sys.stderr)
            sys.exit(2)

    collected = {}
    for fname, queries in library.items():
        for q in queries:
            if args.backend == "links":
                collected.setdefault(fname, []).append({"dork": q, "url": google_url(q)})
                continue
            try:
                hits = BACKENDS[args.backend](q, args.num, key)
            except Exception as exc:
                hits = []
                sys.stderr.write(f"[{fname}] {q[:60]} -> {exc}\n")
            if args.no_platforms:
                hits = [h for h in hits if not is_platform(domain_of(h["url"]))]
            collected.setdefault(fname, []).append({"dork": q, "hits": hits})

    if args.json:
        print(json.dumps(collected, indent=2))
        return

    for fname, items in collected.items():
        print(f"\n## {fname}")
        for it in items:
            if args.backend == "links":
                print(f"  {it['dork']}")
                print(f"    {it['url']}")
            else:
                print(f"  [{it['dork']}]")
                for h in it["hits"]:
                    print(f"    {domain_of(h['url'])}  {h.get('title','')[:70]}")


if __name__ == "__main__":
    main()
