// crc32 — CRC32 of a deterministic byte stream application benchmark (Rust).
use std::env;
use std::time::Instant;

fn build_table() -> [u32; 256] {
    let mut t = [0u32; 256];
    for n in 0..256u32 {
        let mut c = n;
        for _ in 0..8 {
            c = (c >> 1) ^ if c & 1 != 0 { 0xEDB88320 } else { 0 };
        }
        t[n as usize] = c;
    }
    t
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: usize = if args.len() > 1 { args[1].parse().unwrap_or(5_000_000) } else { 5_000_000 };
    let mut src: Vec<u8> = vec![0; n];
    let mut seed: i64 = 1;
    for i in 0..n {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        src[i] = ((seed >> 8) & 0xFF) as u8;
    }
    let table = build_table();

    let t0 = Instant::now();
    let mut crc: u32 = 0xFFFF_FFFF;
    for i in 0..n {
        crc = table[((crc ^ src[i] as u32) & 0xFF) as usize] ^ (crc >> 8);
    }
    crc ^= 0xFFFF_FFFF;
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", crc);
    println!("ELAPSED_MS:{:.6}", ms);
}
