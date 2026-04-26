// xor_shift — xorshift64 PRNG tight-loop micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(50_000_000) } else { 50_000_000 };
    let t0 = Instant::now();
    let mut s: u64 = 0x123456789ABCDEF0;
    for _ in 0..n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", s);
    println!("ELAPSED_MS:{:.6}", ms);
}
