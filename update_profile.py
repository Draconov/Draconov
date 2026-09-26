import base64
import calendar
import html
import json
import os
import urllib.request
import zlib
from datetime import date, datetime, timezone

USER = "Draconov"
BIRTHDAY = date(2002, 6, 1)
JOINED_YEAR = 2017
W = 56
CARD_WIDTH = 840
CARD_HEIGHT = 590
INFO_X = 200
INFO_Y = 150
INFO_LINE_HEIGHT = 21
ANSI_Y = 20
ANSI_PIXEL_WIDTH = 720
ANSI_PIXEL_HEIGHT = 90

# Exact ANSI banner palette chosen for the profile wordmark.
ANSI_MAIN = "#39FF14"
ANSI_HIGHLIGHT = "#F4FF63"
ANSI_SHADOW = "#0E7A0D"

# Matrix rain around the info block. The center is deliberately left clear.
MATRIX_MAIN = "#39FF14"
MATRIX_HEAD = "#F4FF63"
MATRIX_DIM = "#0E7A0D"
MATRIX_FONT_SIZE = 11
MATRIX_LINE_HEIGHT = 13
MATRIX_TOP = 122
MATRIX_BOTTOM = 578
MATRIX_HEAD_GLOW = "#cfff7a"
MATRIX_CHAR_POOL = r"01<>[]{}()/\|+-=*#;:.ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MATRIX_LEFT_COLUMNS = (
    {"x": 17,  "trail": 20, "step": 10, "dur": 5.3, "delay": -0.2, "phase": 4,  "density": 1.00, "opacity": 1.00, "size": 11.5, "jitter": 1.2},
    {"x": 31,  "trail": 13, "step": 12, "dur": 7.9, "delay": -1.7, "phase": 17, "density": 0.82, "opacity": 0.90, "size": 10.7, "jitter": 0.8},
    {"x": 47,  "trail": 17, "step": 11, "dur": 6.2, "delay": -0.8, "phase": 10, "density": 0.96, "opacity": 0.96, "size": 11.1, "jitter": 1.0},
    {"x": 64,  "trail": 10, "step": 13, "dur": 9.0, "delay": -2.6, "phase": 24, "density": 0.72, "opacity": 0.84, "size": 10.4, "jitter": 0.9},
    {"x": 84,  "trail": 15, "step": 10, "dur": 6.9, "delay": -1.0, "phase": 8,  "density": 0.93, "opacity": 0.91, "size": 11.0, "jitter": 1.1},
    {"x": 103, "trail": 9,  "step": 12, "dur": 9.8, "delay": -3.9, "phase": 29, "density": 0.68, "opacity": 0.77, "size": 10.2, "jitter": 0.8},
    {"x": 124, "trail": 13, "step": 11, "dur": 8.1, "delay": -2.0, "phase": 19, "density": 0.86, "opacity": 0.79, "size": 10.6, "jitter": 0.7},
    {"x": 145, "trail": 8,  "step": 13, "dur": 10.9,"delay": -4.8, "phase": 35, "density": 0.60, "opacity": 0.64, "size": 9.9,  "jitter": 0.6},
    {"x": 160, "trail": 6,  "step": 14, "dur": 12.0,"delay": -5.8, "phase": 39, "density": 0.52, "opacity": 0.48, "size": 9.6,  "jitter": 0.5},
)
MATRIX_RIGHT_COLUMNS = (
    {"x": 666, "trail": 6,  "step": 14, "dur": 11.8,"delay": -5.7, "phase": 38, "density": 0.52, "opacity": 0.48, "size": 9.6,  "jitter": 0.5},
    {"x": 684, "trail": 8,  "step": 13, "dur": 10.7,"delay": -4.7, "phase": 34, "density": 0.61, "opacity": 0.64, "size": 9.9,  "jitter": 0.6},
    {"x": 716, "trail": 13, "step": 11, "dur": 8.0, "delay": -2.2, "phase": 18, "density": 0.87, "opacity": 0.79, "size": 10.6, "jitter": 0.7},
    {"x": 737, "trail": 9,  "step": 12, "dur": 9.6, "delay": -4.1, "phase": 28, "density": 0.69, "opacity": 0.77, "size": 10.2, "jitter": 0.8},
    {"x": 756, "trail": 15, "step": 10, "dur": 6.8, "delay": -1.2, "phase": 7,  "density": 0.93, "opacity": 0.91, "size": 11.0, "jitter": 1.1},
    {"x": 776, "trail": 10, "step": 13, "dur": 8.9, "delay": -2.8, "phase": 23, "density": 0.72, "opacity": 0.84, "size": 10.4, "jitter": 0.9},
    {"x": 793, "trail": 17, "step": 11, "dur": 6.1, "delay": -0.9, "phase": 9,  "density": 0.96, "opacity": 0.96, "size": 11.1, "jitter": 1.0},
    {"x": 809, "trail": 13, "step": 12, "dur": 7.7, "delay": -1.8, "phase": 16, "density": 0.83, "opacity": 0.90, "size": 10.7, "jitter": 0.8},
    {"x": 823, "trail": 20, "step": 10, "dur": 5.1, "delay": -0.3, "phase": 3,  "density": 1.00, "opacity": 1.00, "size": 11.5, "jitter": 1.2},
)

# Pixel mask traced from the supplied DRACONOV ANSI reference. 0 = transparent,
# 1 = dark-green depth, 2 = neon-green body, 3 = yellow highlight/scanline.
# It is compressed only to keep this generator readable and the repository small.
# render() expands it into ordinary SVG paths, so the final SVG has no font
# dependency, kerning, fallback glyphs, or inter-character spacing at all.
ANSI_PIXEL_DATA_B64 = (
    "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"
)



TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("ACCESS_TOKEN") or ""
PRIV_TOKEN = os.environ.get("ACCESS_TOKEN") or TOKEN


def gh(url, payload=None, token=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {token or TOKEN}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.loads(r.read() or "{}")


def graphql(query, variables=None, token=None):
    _, resp = gh("https://api.github.com/graphql", {"query": query, "variables": variables or {}}, token)
    if resp.get("errors"):
        raise RuntimeError(resp["errors"])
    return resp["data"]


def age(b, t):
    years = t.year - b.year - ((t.month, t.day) < (b.month, b.day))
    months = (t.month - b.month - (t.day < b.day)) % 12
    if t.day >= b.day:
        days = t.day - b.day
    else:
        pm_year, pm = (t.year, t.month - 1) if t.month > 1 else (t.year - 1, 12)
        days = calendar.monthrange(pm_year, pm)[1] - b.day + t.day
    return years, months, days


def fetch_stats():
    yr_aliases = "\n".join(
        f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y + 1}-01-01T00:00:00Z")'
        " { totalCommitContributions restrictedContributionsCount }"
        for y in range(JOINED_YEAR, datetime.now(timezone.utc).year + 1)
    )
    contrib = graphql(f'query {{ user(login: "{USER}") {{ {yr_aliases} }} }}')["user"]
    commits = sum(
        v["totalCommitContributions"] + v["restrictedContributionsCount"]
        for v in contrib.values()
    )

    u = graphql(f"""
    query {{
      user(login: "{USER}") {{
        id
        followers {{ totalCount }}
        repositories(first: 100, ownerAffiliations: OWNER) {{
          totalCount
          nodes {{ name stargazerCount isFork }}
        }}
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) {{
          totalCount
        }}
      }}
    }}""", token=PRIV_TOKEN)["user"]

    stats = {
        "followers": u["followers"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "contributed": u["repositoriesContributedTo"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "commits": commits,
    }
    stats.update(loc([n["name"] for n in u["repositories"]["nodes"] if not n["isFork"]], u["id"]))
    return stats


LOC_QUERY = """
query($owner: String!, $name: String!, $id: ID!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef { target { ... on Commit {
      history(first: 100, author: {id: $id}, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { additions deletions }
      }
    } } }
  }
}"""


def loc(repo_names, user_id):
    add = rem = 0
    for name in repo_names:
        cursor = None
        try:
            while True:
                ref = graphql(LOC_QUERY, {"owner": USER, "name": name, "id": user_id, "cursor": cursor}, token=PRIV_TOKEN)["repository"]["defaultBranchRef"]
                if ref is None:
                    break  # empty repo
                h = ref["target"]["history"]
                add += sum(n["additions"] for n in h["nodes"])
                rem += sum(n["deletions"] for n in h["nodes"])
                if not h["pageInfo"]["hasNextPage"]:
                    break
                cursor = h["pageInfo"]["endCursor"]
        except Exception as e:
            print(f"loc {name}: {e}")
    return {"loc_add": add, "loc_del": rem, "loc": add - rem}


PALETTES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "h": "#58a6ff",
              "k": "#ffa657", "v": "#c9d1d9", "d": "#484f58", "g": "#3fb950", "r": "#f85149"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "h": "#0969da",
               "k": "#953800", "v": "#24292f", "d": "#afb8c1", "g": "#1a7f37", "r": "#cf222e"},
}


def kv(key, val, width=W):
    dots = "." * max(width - len(key) - len(str(val)) - 3, 1)
    return [(f"{key}: ", "k"), (dots + " ", "d"), (str(val), "v")]


def kv2(k1, v1, k2, v2):
    left = kv(k1, v1, 30)
    return left + [(" | ", "d")] + kv(k2, v2, 23)


def rule(title=""):
    label = f"─ {title} " if title else ""
    return [(label, "h"), ("─" * (W - len(label)), "d")]


def info_lines(s):
    y, m, d = age(BIRTHDAY, date.today())
    n = lambda x: f"{x:,}"
    return [
        [(f"{USER.lower()}@github ", "h"), ("─" * (W - len(USER) - 8), "d")],
        [],
        kv("Android", "Windows"),
        kv("Uptime", f"{y} years, {m} months, {d} days"),
        kv("Vacant", "Working on my CV bucket list"),
        kv("Kernel", "Software Engineer"),
        kv("IDE", "VS Code"),
        [],
        kv("Languages.Programming", "Python, JavaScript"),
        kv("Languages.Real", "English, Ukrainian"),
        kv("Hobbies", "Gaming, Drawing and Coding"),
        [],
        rule("Contact"),
        kv("Email", "draconov666@gmail.com"),
        kv("GitHub", f"github.com/{USER}"),
        [],
        rule("GitHub Stats"),
        kv2("Repos", f"{s['repos']} {{Contributed: {s['contributed']}}}", "Stars", n(s["stars"])),
        kv2("Commits", n(s["commits"]), "Followers", n(s["followers"])),
        [("Lines of Code: ", "k"), (n(s["loc"]), "v"), (" ( ", "d"),
         (n(s["loc_add"]) + "++", "g"), (", ", "d"), (n(s["loc_del"]) + "--", "r"), (" )", "d")],
    ]


def _ansi_pixels():
    raw = zlib.decompress(base64.b64decode(ANSI_PIXEL_DATA_B64))
    expected = ANSI_PIXEL_WIDTH * ANSI_PIXEL_HEIGHT
    if len(raw) != expected:
        raise ValueError(f"ANSI pixel mask has {len(raw)} bytes, expected {expected}")
    return raw


def ansi_paths():
    # Merge adjacent same-colour pixels into horizontal SVG path runs. This keeps
    # the generated SVG compact while preserving the reference pixel-for-pixel.
    pixels = _ansi_pixels()
    paths = {1: [], 2: [], 3: []}
    w = ANSI_PIXEL_WIDTH
    for y in range(ANSI_PIXEL_HEIGHT):
        row = y * w
        x = 0
        while x < w:
            role = pixels[row + x]
            if role == 0:
                x += 1
                continue
            x2 = x + 1
            while x2 < w and pixels[row + x2] == role:
                x2 += 1
            run = x2 - x
            paths[role].append(f"M{x} {y}h{run}v1h-{run}z")
            x = x2
    return {role: "".join(parts) for role, parts in paths.items()}


def _matrix_stream(seed, count):
    alphabet = MATRIX_CHAR_POOL
    out = []
    pos = (seed * 13 + 5) % len(alphabet)
    # A few deterministic hidden name fragments. They are intentionally sparse.
    name_slots = {5, 24} if seed % 3 == 0 else ({12} if seed % 4 == 0 else set())
    i = 0
    while len(out) < count:
        if i in name_slots and len(out) + 8 <= count:
            out.extend("DRACONOV")
            i += 8
            continue
        pos = (pos + 3 + (seed % 9) + (i % 5)) % len(alphabet)
        out.append(alphabet[pos])
        i += 1
    return out[:count]


def _matrix_text(x, y, ch, fill, opacity, size=None, extra=''):
    return (
        f'<text x="{x:.2f}" y="{y}" fill="{fill}" opacity="{opacity:.2f}" '
        f'font-size="{(size or MATRIX_FONT_SIZE):.1f}px" text-anchor="middle"{extra}>'
        f'{html.escape(ch)}</text>'
    )


def _jitter(seed, row, amount):
    # Small deterministic lateral movement makes streams feel less like a rigid grid.
    if not amount:
        return 0.0
    n = ((seed * 37 + row * 17) % 11) - 5
    return (n / 5.0) * amount


def _matrix_column(spec, seed, glow_filter, mode):
    rows = int((MATRIX_BOTTOM - MATRIX_TOP) / spec["step"]) + spec["trail"] + 10
    chars = _matrix_stream(seed, rows + 16)
    period = rows * spec["step"]
    visible_rows = []
    for idx in range(spec["trail"]):
        row = spec["phase"] - idx
        while row < 0:
            row += rows
        visible_rows.append(row)
    visible_set = set(visible_rows)

    def copy(base_y, anim_delay):
        glow_parts = []
        crisp_parts = []
        for row in range(rows):
            if row not in visible_set:
                continue
            dist = (spec["phase"] - row) % rows
            if dist >= spec["trail"]:
                continue
            # Sparse streams intentionally skip some cells.
            gate = ((row * 7 + seed * 3) % 100) / 100.0
            if gate > spec["density"] and dist > 1:
                continue
            y = base_y + row * spec["step"]
            x = spec["x"] + _jitter(seed, row, spec.get("jitter", 0.0))
            ch = chars[row % len(chars)]
            base_size = spec.get("size", MATRIX_FONT_SIZE)

            if dist == 0:
                fill = MATRIX_HEAD
                glow_fill = MATRIX_HEAD_GLOW
                op = 1.0 * spec["opacity"]
                gop = 0.58 if mode == "dark" else 0.23
                size = base_size + 0.9
            elif dist == 1:
                fill = MATRIX_MAIN
                glow_fill = MATRIX_MAIN
                op = 0.97 * spec["opacity"]
                gop = 0.34 if mode == "dark" else 0.13
                size = base_size + 0.4
            elif dist <= 3:
                fill = MATRIX_MAIN
                glow_fill = MATRIX_MAIN
                op = (0.86 - 0.12 * (dist - 2)) * spec["opacity"]
                gop = 0.20 if mode == "dark" else 0.07
                size = base_size
            elif dist <= 6:
                fill = MATRIX_MAIN if dist % 3 == 0 else MATRIX_DIM
                glow_fill = MATRIX_MAIN
                op = (0.49 - 0.055 * (dist - 4)) * spec["opacity"]
                gop = 0.09 if mode == "dark" else 0.03
                size = base_size - 0.2
            else:
                fill = MATRIX_DIM
                glow_fill = MATRIX_DIM
                op = max(0.08, 0.28 - 0.020 * (dist - 7)) * spec["opacity"]
                gop = 0.0
                size = base_size - 0.45

            if gop > 0:
                glow_parts.append(_matrix_text(x, y, ch, glow_fill, gop, size, f' filter="url(#{glow_filter})"'))
            crisp_parts.append(_matrix_text(x, y, ch, fill, op, size))

        return (
            '<g>' + ''.join(glow_parts) + ''.join(crisp_parts)
            + f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {period}" '
            + f'dur="{spec["dur"]:.1f}s" begin="{anim_delay:.1f}s" repeatCount="indefinite"/></g>'
        )

    # Deliberately place every stream head somewhere inside the card for the
    # static fallback. Animation starts from that staggered snapshot.
    span = MATRIX_BOTTOM - MATRIX_TOP - 86
    target_head_y = MATRIX_TOP + 48 + ((seed * 83 + int(abs(spec["delay"]) * 29)) % max(span, 1))
    base = target_head_y - spec["phase"] * spec["step"]
    return copy(base, spec["delay"]) + copy(base - period, spec["delay"])


def matrix_rain(mode):
    glow_std = 1.15 if mode == "dark" else 0.65
    fog_opacity = 0.082 if mode == "dark" else 0.028
    out = [
        '<defs>',
        f'<clipPath id="matrix-left"><rect x="1" y="{MATRIX_TOP}" width="189" height="{MATRIX_BOTTOM - MATRIX_TOP}"/></clipPath>',
        f'<clipPath id="matrix-right"><rect x="650" y="{MATRIX_TOP}" width="189" height="{MATRIX_BOTTOM - MATRIX_TOP}"/></clipPath>',
        '<linearGradient id="matrix-edge-left" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="#39FF14" stop-opacity="1"/>'
        '<stop offset="42%" stop-color="#39FF14" stop-opacity="0.42"/>'
        '<stop offset="100%" stop-color="#39FF14" stop-opacity="0"/></linearGradient>',
        '<linearGradient id="matrix-edge-right" x1="1" y1="0" x2="0" y2="0">'
        '<stop offset="0%" stop-color="#39FF14" stop-opacity="1"/>'
        '<stop offset="42%" stop-color="#39FF14" stop-opacity="0.42"/>'
        '<stop offset="100%" stop-color="#39FF14" stop-opacity="0"/></linearGradient>',
        '<linearGradient id="matrix-vertical-fade" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="white" stop-opacity="0.20"/>'
        '<stop offset="10%" stop-color="white" stop-opacity="1"/>'
        '<stop offset="90%" stop-color="white" stop-opacity="1"/>'
        '<stop offset="100%" stop-color="white" stop-opacity="0.22"/></linearGradient>',
        '<mask id="matrix-left-mask"><rect x="1" y="0" width="189" height="590" fill="url(#matrix-vertical-fade)"/></mask>',
        '<mask id="matrix-right-mask"><rect x="615" y="0" width="224" height="590" fill="url(#matrix-vertical-fade)"/></mask>',
        f'<filter id="matrix-glow" x="-70%" y="-25%" width="240%" height="150%">'
        f'<feGaussianBlur stdDeviation="{glow_std}"/></filter>',
        '</defs>',
        f'<rect x="1" y="0" width="189" height="{CARD_HEIGHT}" fill="url(#matrix-edge-left)" opacity="{fog_opacity}" mask="url(#matrix-left-mask)"/>',
        f'<rect x="615" y="0" width="224" height="{CARD_HEIGHT}" fill="url(#matrix-edge-right)" opacity="{fog_opacity}" mask="url(#matrix-right-mask)"/>',
        '<g font-family="Consolas, Menlo, monospace" font-weight="700" letter-spacing="0.2px">',
        '<g clip-path="url(#matrix-left)" mask="url(#matrix-left-mask)">',
    ]
    for i, spec in enumerate(MATRIX_LEFT_COLUMNS):
        out.append(_matrix_column(spec, i + 1, 'matrix-glow', mode))
    out.append('</g><g clip-path="url(#matrix-right)" mask="url(#matrix-right-mask)">')
    for i, spec in enumerate(MATRIX_RIGHT_COLUMNS):
        out.append(_matrix_column(spec, i + 31, 'matrix-glow', mode))
    out.append('</g></g>')
    return ''.join(out)

def render(mode, stats):
    p = PALETTES[mode]
    x0 = (CARD_WIDTH - ANSI_PIXEL_WIDTH) // 2
    paths = ansi_paths()
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_WIDTH}" height="{CARD_HEIGHT}" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" '
        f'font-family="Consolas, Menlo, monospace" font-size="13px">',
        f'<rect x="0.5" y="0.5" width="{CARD_WIDTH - 1}" height="{CARD_HEIGHT - 1}" rx="10" fill="{p["bg"]}" stroke="{p["border"]}"/>',
        matrix_rain(mode),
        f'<g transform="translate({x0} {ANSI_Y})" shape-rendering="crispEdges">',
        f'<path d="{paths[1]}" fill="{ANSI_SHADOW}"/>',
        f'<path d="{paths[2]}" fill="{ANSI_MAIN}"/>',
        f'<path d="{paths[3]}" fill="{ANSI_HIGHLIGHT}"/>',
        '</g>',
    ]

    for i, segs in enumerate(info_lines(stats)):
        if not segs:
            continue
        spans = "".join(f'<tspan fill="{p[c]}">{html.escape(t)}</tspan>' for t, c in segs)
        out.append(f'<text x="{INFO_X}" y="{INFO_Y + i * INFO_LINE_HEIGHT}" xml:space="preserve">{spans}</text>')
    out.append("</svg>")
    return "\n".join(out)


def selfcheck():
    assert age(date(2000, 3, 31), date(2026, 4, 1)) == (26, 0, 1)
    assert age(date(2000, 1, 1), date(2026, 1, 1)) == (26, 0, 0)
    assert len("".join(t for t, _ in kv("OS", "Windows, macOS"))) == W
    raw = _ansi_pixels()
    assert len(raw) == ANSI_PIXEL_WIDTH * ANSI_PIXEL_HEIGHT
    assert set(raw) <= {0, 1, 2, 3}
    assert ANSI_PIXEL_WIDTH < CARD_WIDTH
    assert ANSI_Y + ANSI_PIXEL_HEIGHT < INFO_Y
    assert (ANSI_MAIN, ANSI_HIGHLIGHT, ANSI_SHADOW) == ("#39FF14", "#F4FF63", "#0E7A0D")
    assert len(MATRIX_LEFT_COLUMNS) >= 9
    assert len(MATRIX_RIGHT_COLUMNS) >= 9
    assert max(c["x"] for c in MATRIX_LEFT_COLUMNS) < INFO_X
    assert min(c["x"] for c in MATRIX_RIGHT_COLUMNS) > INFO_X + 400


if __name__ == "__main__":
    selfcheck()
    stats = fetch_stats()
    print("stats:", stats)
    for mode in PALETTES:
        with open(f"{mode}_mode.svg", "w", encoding="utf-8") as f:
            f.write(render(mode, stats))
    print("wrote dark_mode.svg, light_mode.svg")
