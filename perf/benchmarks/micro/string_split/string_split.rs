// string_split — repeated stdlib string-split micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let repeats: i64 = if args.len() > 1 { args[1].parse().unwrap_or(20_000) } else { 20_000 };

    // Build input once.
    let mut seed: i64 = 1;
    let mut parts: Vec<String> = Vec::with_capacity(64);
    for _ in 0..64 {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        parts.push(format!("tok{:05}", seed % 100000));
    }
    let s = parts.join(",");

    let t0 = Instant::now();
    let mut cs: i64 = 0;
    for r in 0..repeats {
        let toks: Vec<&str> = s.split(',').collect();
        let idx = (r as usize) % toks.len();
        cs ^= (r + 1) * 1_000_003 + (toks.len() as i64) + (toks[idx].len() as i64);
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
