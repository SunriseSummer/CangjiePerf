// Spectral norm — CLBG numerical kernel (Rust).
use std::env;
use std::time::Instant;

#[inline]
fn a(i: i64, j: i64) -> f64 {
    1.0 / ((((i + j) * (i + j + 1)) >> 1) + i + 1) as f64
}

fn av(v: &[f64], out: &mut [f64], n: usize) {
    for i in 0..n {
        let mut s = 0.0;
        for j in 0..n {
            s += a(i as i64, j as i64) * v[j];
        }
        out[i] = s;
    }
}

fn atv(v: &[f64], out: &mut [f64], n: usize) {
    for i in 0..n {
        let mut s = 0.0;
        for j in 0..n {
            s += a(j as i64, i as i64) * v[j];
        }
        out[i] = s;
    }
}

fn atav(v: &[f64], out: &mut [f64], tmp: &mut [f64], n: usize) {
    av(v, tmp, n);
    atv(tmp, out, n);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: usize = if args.len() > 1 { args[1].parse().unwrap_or(1500) } else { 1500 };
    let mut u: Vec<f64> = vec![1.0; n];
    let mut v: Vec<f64> = vec![0.0; n];
    let mut tmp: Vec<f64> = vec![0.0; n];

    let t0 = Instant::now();
    for _ in 0..10 {
        atav(&u, &mut v, &mut tmp, n);
        atav(&v, &mut u, &mut tmp, n);
    }
    let mut vbv = 0.0;
    let mut vv = 0.0;
    for i in 0..n {
        vbv += u[i] * v[i];
        vv += v[i] * v[i];
    }
    let sn = (vbv / vv).sqrt();
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let cs = (sn * 1e9).round() as i64;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
