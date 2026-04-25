// Mandelbrot — application-style numerical benchmark (Rust).
use std::env;
use std::time::Instant;

fn mandelbrot(width: i32, max_iter: i32) -> i64 {
    let inv_w = 2.0 / width as f64;
    let mut total: i64 = 0;
    for py in 0..width {
        let ci = py as f64 * inv_w - 1.0;
        for px in 0..width {
            let cr = px as f64 * inv_w - 1.5;
            let mut zr: f64 = 0.0;
            let mut zi: f64 = 0.0;
            let mut n: i32 = 0;
            while n < max_iter {
                let zr2 = zr * zr;
                let zi2 = zi * zi;
                if zr2 + zi2 > 4.0 { break; }
                zi = 2.0 * zr * zi + ci;
                zr = zr2 - zi2 + cr;
                n += 1;
            }
            total += n as i64;
        }
    }
    total
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let width: i32 = if args.len() > 1 { args[1].parse().unwrap_or(600) } else { 600 };
    let max_iter: i32 = if args.len() > 2 { args[2].parse().unwrap_or(200) } else { 200 };
    let t0 = Instant::now();
    let cs = mandelbrot(width, max_iter);
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
