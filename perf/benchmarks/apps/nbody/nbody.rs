// N-Body — 5-body solar system symplectic integrator (Rust).
use std::env;
use std::time::Instant;

const PI: f64 = 3.141592653589793;
const SOLAR_MASS: f64 = 4.0 * PI * PI;
const DAYS_PER_YEAR: f64 = 365.24;
const N_BODIES: usize = 5;

#[derive(Clone, Copy)]
struct Body {
    x: f64, y: f64, z: f64,
    vx: f64, vy: f64, vz: f64,
    mass: f64,
}

fn initial_bodies() -> [Body; N_BODIES] {
    [
        Body { x: 0.0, y: 0.0, z: 0.0, vx: 0.0, vy: 0.0, vz: 0.0, mass: SOLAR_MASS },
        Body {
            x:  4.84143144246472090e+00,
            y: -1.16032004402742839e+00,
            z: -1.03622044471123109e-01,
            vx: 1.66007664274403694e-03 * DAYS_PER_YEAR,
            vy: 7.69901118419740425e-03 * DAYS_PER_YEAR,
            vz:-6.90460016972063023e-05 * DAYS_PER_YEAR,
            mass: 9.54791938424326609e-04 * SOLAR_MASS,
        },
        Body {
            x:  8.34336671824457987e+00,
            y:  4.12479856412430479e+00,
            z: -4.03523417114321381e-01,
            vx:-2.76742510726862411e-03 * DAYS_PER_YEAR,
            vy: 4.99852801234917238e-03 * DAYS_PER_YEAR,
            vz: 2.30417297573763929e-05 * DAYS_PER_YEAR,
            mass: 2.85885980666130812e-04 * SOLAR_MASS,
        },
        Body {
            x:  1.28943695621391310e+01,
            y: -1.51111514016986312e+01,
            z: -2.23307578892655734e-01,
            vx: 2.96460137564761618e-03 * DAYS_PER_YEAR,
            vy: 2.37847173959480950e-03 * DAYS_PER_YEAR,
            vz:-2.96589568540237556e-05 * DAYS_PER_YEAR,
            mass: 4.36624404335156298e-05 * SOLAR_MASS,
        },
        Body {
            x:  1.53796971148509165e+01,
            y: -2.59193146099879641e+01,
            z:  1.79258772950371181e-01,
            vx: 2.68067772490389322e-03 * DAYS_PER_YEAR,
            vy: 1.62824170038242295e-03 * DAYS_PER_YEAR,
            vz:-9.51592254519715870e-05 * DAYS_PER_YEAR,
            mass: 5.15138902046611451e-05 * SOLAR_MASS,
        },
    ]
}

fn offset_momentum(b: &mut [Body; N_BODIES]) {
    let mut px = 0.0; let mut py = 0.0; let mut pz = 0.0;
    for bi in b.iter() {
        px += bi.vx * bi.mass;
        py += bi.vy * bi.mass;
        pz += bi.vz * bi.mass;
    }
    b[0].vx = -px / SOLAR_MASS;
    b[0].vy = -py / SOLAR_MASS;
    b[0].vz = -pz / SOLAR_MASS;
}

fn energy(b: &[Body; N_BODIES]) -> f64 {
    let mut e = 0.0;
    for i in 0..N_BODIES {
        let bi = &b[i];
        e += 0.5 * bi.mass * (bi.vx*bi.vx + bi.vy*bi.vy + bi.vz*bi.vz);
        for j in (i + 1)..N_BODIES {
            let bj = &b[j];
            let dx = bi.x - bj.x;
            let dy = bi.y - bj.y;
            let dz = bi.z - bj.z;
            let d = (dx*dx + dy*dy + dz*dz).sqrt();
            e -= bi.mass * bj.mass / d;
        }
    }
    e
}

fn advance(b: &mut [Body; N_BODIES], dt: f64) {
    for i in 0..N_BODIES {
        for j in (i + 1)..N_BODIES {
            let dx = b[i].x - b[j].x;
            let dy = b[i].y - b[j].y;
            let dz = b[i].z - b[j].z;
            let d2 = dx*dx + dy*dy + dz*dz;
            let mag = dt / (d2 * d2.sqrt());
            let bm = b[j].mass * mag;
            b[i].vx -= dx * bm;
            b[i].vy -= dy * bm;
            b[i].vz -= dz * bm;
            let am = b[i].mass * mag;
            b[j].vx += dx * am;
            b[j].vy += dy * am;
            b[j].vz += dz * am;
        }
    }
    for bi in b.iter_mut() {
        bi.x += dt * bi.vx;
        bi.y += dt * bi.vy;
        bi.z += dt * bi.vz;
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i64 = if args.len() > 1 { args[1].parse().unwrap_or(200_000) } else { 200_000 };
    let mut b = initial_bodies();
    offset_momentum(&mut b);

    let t0 = Instant::now();
    for _ in 0..n {
        advance(&mut b, 0.01);
    }
    let e = energy(&b);
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    let cs = (e * 1e9).round() as i64;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
