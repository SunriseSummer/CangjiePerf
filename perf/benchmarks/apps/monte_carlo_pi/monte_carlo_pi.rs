// monte_carlo_pi — integer-only Monte-Carlo PI count benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(5_000_000) } else { 5_000_000 };
    const R: i64 = 65536;
    const R2: i64 = R * R;
    let t0 = Instant::now();
    let mut seed: i64 = 1;
    let mut inside: i64 = 0;
    for _ in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        let x = seed % R;
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        let y = seed % R;
        if x * x + y * y <= R2 { inside += 1; }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", inside);
    println!("ELAPSED_MS:{:.6}", ms);
}
