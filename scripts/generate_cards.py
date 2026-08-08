#!/usr/bin/env python3
"""Render the profile's language card as a self-hosted SVG.

Nothing here depends on a third-party rendering service: the data comes from
GitHub's GraphQL API and the SVG is emitted locally, so the card cannot break
because someone else's shared instance is rate limited.

Markup and styling languages are excluded on purpose -- committed build output
and templates otherwise drown out the languages actually written by hand.

Usage:
    GH_TOKEN=... GH_LOGIN=octocat python generate_cards.py --out dist
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from xml.sax.saxutils import escape

API = "https://api.github.com/graphql"

# Excluded from the breakdown: generated bundles and templates dominate these.
EXCLUDED = {"HTML", "CSS", "SCSS", "Sass", "Less", "Stylus", "Roff", "Batchfile"}

THEMES = {
    "dark": {
        "bg": "#0D1117",
        "border": "#30363D",
        "title": "#58A6FF",
        "label": "#8B949E",
        "value": "#C9D1D9",
        "track": "#21262D",
    },
    "light": {
        "bg": "#FFFFFF",
        "border": "#D0D7DE",
        "title": "#0969DA",
        "label": "#57606A",
        "value": "#1F2328",
        "track": "#EAEEF2",
    },
}

FONT = "'Segoe UI',Ubuntu,'Helvetica Neue',Helvetica,sans-serif"

QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes {
        languages(first: 20, orderBy: { field: SIZE, direction: DESC }) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def gql(token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-card-generator",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        sys.exit(f"GraphQL HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:400]}")

    if "errors" in payload:
        sys.exit(f"GraphQL errors: {payload['errors']}")
    return payload["data"]


def collect_languages(token: str, login: str) -> dict[str, tuple[int, str]]:
    totals: dict[str, tuple[int, str]] = {}
    cursor = None

    while True:
        repos = gql(token, QUERY, {"login": login, "cursor": cursor})["user"]["repositories"]
        for node in repos["nodes"]:
            for edge in node["languages"]["edges"]:
                name = edge["node"]["name"]
                if name in EXCLUDED:
                    continue
                color = edge["node"]["color"] or "#8B949E"
                size, _ = totals.get(name, (0, color))
                totals[name] = (size + edge["size"], color)

        if not repos["pageInfo"]["hasNextPage"]:
            return totals
        cursor = repos["pageInfo"]["endCursor"]


def render(languages: dict[str, tuple[int, str]], theme: dict, top: int = 8) -> str:
    ranked = sorted(languages.items(), key=lambda kv: kv[1][0], reverse=True)[:top]
    total = sum(size for _, (size, _) in ranked) or 1

    rows = (len(ranked) + 1) // 2
    width = 470
    # No heading: the bar sits at the top and the legend labels speak for themselves.
    height = 106 + (rows - 1) * 26

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Code by language">',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{theme["bg"]}" stroke="{theme["border"]}"/>',
    ]

    bar_x, bar_w, bar_y, bar_h = 24, width - 48, 24, 10
    out.append(
        f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5" '
        f'fill="{theme["track"]}"/>'
    )
    out.append(
        f'<clipPath id="bar"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" '
        f'height="{bar_h}" rx="5"/></clipPath>'
    )
    out.append('<g clip-path="url(#bar)">')
    offset = float(bar_x)
    for _, (size, color) in ranked:
        seg = bar_w * size / total
        out.append(
            f'<rect x="{offset:.2f}" y="{bar_y}" width="{seg:.2f}" '
            f'height="{bar_h}" fill="{color}"/>'
        )
        offset += seg
    out.append("</g>")

    for idx, (name, (size, color)) in enumerate(ranked):
        x = 24 + (idx % 2) * 214
        y = 64 + (idx // 2) * 26
        out.append(f'<circle cx="{x + 5}" cy="{y - 4}" r="5" fill="{color}"/>')
        out.append(
            f'<text x="{x + 18}" y="{y}" font-family="{FONT}" font-size="12.5" '
            f'fill="{theme["value"]}">{escape(name)}</text>'
        )
        out.append(
            f'<text x="{x + 192}" y="{y}" font-family="{FONT}" font-size="12" '
            f'text-anchor="end" fill="{theme["label"]}">{100.0 * size / total:.1f}%</text>'
        )

    out.append(
        f'<text x="24" y="{height - 16}" font-family="{FONT}" font-size="10" '
        f'fill="{theme["label"]}">Hand-written code across public and private '
        f'repositories; markup and stylesheets excluded</text>'
    )
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()

    token = os.environ.get("GH_TOKEN")
    login = os.environ.get("GH_LOGIN")
    if not token or not login:
        sys.exit("GH_TOKEN and GH_LOGIN must be set")

    languages = collect_languages(token, login)
    if not languages:
        sys.exit("no language data returned")

    os.makedirs(args.out, exist_ok=True)
    for suffix, theme in THEMES.items():
        path = os.path.join(args.out, f"langs-{suffix}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(languages, theme))
        print(f"wrote {path}")

    total = sum(size for size, _ in languages.values())
    for name, (size, _) in sorted(languages.items(), key=lambda kv: kv[1][0], reverse=True):
        print(f"  {name:<14} {100.0 * size / total:5.1f}%")


if __name__ == "__main__":
    main()
