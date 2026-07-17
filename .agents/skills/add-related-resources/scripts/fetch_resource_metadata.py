#!/usr/bin/env python3
"""Draft ResourceCard metadata from a source URL.

The script returns best-effort JSON. Treat warnings and missing required fields
as prompts for agent/user review before editing docs.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


BLOG_HOSTS = {
    "en": "www.pingcap.com",
    "zh": "pingkai.cn",
    "ja": "pingcap.co.jp",
}

LAB_BASES = {
    "en": "https://labs.tidb.io/labs/",
    "zh": "https://labs.pingcap.com/labs/",
    "ja": "https://labs.tidb.io/ja/labs/",
}

LANG_DURATION_UNIT = {
    "en": "mins",
    "zh": "分钟",
    "ja": "分",
}


def fetch(url: str) -> tuple[str, str, int | None]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
            )
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace"), response.geturl(), response.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return body, exc.geturl(), exc.code
    except urllib.error.URLError as exc:
        return "", url, -1


def clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or None


def strip_tags(value: str | None) -> str | None:
    if value is None:
        return None
    value = re.sub(r"<script\b.*?</script>", "", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", "", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return clean(value)


def unique(values: list[str | None]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = clean(value)
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def meta(html_text: str, key: str) -> str | None:
    patterns = [
        rf'<meta[^>]+property=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']{re.escape(key)}["\']',
        rf'<meta[^>]+name=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']{re.escape(key)}["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, re.I | re.S)
        if match:
            return clean(match.group(1))
    return None


def first_match(html_text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, html_text, re.I | re.S)
        if match:
            return clean(match.group(1))
    return None


def json_ld_author_names(html_text: str) -> list[str]:
    names: list[str] = []
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html_text,
        flags=re.I | re.S,
    )

    def collect_author(value: object) -> None:
        if isinstance(value, str):
            names.append(value)
        elif isinstance(value, dict):
            name = value.get("name")
            if isinstance(name, str):
                names.append(name)
        elif isinstance(value, list):
            for item in value:
                collect_author(item)

    def walk(value: object) -> None:
        if isinstance(value, dict):
            if "author" in value:
                collect_author(value["author"])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for script in scripts:
        try:
            data = json.loads(html.unescape(script))
        except json.JSONDecodeError:
            continue
        walk(data)

    return unique(names)


def blog_author(html_text: str) -> str | None:
    author_links = re.findall(
        r'<a\b[^>]*href=["\'][^"\']*/blog/author/[^"\']*["\'][^>]*>(.*?)</a>',
        html_text,
        flags=re.I | re.S,
    )
    authors = unique([strip_tags(link) for link in author_links])
    if authors:
        return ", ".join(authors)

    authors = json_ld_author_names(html_text)
    if authors:
        return ", ".join(authors)

    return first_match(
        html_text,
        [
            r'"author"\s*:\s*"([^"]+)"',
            r'<meta[^>]+name=["\']author["\'][^>]+content=["\']([^"\']+)["\']',
        ],
    )


def iso_date(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"(\d{4})[-/](\d{2})[-/](\d{2})", value)
    if match:
        return "-".join(match.groups())
    return None


def youtube_id(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("youtu.be"):
        return parsed.path.strip("/").split("/")[0] or None
    if "youtube.com" in parsed.netloc:
        query = urllib.parse.parse_qs(parsed.query)
        if query.get("v"):
            return query["v"][0]
    return None


def detect_type(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if "youtube.com" in host or host.endswith("youtu.be"):
        return "video"
    if host in {"www.pingcap.com", "pingkai.cn", "pingcap.co.jp"} and "/blog/" in path:
        return "blog"
    if host in {"labs.tidb.io", "labs.pingcap.com"} and "/labs/" in path:
        return "lab"
    return None


def normalize_blog_url(url: str, lang: str) -> str:
    parsed = urllib.parse.urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if "blog" in parts:
        slug = parts[parts.index("blog") + 1] if parts.index("blog") + 1 < len(parts) else ""
    else:
        slug = parts[-1] if parts else ""
    if lang == "zh":
        return f"https://{BLOG_HOSTS[lang]}/tidbcommunity/blog/{slug}/"
    return f"https://{BLOG_HOSTS[lang]}/blog/{slug}/"


def normalize_lab_url(url: str, lang: str) -> str:
    parsed = urllib.parse.urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    slug = parts[-1] if parts else ""
    return LAB_BASES[lang] + slug


def format_minutes(minutes: int, lang: str) -> str:
    if lang == "en":
        return f"{minutes} {LANG_DURATION_UNIT[lang]}"
    return f"{minutes} {LANG_DURATION_UNIT[lang]}"


def parse_iso8601_duration(value: str | None) -> int | None:
    if not value:
        return None
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value)
    if not match:
        return None
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    total = hours * 60 + minutes + (1 if seconds >= 30 else 0)
    return max(total, 1)


def draft_blog(url: str, lang: str) -> dict:
    warnings: list[str] = []
    normalized = normalize_blog_url(url, lang)
    html_text, final_url, status = fetch(normalized)
    if status == -1:
        warnings.append("Fetch failed. Inspect the source manually or retry with network access.")
    elif status == 404 and lang == "ja":
        warnings.append("Japanese blog URL returned 404. Ask before falling back or substituting.")
    elif status and status >= 400:
        warnings.append(f"Fetch returned HTTP {status}.")

    title = first_match(
        html_text,
        [
            r'<h1[^>]*class=["\'][^"\']*banner-resource__title[^"\']*["\'][^>]*>(.*?)</h1>',
            r"<h1[^>]*>(.*?)</h1>",
        ],
    ) or meta(html_text, "og:title")
    image = meta(html_text, "og:image")
    author = blog_author(html_text)
    date = iso_date(first_match(html_text, [r'"datePublished"\s*:\s*"([^"]+)"']) or meta(html_text, "article:published_time"))

    return card("blog", title, final_url, image, author=author, date=date, warnings=warnings)


def draft_video(url: str, lang: str) -> dict:
    warnings: list[str] = []
    video_id = youtube_id(url)
    if not video_id:
        return card("video", None, url, None, warnings=["Could not extract YouTube video ID."])

    html_text, final_url, status = fetch(url)
    if status == -1:
        warnings.append("Fetch failed; title/channel/duration might be missing.")
    elif status and status >= 400:
        warnings.append(f"Fetch returned HTTP {status}; title/channel/duration might be missing.")

    title = meta(html_text, "og:title") or first_match(
        html_text,
        [
            r'"playerOverlayVideoDetailsRenderer"\s*:\s*{\s*"title"\s*:\s*{\s*"simpleText"\s*:\s*"([^"]+)"',
            r'"title"\s*:\s*{\s*"runs"\s*:\s*\[\s*{\s*"text"\s*:\s*"([^"]+)"',
        ],
    )
    author = meta(html_text, "og:video:tag") or first_match(
        html_text,
        [
            r'"shortBylineText"\s*:\s*{\s*"runs"\s*:\s*\[\s*{\s*"text"\s*:\s*"([^"]+)"',
            r'"ownerChannelName"\s*:\s*"([^"]+)"',
        ],
    )
    duration_iso = meta(html_text, "duration") or first_match(html_text, [r'"lengthSeconds"\s*:\s*"(\d+)"'])
    minutes = None
    if duration_iso and duration_iso.isdigit():
        seconds = int(duration_iso)
        minutes = max(seconds // 60 + (1 if seconds % 60 >= 30 else 0), 1)
    else:
        minutes = parse_iso8601_duration(duration_iso)
    duration = format_minutes(minutes, lang) if minutes else None
    image = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

    return card("video", title, final_url or url, image, author=author, duration=duration, warnings=warnings)


def draft_lab(url: str, lang: str) -> dict:
    warnings: list[str] = []
    normalized = normalize_lab_url(url, lang)
    html_text, final_url, status = fetch(normalized)
    if status == -1:
        warnings.append("Fetch failed. Inspect the source manually or retry with network access.")
    elif status and status >= 400:
        warnings.append(f"Fetch returned HTTP {status}.")

    title = meta(html_text, "og:title") or first_match(
        html_text,
        [
            r"<h1[^>]*>(.*?)</h1>",
            r'"title"\s*:\s*"([^"]+)"',
        ],
    )
    image = meta(html_text, "og:image") or first_match(
        html_text,
        [r'(https://lab-static\.pingcap\.com/[^"\\<>\s]+?\.(?:png|jpg|jpeg|webp))'],
    )
    minutes_text = first_match(
        html_text,
        [
            r'(\d+)\s*(?:mins|minutes|分钟|分)',
            r'"duration"\s*:\s*"?(\d+)"?',
        ],
    )
    duration = format_minutes(int(minutes_text), lang) if minutes_text and minutes_text.isdigit() else None

    return card("lab", title, final_url, image, duration=duration, warnings=warnings)


def card(
    type_: str,
    title: str | None,
    link: str | None,
    image: str | None,
    *,
    author: str | None = None,
    date: str | None = None,
    duration: str | None = None,
    warnings: list[str] | None = None,
) -> dict:
    result = {
        "type": type_,
        "title": clean(title),
        "link": link,
        "imgSrc": clean(image),
        "author": clean(author),
        "date": date,
        "duration": clean(duration),
        "warnings": warnings or [],
    }
    missing = [key for key in ("title", "link", "imgSrc") if not result.get(key)]
    if missing:
        result["warnings"].append("Missing required field(s): " + ", ".join(missing))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--lang", choices=["en", "zh", "ja"], required=True)
    args = parser.parse_args()

    type_ = detect_type(args.url)
    if type_ == "blog":
        result = draft_blog(args.url, args.lang)
    elif type_ == "video":
        result = draft_video(args.url, args.lang)
    elif type_ == "lab":
        result = draft_lab(args.url, args.lang)
    else:
        result = card("unknown", None, args.url, None, warnings=["Unsupported or ambiguous resource URL."])

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
