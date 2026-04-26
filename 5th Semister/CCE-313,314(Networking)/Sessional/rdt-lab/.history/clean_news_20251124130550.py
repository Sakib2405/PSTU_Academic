import re
import json
import argparse
from pathlib import Path

# Unicode ranges:
# Bengali: \u0980-\u09FF
# Bengali digits: \u09E6-\u09EF

AD_MARKERS = [
    'বিজ্ঞাপন', 'Advertisement', 'PRIVACY POLICY', 'TERMS OF USE', 'ই-মেইল', 'ই-মেইল:', 'ফোন', 'ফোন :', 'ফোন:', 'ই-মেইল', 'marketing', 'Advertise', 'বিজ্ঞাপ', 'Contact', 'Phone', 'email', 'www.', 'http', 'https', 'SAMAKAL', 'সমকাল', 'সাম্প্রতিক'
]

URL_RE = re.compile(r'https?://\S+|www\.\S+')
EMAIL_RE = re.compile(r'\S+@\S+')
PHONE_RE = re.compile(r'(?:\+?\d[\d\-\s]{6,}\d)')
LATIN_RE = re.compile(r'[A-Za-z]')

# Keep Bengali letters, Bengali digits, common punctuation and whitespace and Bengali danda (।)
KEEP_RE = re.compile(r'[^\u0980-\u09FF\u09E6-\u09EF\s\d\.,"\'\:\;\?\!\(\)\-\–\—।]')


def clean_article(text: str) -> str:
    # Split into lines and remove lines that look like ads/contact/meta
    lines = text.splitlines()
    kept_lines = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        # Drop if contains obvious ad markers or English-only lines with uppercase keywords
        low = s.lower()
        if any(marker.lower() in low for marker in AD_MARKERS):
            continue
        if 'privacy policy' in low or 'terms of use' in low:
            continue
        # Remove urls, emails, phone numbers inside line
        s = URL_RE.sub(' ', s)
        s = EMAIL_RE.sub(' ', s)
        s = PHONE_RE.sub(' ', s)
        # If after removing urls/emails the line has many latin letters and few bengali letters, drop it
        bengali_chars = re.findall(r'[\u0980-\u09FF]', s)
        latin_chars = LATIN_RE.findall(s)
        if len(bengali_chars) == 0 and len(latin_chars) > 5:
            continue
        # Remove characters not in keep set
        s = KEEP_RE.sub(' ', s)
        s = re.sub(r'\s+', ' ', s).strip()
        if s:
            kept_lines.append(s)

    cleaned = ' '.join(kept_lines)
    # Final normalization: collapse repeated punctuation and whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # If cleaned is mostly non-bangla, return empty
    bengali_count = len(re.findall(r'[\u0980-\u09FF]', cleaned))
    non_space_len = len(cleaned.replace(' ', ''))
    if non_space_len == 0:
        return ''
    bangla_ratio = bengali_count / non_space_len
    # Heuristic thresholds: must have at least 20 bengali chars and bangla ratio >= 0.3
    if bengali_count < 20 or bangla_ratio < 0.25:
        return ''
    return cleaned


def main(input_path: Path, output_path: Path, min_len: int = 20):
    data = json.loads(input_path.read_text(encoding='utf-8'))
    cleaned = {}
    stats = {
        'total_categories': 0,
        'total_articles': 0,
        'kept_articles': 0,
        'dropped_articles': 0
    }

    for cat, articles in data.items():
        stats['total_categories'] += 1
        cleaned_list = []
        for art in articles:
            stats['total_articles'] += 1
            # some entries might already be not strings
            if not isinstance(art, str):
                stats['dropped_articles'] += 1
                continue
            out = clean_article(art)
            if out and len(out) >= min_len:
                cleaned_list.append(out)
                stats['kept_articles'] += 1
            else:
                stats['dropped_articles'] += 1
        if cleaned_list:
            cleaned[cat] = cleaned_list

    output_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding='utf-8')
    log = {
        'stats': stats,
        'output_path': str(output_path)
    }
    print(json.dumps(log, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean Bangla news dataset JSON')
    parser.add_argument('input', help='Path to input JSON file')
    parser.add_argument('output', nargs='?', help='Path to output cleaned JSON file', default=None)
    args = parser.parse_args()
    ip = Path(args.input)
    op = Path(args.output) if args.output else ip.with_name(ip.stem + '_cleaned.json')
    main(ip, op)
