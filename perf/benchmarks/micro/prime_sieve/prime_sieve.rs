// Sieve of Eratosthenes — micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(20_000_000) } else { 20_000_000 };
    let t0 = Instant::now();
    let len = (n + 1) as usize;
    let mut sieve: Vec<u8> = vec![1u8; len];
    sieve[0] = 0;
    sieve[1] = 0;
    let mut i: i64 = 2;
    while i * i <= n {
        if sieve[i as usize] != 0 {
            let mut j = i * i;
            while j <= n {
                sieve[j as usize] = 0;
                j += i;
            }
        }
        i += 1;
    }
    let mut count: i64 = 0;
    let mut psum: i64 = 0;
    let mask: i64 = 0x7FFFFFFF;
    for k in 2..=n {
        if sieve[k as usize] != 0 {
            count += 1;
            psum = (psum + k) & mask;
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let cs = (count.wrapping_mul(1_000_003).wrapping_add(psum)) & mask;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
