// knapsack_dp — 0/1 knapsack DP application benchmark (Rust).
use std::env;
use std::time::Instant;

const C: usize = 4000;
const MAXW: i64 = 200;
const MAXV: i64 = 1000;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: usize = if args.len() > 1 { args[1].parse().unwrap_or(1500) } else { 1500 };
    let mut w = vec![0i32; n];
    let mut v = vec![0i32; n];
    let mut seed: i64 = 1;
    for i in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        w[i] = (1 + seed % MAXW) as i32;
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        v[i] = (1 + seed % MAXV) as i32;
    }
    let t0 = Instant::now();
    let mut dp: Vec<i32> = vec![0; C + 1];
    for i in 0..n {
        let wi = w[i] as usize;
        let vi = v[i];
        let mut c = C;
        while c >= wi {
            let nv = dp[c - wi] + vi;
            if nv > dp[c] { dp[c] = nv; }
            c -= 1;
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", dp[C]);
    println!("ELAPSED_MS:{:.6}", ms);
}
