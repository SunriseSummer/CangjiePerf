// N-Body — application-style numerical benchmark (Cangjie).
// Adapted from the Computer Language Benchmarks Game.
package nbody

import std.math.*
import std.time.*
import std.process.*
import std.convert.*

const PI: Float64 = 3.141592653589793
const SOLAR_MASS: Float64 = 4.0 * PI * PI
const DAYS_PER_YEAR: Float64 = 365.24
const N_BODIES: Int64 = 5

class Body {
    var x: Float64
    var y: Float64
    var z: Float64
    var vx: Float64
    var vy: Float64
    var vz: Float64
    var mass: Float64

    init(x: Float64, y: Float64, z: Float64,
         vx: Float64, vy: Float64, vz: Float64, mass: Float64) {
        this.x = x; this.y = y; this.z = z
        this.vx = vx; this.vy = vy; this.vz = vz
        this.mass = mass
    }
}

func makeBodies(): Array<Body> {
    let bs = Array<Body>(N_BODIES, repeat: Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    bs[0] = Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS)
    bs[1] = Body(
        4.84143144246472090e+00,
       -1.16032004402742839e+00,
       -1.03622044471123109e-01,
        1.66007664274403694e-03 * DAYS_PER_YEAR,
        7.69901118419740425e-03 * DAYS_PER_YEAR,
       -6.90460016972063023e-05 * DAYS_PER_YEAR,
        9.54791938424326609e-04 * SOLAR_MASS
    )
    bs[2] = Body(
        8.34336671824457987e+00,
        4.12479856412430479e+00,
       -4.03523417114321381e-01,
       -2.76742510726862411e-03 * DAYS_PER_YEAR,
        4.99852801234917238e-03 * DAYS_PER_YEAR,
        2.30417297573763929e-05 * DAYS_PER_YEAR,
        2.85885980666130812e-04 * SOLAR_MASS
    )
    bs[3] = Body(
        1.28943695621391310e+01,
       -1.51111514016986312e+01,
       -2.23307578892655734e-01,
        2.96460137564761618e-03 * DAYS_PER_YEAR,
        2.37847173959480950e-03 * DAYS_PER_YEAR,
       -2.96589568540237556e-05 * DAYS_PER_YEAR,
        4.36624404335156298e-05 * SOLAR_MASS
    )
    bs[4] = Body(
        1.53796971148509165e+01,
       -2.59193146099879641e+01,
        1.79258772950371181e-01,
        2.68067772490389322e-03 * DAYS_PER_YEAR,
        1.62824170038242295e-03 * DAYS_PER_YEAR,
       -9.51592254519715870e-05 * DAYS_PER_YEAR,
        5.15138902046611451e-05 * SOLAR_MASS
    )
    return bs
}

func offsetMomentum(bodies: Array<Body>) {
    var px: Float64 = 0.0
    var py: Float64 = 0.0
    var pz: Float64 = 0.0
    for (i in 0..N_BODIES) {
        px += bodies[i].vx * bodies[i].mass
        py += bodies[i].vy * bodies[i].mass
        pz += bodies[i].vz * bodies[i].mass
    }
    bodies[0].vx = -px / SOLAR_MASS
    bodies[0].vy = -py / SOLAR_MASS
    bodies[0].vz = -pz / SOLAR_MASS
}

func energy(bodies: Array<Body>): Float64 {
    var e: Float64 = 0.0
    for (i in 0..N_BODIES) {
        let bi = bodies[i]
        e += 0.5 * bi.mass * (bi.vx * bi.vx + bi.vy * bi.vy + bi.vz * bi.vz)
        for (j in (i + 1)..N_BODIES) {
            let bj = bodies[j]
            let dx = bi.x - bj.x
            let dy = bi.y - bj.y
            let dz = bi.z - bj.z
            let d = sqrt(dx * dx + dy * dy + dz * dz)
            e -= bi.mass * bj.mass / d
        }
    }
    return e
}

func advance(bodies: Array<Body>, dt: Float64) {
    for (i in 0..N_BODIES) {
        let bi = bodies[i]
        for (j in (i + 1)..N_BODIES) {
            let bj = bodies[j]
            let dx = bi.x - bj.x
            let dy = bi.y - bj.y
            let dz = bi.z - bj.z
            let d2 = dx * dx + dy * dy + dz * dz
            let mag = dt / (d2 * sqrt(d2))
            let bm = bj.mass * mag
            bi.vx -= dx * bm
            bi.vy -= dy * bm
            bi.vz -= dz * bm
            let am = bi.mass * mag
            bj.vx += dx * am
            bj.vy += dy * am
            bj.vz += dz * am
        }
    }
    for (i in 0..N_BODIES) {
        bodies[i].x += dt * bodies[i].vx
        bodies[i].y += dt * bodies[i].vy
        bodies[i].z += dt * bodies[i].vz
    }
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 200_000 }
    let bodies = makeBodies()
    offsetMomentum(bodies)

    let start = MonoTime.now()
    for (_ in 0..n) {
        advance(bodies, 0.01)
    }
    let e = energy(bodies)
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0

    // Round to an integer (e * 1e9) so all 3 implementations produce the
    // exact same CHECKSUM string, despite tiny FP reordering effects.
    let cs: Int64 = Int64(round(e * 1.0e9))
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
