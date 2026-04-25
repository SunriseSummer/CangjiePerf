// Sort N integers — stdlib-sort micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(2_000_000) } else { 2_000_000 };
    let mut arr: Vec<i64> = vec![0; n as usize];
    let mut seed: i64 = 12345;
    for i in 0..n as usize {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFFFFFF;
        arr[i] = seed;
    }
    let t0 = Instant::now();
    arr.sort();
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let cs = arr[0] ^ arr[(n / 2) as usize] ^ arr[(n - 1) as usize];
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
