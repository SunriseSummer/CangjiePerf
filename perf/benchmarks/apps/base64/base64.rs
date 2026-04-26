// base64 — base64 encoding application benchmark (Rust).
use std::env;
use std::time::Instant;

const ALPHA: &[u8; 64] =
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: usize = if args.len() > 1 { args[1].parse().unwrap_or(2_000_000) } else { 2_000_000 };
    let mut src: Vec<u8> = vec![0; n];
    let mut seed: i64 = 1;
    for i in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        src[i] = ((seed >> 8) & 0xFF) as u8;
    }

    let t0 = Instant::now();
    let out_len = ((n + 2) / 3) * 4;
    let mut out: Vec<u8> = vec![0; out_len];
    let mut oi = 0;
    let mut i = 0;
    while i + 3 <= n {
        let b0 = src[i]; let b1 = src[i + 1]; let b2 = src[i + 2];
        out[oi]     = ALPHA[(b0 >> 2) as usize];
        out[oi + 1] = ALPHA[(((b0 & 0x3) << 4) | (b1 >> 4)) as usize];
        out[oi + 2] = ALPHA[(((b1 & 0xF) << 2) | (b2 >> 6)) as usize];
        out[oi + 3] = ALPHA[(b2 & 0x3F) as usize];
        oi += 4; i += 3;
    }
    let rem = n - i;
    if rem == 1 {
        let b0 = src[i];
        out[oi]     = ALPHA[(b0 >> 2) as usize];
        out[oi + 1] = ALPHA[((b0 & 0x3) << 4) as usize];
        out[oi + 2] = b'=';
        out[oi + 3] = b'=';
    } else if rem == 2 {
        let b0 = src[i]; let b1 = src[i + 1];
        out[oi]     = ALPHA[(b0 >> 2) as usize];
        out[oi + 1] = ALPHA[(((b0 & 0x3) << 4) | (b1 >> 4)) as usize];
        out[oi + 2] = ALPHA[((b1 & 0xF) << 2) as usize];
        out[oi + 3] = b'=';
    }
    let mut cs: i64 = 0;
    for v in &out { cs ^= *v as i64; }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
