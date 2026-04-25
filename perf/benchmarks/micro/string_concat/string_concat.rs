// String building — stdlib String/push_str micro-benchmark (Rust).
use std::env;
use std::fmt::Write;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(500_000) } else { 500_000 };
    let t0 = Instant::now();
    let mut s = String::with_capacity((n as usize) * 12);
    for i in 0..n {
        s.push_str("frag");
        // write! to avoid allocating an intermediate String for the integer.
        let _ = write!(&mut s, "{}", i);
        s.push(';');
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", s.len());
    println!("ELAPSED_MS:{:.6}", ms);
}
