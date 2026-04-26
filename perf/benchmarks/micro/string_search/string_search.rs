// string_search — substring-search tight-loop micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let repeats: i64 = if args.len() > 1 { args[1].parse().unwrap_or(50_000) } else { 50_000 };

    let mut seed: i64 = 1;
    let mut hay = String::with_capacity(10_000);
    for _ in 0..10_000 {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        hay.push((b'a' + (seed % 8) as u8) as char);
    }
    let needle = "abcde";

    let t0 = Instant::now();
    let mut cs: i64 = 0;
    for r in 0..repeats {
        let mut count: i64 = 0;
        let mut pos: usize = 0;
        while let Some(i) = hay[pos..].find(needle) {
            count += 1;
            pos += i + 1;
        }
        cs ^= (r + 1) * 1_000_003 + count;
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
