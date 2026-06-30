# Contributing

Contributions are welcome — new dork queries, bug fixes, backend improvements, and category ideas.

## Adding Dork Queries

1. Pick the right category file in `dorks/`. If none fits, create a new `NN-name.txt` file (zero-padded number, lowercase, hyphenated).

2. Follow the existing format:
   ```
   # Section header (optional but recommended for grouping)
   inurl:/example "keyword" -site:example.com
   ```

3. Rules:
   - One query per line.
   - Lines starting with `#` are comments (skipped by `scout.py`).
   - Blank lines are ignored.
   - Google-flavored syntax (`inurl:`, `intext:`, `site:`, `filetype:`).
   - Use `-site:` to exclude noise (platforms, your own domains, etc.).
   - Check for duplicates — run `python3 scout.py --list` and grep existing files before adding.

4. Test your queries:
   ```bash
   # verify the category loads
   python3 scout.py --backend links --category your-category.txt

   # verify no cross-file duplicates
   grep -r "your new query" dorks/
   ```

## Adding a New Category

1. Create `dorks/NN-name.txt` with a header comment explaining the focus.
2. Add the file to the README category table and layout section.
3. Update the query count in the README.
4. Run `python3 scout.py --list` to verify it appears.

## Improving scout.py

- Keep it dependency-light. `requests` is the only external import, and only inside backend functions (lazy import).
- No keys hardcoded anywhere. Read from environment variables.
- Test all backends before submitting:
  ```bash
  python3 scout.py --backend links
  python3 scout.py --backend links --engine bing
  python3 scout.py --list
  ```

## Style

- Dork files: Google-flavored syntax, lowercase where possible, quotes around multi-word phrases.
- Python: PEP 8, 4-space indent, no unnecessary complexity.
- README: use GitHub-flavored markdown (tables, `<details>`, alerts).

## Pull Requests

- Keep commits focused — one category or one fix per PR.
- Write clear commit messages (what changed, why).
- Don't bundle API keys, tokens, or personal data.

## Reporting Issues

Open an issue if:
- A dork produces consistently broken results (search engine changed syntax).
- `scout.py` crashes on a valid input.
- A category is missing queries it should have.

Include the command you ran and the output.
