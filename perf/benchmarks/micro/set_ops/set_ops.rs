// set_ops — HashSet insert + membership micro-benchmark (Rust).
use std::collections::HashSet;
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(500_000) } else { 500_000 };
    let t0 = Instant::now();
    let mut s: HashSet<i64> = HashSet::with_capacity(n as usize);
    let mut seed: i64 = 1;
    let mod_v: i64 = n * 2;
    for _ in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        s.insert(seed % mod_v);
    }
    let mut found: i64 = 0;
    for _ in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        if s.contains(&(seed % mod_v)) {
            found += 1;
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", found);
    println!("ELAPSED_MS:{:.6}", ms);
}
