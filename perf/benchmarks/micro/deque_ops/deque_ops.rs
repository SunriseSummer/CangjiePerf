// deque_ops — dynamic-array push/pop micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(2_000_000) } else { 2_000_000 };
    let t0 = Instant::now();
    let mut a: Vec<i64> = Vec::new();
    let mut seed: i64 = 1;
    for _ in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        a.push(seed);
    }
    let mut cs: i64 = 0;
    while let Some(v) = a.pop() {
        cs ^= v;
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
