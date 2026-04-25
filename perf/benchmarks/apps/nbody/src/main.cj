package nbody

import std.math.*
import std.time.*

let PI = 3.141592653589793
let SOLAR_MASS = 4.0 * PI * PI
let DAYS_PER_YEAR = 365.24

class Body {
    var x: Float64
    var y: Float64
    var z: Float64
    var vx: Float64
    var vy: Float64
    var vz: Float64
    var mass: Float64

    init(x!: Float64 = 0.0, y!: Float64 = 0.0, z!: Float64 = 0.0,
         vx!: Float64 = 0.0, vy!: Float64 = 0.0, vz!: Float64 = 0.0,
         mass!: Float64 = 0.0) {
        this.x = x
        this.y = y
        this.z = z
        this.vx = vx
        this.vy = vy
        this.vz = vz
        this.mass = mass
    }
}

func advance(bodies: Array<Body>, dt: Float64): Unit {
    let n = bodies.size
    for (i in 0..n) {
        for (j in (i + 1)..n) {
            let dx = bodies[i].x - bodies[j].x
            let dy = bodies[i].y - bodies[j].y
            let dz = bodies[i].z - bodies[j].z
            let dist2 = dx * dx + dy * dy + dz * dz
            let dist = sqrt(dist2)
            let mag = dt / (dist2 * dist)
            bodies[i].vx -= dx * bodies[j].mass * mag
            bodies[i].vy -= dy * bodies[j].mass * mag
            bodies[i].vz -= dz * bodies[j].mass * mag
            bodies[j].vx += dx * bodies[i].mass * mag
            bodies[j].vy += dy * bodies[i].mass * mag
            bodies[j].vz += dz * bodies[i].mass * mag
        }
    }
    for (i in 0..n) {
        bodies[i].x += dt * bodies[i].vx
        bodies[i].y += dt * bodies[i].vy
        bodies[i].z += dt * bodies[i].vz
    }
}

func energy(bodies: Array<Body>): Float64 {
    let n = bodies.size
    var e = 0.0
    for (i in 0..n) {
        e += 0.5 * bodies[i].mass * (bodies[i].vx * bodies[i].vx + bodies[i].vy * bodies[i].vy + bodies[i].vz * bodies[i].vz)
        for (j in (i + 1)..n) {
            let dx = bodies[i].x - bodies[j].x
            let dy = bodies[i].y - bodies[j].y
            let dz = bodies[i].z - bodies[j].z
            let dist = sqrt(dx * dx + dy * dy + dz * dz)
            e -= bodies[i].mass * bodies[j].mass / dist
        }
    }
    return e
}

main(): Int64 {
    let sun = Body(mass: SOLAR_MASS)
    let jupiter = Body(
        x: 4.84143144246472090,
        y: -1.16032004402742839,
        z: -0.103622044471883028,
        vx: 0.00166007664274403694 * DAYS_PER_YEAR,
        vy: 0.00769901118419740425 * DAYS_PER_YEAR,
        vz: -0.0000690460016972063023 * DAYS_PER_YEAR,
        mass: 0.000954791938424326609 * SOLAR_MASS
    )
    let saturn = Body(
        x: 8.34336671824457987,
        y: 4.12479856412430479,
        z: -0.403523417114321381,
        vx: -0.00276742510726862411 * DAYS_PER_YEAR,
        vy: 0.00499852801234917238 * DAYS_PER_YEAR,
        vz: 0.0000230417297573763929 * DAYS_PER_YEAR,
        mass: 0.000285885980666130812 * SOLAR_MASS
    )
    let uranus = Body(
        x: 12.8943695621391310,
        y: -15.1111514016986312,
        z: -0.223307578892655734,
        vx: 0.00296460137564761618 * DAYS_PER_YEAR,
        vy: 0.00237847173959480950 * DAYS_PER_YEAR,
        vz: -0.0000296589568540237556 * DAYS_PER_YEAR,
        mass: 0.0000436624404335156298 * SOLAR_MASS
    )
    let neptune = Body(
        x: 15.3796971148509165,
        y: -25.9193146099879641,
        z: 0.179258772950371181,
        vx: 0.00268067772490389322 * DAYS_PER_YEAR,
        vy: 0.00162824170038242295 * DAYS_PER_YEAR,
        vz: -0.0000951592254519715870 * DAYS_PER_YEAR,
        mass: 0.0000515138902046611451 * SOLAR_MASS
    )
    let bodies = [sun, jupiter, saturn, uranus, neptune]
    let n = 50000000
    let start = MonoTime.now()
    println("Initial energy: ${energy(bodies)}")
    for (_ in 0..n) {
        advance(bodies, 0.01)
    }
    println("Final energy:   ${energy(bodies)}")
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("N-body ${n} steps: ${ms} ms")
    return 0
}
