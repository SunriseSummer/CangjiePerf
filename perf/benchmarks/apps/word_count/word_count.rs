// Word-count — typical text-processing application benchmark (Rust).
use std::collections::HashMap;
use std::env;
use std::fmt::Write;
use std::time::Instant;

fn gen_text(n: i64) -> String {
    let mut seed: i64 = 12345;
    let mut s = String::with_capacity((n as usize) * 7);
    for i in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFFFFFF;
        let idx = seed % 1024;
        let _ = write!(&mut s, "w{:04}", idx);
        if i % 12 == 11 {
            s.push('\n');
        } else {
            s.push(' ');
        }
    }
    s
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(1_000_000) } else { 1_000_000 };
    let text = gen_text(n);
    let bytes = text.as_bytes();

    let t0 = Instant::now();
    let mut counts: HashMap<&str, i64> = HashMap::with_capacity(2048);
    let mut i: usize = 0;
    let sz = bytes.len();
    while i < sz {
        while i < sz && (bytes[i] == b' ' || bytes[i] == b'\n') { i += 1; }
        let start = i;
        while i < sz && bytes[i] != b' ' && bytes[i] != b'\n' { i += 1; }
        if i > start {
            // Safe: ASCII-only generator above, so [start..i] is valid UTF-8.
            let key = unsafe { std::str::from_utf8_unchecked(&bytes[start..i]) };
            *counts.entry(key).or_insert(0) += 1;
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;

    let mut cs: i64 = 0;
    for (k, v) in counts.iter() {
        let idx: i64 = k[1..].parse().unwrap_or(0);
        cs ^= idx.wrapping_mul(1000003).wrapping_add(*v);
    }
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
