// gcd_loop — Euclidean GCD tight-loop micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(2_000_000) } else { 2_000_000 };
    let t0 = Instant::now();
    let mut cs: i64 = 0;
    let mut seed: i64 = 1;
    for i in 1..=n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        cs = (cs + gcd(i, seed)) & 0x7FFF_FFFF;
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
