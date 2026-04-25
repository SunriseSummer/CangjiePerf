// Hand-written quicksort — micro-benchmark (Rust).
use std::env;
use std::time::Instant;

fn quicksort(a: &mut [i64], mut lo: i64, mut hi: i64) {
    while lo < hi {
        let mid = (lo + hi) >> 1;
        let pivot = a[mid as usize];
        a.swap(mid as usize, hi as usize);
        let mut i = lo - 1;
        let mut j = lo;
        while j < hi {
            if a[j as usize] <= pivot {
                i += 1;
                a.swap(i as usize, j as usize);
            }
            j += 1;
        }
        i += 1;
        a.swap(i as usize, hi as usize);
        if (i - lo) < (hi - i) {
            quicksort(a, lo, i - 1);
            lo = i + 1;
        } else {
            quicksort(a, i + 1, hi);
            hi = i - 1;
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(1_500_000) } else { 1_500_000 };
    let mut a: Vec<i64> = vec![0; n as usize];
    let mut seed: i64 = 1234567;
    let mask: i64 = 0x7FFFFFFF;
    for i in 0..n as usize {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & mask;
        a[i] = seed;
    }
    let t0 = Instant::now();
    quicksort(&mut a, 0, n - 1);
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let mut cs: i64 = 0;
    let mut k: i64 = 0;
    while k < n {
        cs ^= a[k as usize];
        k += 1024;
    }
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
