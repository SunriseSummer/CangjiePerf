// Fibonacci — recursive function-call micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn fib(n: i64) -> i64 {
    if n < 2 {
        return n;
    }
    fib(n - 1) + fib(n - 2)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(32) } else { 32 };
    let t0 = Instant::now();
    let result = fib(n);
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", result);
    println!("ELAPSED_MS:{:.6}", ms);
}
