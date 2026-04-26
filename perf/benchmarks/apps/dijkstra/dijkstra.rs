// dijkstra — dense-graph SSSP application benchmark (Rust).
use std::env;
use std::time::Instant;

const INF: i32 = 1 << 30;

fn main() {
    let args: Vec<String> = env::args().collect();
    let v: usize = if args.len() > 1 { args[1].parse().unwrap_or(800) } else { 800 };
    let mut seed: i64 = 1;
    let mut g: Vec<i32> = vec![0; v * v];
    for i in 0..v {
        for j in 0..v {
            seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
            g[i * v + j] = 1 + ((seed >> 8) % 100) as i32;
        }
        g[i * v + i] = 0;
    }

    let t0 = Instant::now();
    let mut dist: Vec<i32> = vec![INF; v];
    let mut visited: Vec<bool> = vec![false; v];
    dist[0] = 0;
    for _ in 0..v {
        let mut u: isize = -1;
        let mut best = INF;
        for k in 0..v {
            if !visited[k] && dist[k] < best {
                best = dist[k];
                u = k as isize;
            }
        }
        if u < 0 { break; }
        let u = u as usize;
        visited[u] = true;
        let du = dist[u];
        let base = u * v;
        for k in 0..v {
            let nd = du + g[base + k];
            if nd < dist[k] { dist[k] = nd; }
        }
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let mut cs: i64 = 0;
    for &d in &dist { cs ^= d as i64; }
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
