#!/usr/bin/env python3
"""Render the profile's commit-activity chart as a self-hosted SVG.

Nothing here depends on a third-party rendering service: the data comes from
GitHub's search API and the SVG is emitted locally, so the chart cannot break
because someone else's shared instance is rate limited.

Data source note: GitHub's own contribution calendar honours the "include
private contributions" profile setting, so it reports zero for days spent in
private repositories. The commit search API respects token scope instead, so
with a token that can read private repositories this chart shows the work that
actually happened.

Usage:
    GH_TOKEN=... GH_LOGIN=octocat python generate_cards.py --out dist
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone

SEARCH = "https://api.github.com/search/commits"

THEMES = {
    "dark": {
        "bg": "#0D1117",
        "border": "#30363D",
        "title": "#8B949E",
        "axis": "#8B949E",
        "grid": "#21262D",
        "line": "#E3B341",
        "dot": "#F2CC60",
    },
    "light": {
        "bg": "#FFFFFF",
        "border": "#D0D7DE",
        "title": "#57606A",
        "axis": "#57606A",
        "grid": "#EAEEF2",
        "line": "#BF8700",
        "dot": "#9A6700",
    },
}

FONT = "'Segoe UI',Ubuntu,'Helvetica Neue',Helvetica,sans-serif"
WINDOW_DAYS = 31


def request_json(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-activity-generator",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        sys.exit(f"HTTP {exc.code} on {url}: {exc.read().decode('utf-8', 'replace')[:300]}")


def collect_commits(token: str, login: str, start: date, end: date) -> dict[date, int]:
    counts = {start + timedelta(days=i): 0 for i in range((end - start).days + 1)}
    page = 1

    while True:
        query = f"author:{login} author-date:{start.isoformat()}..{end.isoformat()}"
        url = f"{SEARCH}?q={urllib.parse.quote(query)}&per_page=100&page={page}"
        payload = request_json(url, token)

        items = payload.get("items", [])
        for item in items:
            stamp = item["commit"]["author"]["date"]
            day = datetime.fromisoformat(stamp.replace("Z", "+00:00")).date()
            if day in counts:
                counts[day] += 1

        # The search API caps out at 1000 results; stop when a page comes back short.
        if len(items) < 100 or page >= 10:
            return counts
        page += 1


def nice_top(value: int) -> tuple[int, int]:
    """Return (axis_top, step) giving at most four gridline steps."""
    if value <= 4:
        return 4, 1
    magnitude = 10 ** int(math.floor(math.log10(value)))
    step = magnitude
    for multiplier in (1, 2, 2.5, 5, 10):
        step = multiplier * magnitude
        if value / step <= 4:
            break
    step = int(math.ceil(step))
    return step * int(math.ceil(value / step)), step


def render(counts: dict[date, int], theme: dict) -> str:
    days = sorted(counts)
    values = [counts[d] for d in days]
    total = sum(values)

    width, height = 860, 250
    left, right, top, bottom = 58, 22, 52, 46
    plot_w = width - left - right
    plot_h = height - top - bottom

    axis_top, step = nice_top(max(values))

    def px(idx: int) -> float:
        return left + plot_w * idx / (len(days) - 1)

    def py(value: float) -> float:
        return top + plot_h * (1 - value / axis_top)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Commit activity, last {len(days)} days, {total} commits">',
        '<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{theme["line"]}" stop-opacity="0.38"/>'
        f'<stop offset="1" stop-color="{theme["line"]}" stop-opacity="0.02"/>'
        "</linearGradient></defs>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{theme["bg"]}" stroke="{theme["border"]}"/>',
        f'<text x="{width / 2:.0f}" y="30" font-family="{FONT}" font-size="14" '
        f'font-weight="600" text-anchor="middle" fill="{theme["title"]}">'
        f"Commit activity · last {len(days)} days · {total} commits</text>",
    ]

    tick = 0
    while tick <= axis_top:
        y = py(tick)
        out.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" '
            f'stroke="{theme["grid"]}"/>'
        )
        out.append(
            f'<text x="{left - 9}" y="{y + 3.5:.1f}" font-family="{FONT}" font-size="10" '
            f'text-anchor="end" fill="{theme["axis"]}">{tick}</text>'
        )
        tick += step

    area = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(values))
    out.append(
        f'<polygon points="{left},{py(0):.1f} {area} {left + plot_w},{py(0):.1f}" '
        'fill="url(#fade)"/>'
    )
    out.append(
        f'<polyline points="{area}" fill="none" stroke="{theme["line"]}" '
        'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
    )

    for i, v in enumerate(values):
        out.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="2.6" fill="{theme["dot"]}"/>')

    for i, day in enumerate(days):
        out.append(
            f'<text x="{px(i):.1f}" y="{top + plot_h + 16}" font-family="{FONT}" '
            f'font-size="9.5" text-anchor="middle" fill="{theme["axis"]}">{day.day}</text>'
        )

    mid_y = int(top + plot_h / 2)
    out.append(
        f'<text x="14" y="{mid_y}" font-family="{FONT}" font-size="10" '
        f'text-anchor="middle" fill="{theme["axis"]}" '
        f'transform="rotate(-90 14 {mid_y})">Commits</text>'
    )
    out.append(
        f'<text x="{left + plot_w / 2:.0f}" y="{height - 12}" font-family="{FONT}" '
        f'font-size="10" text-anchor="middle" fill="{theme["axis"]}">'
        f"{days[0].isoformat()} → {days[-1].isoformat()}</text>"
    )
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dist")
    # A token that cannot read private repositories reports a handful of days with
    # everything else at zero, which reads as "did nothing for a month". Guard on the
    # spread rather than the total, since one busy public day can clear a total check.
    ap.add_argument("--min-active-days", type=int, default=5)
    args = ap.parse_args()

    token = os.environ.get("GH_TOKEN")
    login = os.environ.get("GH_LOGIN")
    if not token or not login:
        sys.exit("GH_TOKEN and GH_LOGIN must be set")

    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=WINDOW_DAYS - 1)
    counts = collect_commits(token, login, start, end)
    total = sum(counts.values())
    active_days = sum(1 for value in counts.values() if value)

    if active_days < args.min_active_days:
        sys.exit(
            f"only {active_days} active day(s) and {total} commits in {start}..{end}. "
            "That is the signature of a token that cannot see private repositories, and "
            "the resulting chart would misrepresent the work. Refusing to publish. In CI, "
            "set the PROFILE_TOKEN secret to a PAT with read access to private repos."
        )

    os.makedirs(args.out, exist_ok=True)
    for suffix, theme in THEMES.items():
        path = os.path.join(args.out, f"activity-{suffix}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(counts, theme))
        print(f"wrote {path}")

    busiest = max(counts, key=lambda d: counts[d])
    print(
        f"{total} commits across {start} .. {end}; {active_days} active days; "
        f"busiest {busiest} = {counts[busiest]}"
    )


if __name__ == "__main__":
    main()
