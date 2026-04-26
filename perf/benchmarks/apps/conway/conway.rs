// conway — Game of Life N-step application benchmark (Rust).
use std::env;
use std::time::Instant;

const W: usize = 200;

fn main() {
    let args: Vec<String> = env::args().collect();
    let steps: i64 = if args.len() > 1 { args[1].parse().unwrap_or(200) } else { 200 };

    let cells = W * W;
    let mut grid: Vec<u8> = vec![0; cells];
    let mut nxt: Vec<u8> = vec![0; cells];
    let mut seed: i64 = 1;
    for i in 0..cells {
        seed = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFF_FFFF;
        grid[i] = if ((seed >> 16) & 3) < 2 { 1 } else { 0 };
    }

    let t0 = Instant::now();
    for _ in 0..steps {
        for y in 0..W {
            let yu = (y + W - 1) % W;
            let yd = (y + 1) % W;
            let row = y * W;
            let row_u = yu * W;
            let row_d = yd * W;
            for x in 0..W {
                let xl = (x + W - 1) % W;
                let xr = (x + 1) % W;
                let n = grid[row_u + xl] + grid[row_u + x] + grid[row_u + xr]
                      + grid[row + xl] + grid[row + xr]
                      + grid[row_d + xl] + grid[row_d + x] + grid[row_d + xr];
                let alive = grid[row + x];
                nxt[row + x] = if alive != 0 {
                    if n == 2 || n == 3 { 1 } else { 0 }
                } else if n == 3 { 1 } else { 0 };
            }
        }
        std::mem::swap(&mut grid, &mut nxt);
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let cs: i64 = grid.iter().map(|&c| c as i64).sum();
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
