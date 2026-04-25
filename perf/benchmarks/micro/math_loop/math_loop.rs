// Math-intensive loop — std math micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(5_000_000) } else { 5_000_000 };
    let t0 = Instant::now();
    let mut s: f64 = 0.0;
    let inv = 1.0 / n as f64;
    for i in 0..n {
        let x = i as f64 * inv;
        s += x.sin() * x.cos() + (x + 1.0).sqrt() - (-x).exp();
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let cs = (s * 1e6).round() as i64;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
