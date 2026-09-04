"""Refresh data/repos.json from the GitHub API.

Run `make refresh` and every asset and the project index rebuild from what the
account actually contains, rather than from anything I typed.
"""
from __future__ import annotations

import subprocess
import sys

from common import DATA

QUERY = """
{ user(login:"adarshcod30") { repositories(first:100, ownerAffiliations:OWNER,
                                           privacy:PUBLIC) { nodes {
  name description createdAt pushedAt isFork stargazerCount
  primaryLanguage{name}
  languages(first:6, orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}
  repositoryTopics(first:12){nodes{topic{name}}}
} } } }
"""


def main() -> int:
    try:
        out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}"],
                             capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        print("gh is not installed - keeping the existing snapshot", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        print(f"gh failed: {e.stderr.strip()[:200]}", file=sys.stderr)
        return 1
    DATA.write_text(out)
    print(f"wrote {DATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
