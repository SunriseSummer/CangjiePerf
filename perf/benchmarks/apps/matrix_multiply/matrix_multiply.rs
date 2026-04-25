// Matrix multiplication — naive O(N^3) double-precision matmul (Rust).
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: usize = if args.len() > 1 { args[1].parse().unwrap_or(250) } else { 250 };
    let mut a: Vec<f64> = vec![0.0; n * n];
    let mut b: Vec<f64> = vec![0.0; n * n];
    let mut c: Vec<f64> = vec![0.0; n * n];
    for i in 0..n {
        for j in 0..n {
            a[i * n + j] = ((i as i64 * 7 + j as i64 * 13) % 100) as f64 * 0.01;
            b[i * n + j] = ((i as i64 * 11 + j as i64 * 17) % 100) as f64 * 0.01;
        }
    }
    let t0 = Instant::now();
    for i in 0..n {
        for k in 0..n {
            let aik = a[i * n + k];
            let (bk_off, ci_off) = (k * n, i * n);
            for j in 0..n {
                c[ci_off + j] += aik * b[bk_off + j];
            }
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let mut total = 0.0;
    for i in 0..n {
        total += c[i * n + i];
    }
    let cs = (total * 1e6).round() as i64;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
