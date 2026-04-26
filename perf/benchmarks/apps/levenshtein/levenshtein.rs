// levenshtein — edit-distance DP application benchmark (Rust).
use std::env;
use std::time::Instant;

fn make_str(mut seed: i64, n: usize) -> Vec<u8> {
    let mut v = Vec::with_capacity(n);
    for _ in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        v.push(b'a' + ((seed >> 16) & 7) as u8);
    }
    v
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: usize = if args.len() > 1 { args[1].parse().unwrap_or(1500) } else { 1500 };
    let a = make_str(1, n);
    let b = make_str(7, n);

    let t0 = Instant::now();
    let mut prev: Vec<i32> = (0..=n as i32).collect();
    let mut cur: Vec<i32> = vec![0; n + 1];
    for i in 1..=n {
        cur[0] = i as i32;
        let ai = a[i - 1];
        for j in 1..=n {
            let cost = if ai == b[j - 1] { 0 } else { 1 };
            let mut v = prev[j - 1] + cost;
            let d = cur[j - 1] + 1;
            if d < v { v = d; }
            let d = prev[j] + 1;
            if d < v { v = d; }
            cur[j] = v;
        }
        std::mem::swap(&mut prev, &mut cur);
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", prev[n]);
    println!("ELAPSED_MS:{:.6}", ms);
}
