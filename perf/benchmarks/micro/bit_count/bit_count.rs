// bit_count — popcount tight-loop micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(5_000_000) } else { 5_000_000 };
    let t0 = Instant::now();
    let mut cs: i64 = 0;
    for i in 0..n {
        let v: u32 = (i as u64).wrapping_mul(2654435761) as u32;
        let mut x = v;
        let mut c: i64 = 0;
        while x != 0 {
            x &= x - 1;
            c += 1;
        }
        cs += c;
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
