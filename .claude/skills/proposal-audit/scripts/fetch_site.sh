#!/usr/bin/env bash
# Download a prospect's WordPress sitemap URLs and every article/service page, slowly.
# Usage: fetch_site.sh <domain> <out_dir>      e.g. fetch_site.sh sambilegal.com.au ./work
# Writes: <out>/list.txt ("A|S|O url" per line), <out>/pages/*.html, <out>/home.html,
#         <out>/robots.txt, <out>/sitemaps/*.xml
set -euo pipefail
DOMAIN="$1"; OUT="$2"; BASE="https://$DOMAIN"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
PACE="${PACE:-1.5}"   # seconds between requests: many law-firm hosts sit behind bot protection
mkdir -p "$OUT/pages" "$OUT/sitemaps"
get(){ curl -sS -L -A "$UA" "$@"; sleep "$PACE"; }

get -o "$OUT/home.html" "$BASE/"
get -o "$OUT/robots.txt" "$BASE/robots.txt" || true
INDEX=""
for cand in sitemap_index.xml wp-sitemap.xml sitemap.xml; do
  get -o "$OUT/sitemaps/index.xml" "$BASE/$cand" || continue
  grep -q '<loc>' "$OUT/sitemaps/index.xml" && { INDEX="$cand"; break; }
done
[ -n "$INDEX" ] || { echo "no sitemap found" >&2; exit 1; }
echo "sitemap index: $INDEX"

: > "$OUT/list.txt"
for sm in $(grep -o '<loc>[^<]*\.xml' "$OUT/sitemaps/index.xml" | sed 's/<loc>//'); do
  name=$(basename "$sm" .xml); get -o "$OUT/sitemaps/$name.xml" "$sm"
  # Classify by sitemap name: posts = articles (A); pages, locations, team, taxonomies,
  # authors = other (O); every other custom post type = service page (S).
  case "$name" in
    post-sitemap*|wp-sitemap-posts-post*) k=A ;;
    page-sitemap*|*location*|*team*|*categor*|*author*|*tag*|*taxonom*|wp-sitemap-users*|wp-sitemap-posts-page*) k=O ;;
    *) k=S ;;
  esac
  python3 -c "
import re,sys
x=open(sys.argv[1]).read()
for u in re.findall(r'<url>\s*<loc>([^<]+)</loc>',x): print(sys.argv[2],u)
" "$OUT/sitemaps/$name.xml" "$k" >> "$OUT/list.txt"
  echo "$name: $(grep -c '<loc>' "$OUT/sitemaps/$name.xml") urls -> $k"
done
echo "Review list.txt: hub/service pages that live in page-sitemap are tagged O; change them to S by hand."

while read -r k u; do
  [ "$k" = O ] && case "$u" in */contact/|*/news/|*/about-us/|*/blog/|*/insights/) ;; *) continue;; esac
  f="$OUT/pages/$(echo "$u" | sed "s#https\?://[^/]*/##; s#/\$##; s#/#__#g").html"
  [ "$f" = "$OUT/pages/.html" ] && continue
  [ -s "$f" ] || { code=$(curl -sS -L -A "$UA" -o "$f" -w '%{http_code}' "$u"); sleep "$PACE"; [ "$code" = 200 ] || echo "$code $u"; }
done < "$OUT/list.txt"
grep -li 'sgcaptcha\|cf-challenge\|Just a moment' "$OUT"/pages/*.html 2>/dev/null && echo "WARNING: bot-protection pages above - delete them, raise PACE, re-run" || true
echo "pages: $(ls "$OUT/pages" | wc -l)"
