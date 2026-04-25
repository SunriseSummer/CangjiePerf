// Regex find-all — micro-benchmark (Rust, hand-rolled scanner).
//
// Rust's standard library does not include a regex engine, so to keep this
// benchmark self-contained (no external crates) we hand-implement an
// equivalent scanner for the same alternation pattern used by the other
// implementations:
//
//     (\d{4}-\d{2}-\d{2})            date
//   | ([A-Za-z]+@[a-z]+\.[a-z]+)     email
//   | (\b[A-Z][a-z]{3,8}\b)          capitalized word
//
// As with `regexp.FindAllStringIndex` (Go) and `re.finditer` (Python), we
// scan left-to-right, take the leftmost alternative when several match at
// the same position, and advance past every match. This produces the same
// match count as the regex-based implementations.
use std::env;
use std::time::Instant;

const SAMPLE: &str =
    "On 2024-03-21 Alice wrote to bob@example.com about the meeting. \
     Charlie replied 2024-04-02 from charlie_99@dev.io with notes about \
     Project Kingfisher. References: 1999-12-31, foo@bar.org, Madison.";

#[inline]
fn is_digit(b: u8) -> bool { b.is_ascii_digit() }
#[inline]
fn is_lower(b: u8) -> bool { b.is_ascii_lowercase() }
#[inline]
fn is_upper(b: u8) -> bool { b.is_ascii_uppercase() }
#[inline]
fn is_alpha(b: u8) -> bool { is_lower(b) || is_upper(b) }
#[inline]
fn is_word(b: u8) -> bool { is_alpha(b) || is_digit(b) || b == b'_' }

// Try to match a date `\d{4}-\d{2}-\d{2}` starting at `i`; return its length.
fn match_date(s: &[u8], i: usize) -> usize {
    if i + 10 > s.len() { return 0; }
    for k in [0, 1, 2, 3, 5, 6, 8, 9] {
        if !is_digit(s[i + k]) { return 0; }
    }
    if s[i + 4] != b'-' || s[i + 7] != b'-' { return 0; }
    10
}

// Try to match `[A-Za-z]+@[a-z]+\.[a-z]+` starting at `i`; return its length.
fn match_email(s: &[u8], i: usize) -> usize {
    let mut p = i;
    let n = s.len();
    let start = p;
    while p < n && is_alpha(s[p]) { p += 1; }
    if p == start { return 0; }
    if p >= n || s[p] != b'@' { return 0; }
    p += 1;
    let h0 = p;
    while p < n && is_lower(s[p]) { p += 1; }
    if p == h0 { return 0; }
    if p >= n || s[p] != b'.' { return 0; }
    p += 1;
    let t0 = p;
    while p < n && is_lower(s[p]) { p += 1; }
    if p == t0 { return 0; }
    p - i
}

// Try to match `\b[A-Z][a-z]{3,8}\b` starting at `i`; return its length.
fn match_capword(s: &[u8], i: usize) -> usize {
    // Left word boundary: previous char must not be word-char.
    if i > 0 && is_word(s[i - 1]) { return 0; }
    let n = s.len();
    if i >= n || !is_upper(s[i]) { return 0; }
    let mut p = i + 1;
    let mut lower_count = 0;
    while p < n && is_lower(s[p]) && lower_count < 8 {
        p += 1;
        lower_count += 1;
    }
    if lower_count < 3 { return 0; }
    // Right word boundary: next char must not be word-char.
    if p < n && is_word(s[p]) { return 0; }
    p - i
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let repeats: usize = if args.len() > 1 { args[1].parse().unwrap_or(4000) } else { 4000 };

    let mut text = String::with_capacity(repeats * (SAMPLE.len() + 1));
    for _ in 0..repeats {
        text.push_str(SAMPLE);
        text.push('\n');
    }
    let bytes = text.as_bytes();

    let t0 = Instant::now();
    let mut count: i64 = 0;
    let mut i: usize = 0;
    let n = bytes.len();
    while i < n {
        // Leftmost alternative wins; advance past whichever matched.
        let mut len = match_date(bytes, i);
        if len == 0 { len = match_email(bytes, i); }
        if len == 0 { len = match_capword(bytes, i); }
        if len > 0 {
            count += 1;
            i += len;
        } else {
            i += 1;
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", count);
    println!("ELAPSED_MS:{:.6}", ms);
}
