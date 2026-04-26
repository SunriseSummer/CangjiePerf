// histogram — bucket-counts of LCG ints application benchmark (Rust).
use std::env;
use std::time::Instant;

const K: usize = 1024;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(5_000_000) } else { 5_000_000 };
    let t0 = Instant::now();
    let mut buckets: Vec<i64> = vec![0; K];
    let mut seed: i64 = 1;
    for _ in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        buckets[((seed >> 8) as usize) & (K - 1)] += 1;
    }
    let mut cs: i64 = 0;
    for v in &buckets { cs ^= v; }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
