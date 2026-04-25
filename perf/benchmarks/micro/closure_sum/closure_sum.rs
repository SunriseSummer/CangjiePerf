// Closure / higher-order pipeline — micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(2_000_000) } else { 2_000_000 };
    let data: Vec<i64> = (0..n).collect();

    // Use boxed `dyn Fn` indirection to force closure-style indirect dispatch
    // (parallel to `std::function` in the C++ baseline). This keeps the
    // comparison fair across languages where closures are inherently boxed.
    let mapper: Box<dyn Fn(i64) -> i64> = Box::new(|x| x.wrapping_mul(x).wrapping_sub(7));
    let pred: Box<dyn Fn(i64) -> bool> = Box::new(|x| x % 3 == 0);
    let reducer: Box<dyn Fn(i64, i64) -> i64> = Box::new(|a, b| a.wrapping_add(b));

    let t0 = Instant::now();
    let mut cs: i64 = 0;
    for i in 0..n as usize {
        let v = mapper(data[i]);
        if pred(v) {
            cs = reducer(cs, v);
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
