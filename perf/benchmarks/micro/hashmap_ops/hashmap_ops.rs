// HashMap insert + lookup — stdlib hash-table micro-benchmark (Rust).
use std::collections::HashMap;
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(500_000) } else { 500_000 };

    let mut keys: Vec<String> = Vec::with_capacity(n as usize);
    for i in 0..n {
        keys.push(format!("key-{}", i));
    }

    let t0 = Instant::now();
    let mut m: HashMap<String, i64> = HashMap::with_capacity(n as usize);
    for i in 0..n as usize {
        m.insert(keys[i].clone(), i as i64);
    }
    let mut cs: i64 = 0;
    for i in 0..n as usize {
        if let Some(&v) = m.get(&keys[i]) {
            cs ^= v;
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
