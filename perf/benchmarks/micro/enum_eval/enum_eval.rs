// Enum / algebraic-data-type recursive pattern matching — micro-benchmark (Rust).
use std::env;
use std::time::Instant;

enum Expr {
    Num(i64),
    Add(Box<Expr>, Box<Expr>),
    Sub(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}

fn build(depth: i32, seed: i64) -> Box<Expr> {
    if depth == 0 {
        return Box::new(Expr::Num((seed & 0x3F) + 1));
    }
    let s: i64 = (seed.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7FFFFFFF;
    let tag = (s >> 17) & 3;
    let left = build(depth - 1, s);
    let right = build(depth - 1, s ^ 0xABCDEF);
    Box::new(match tag {
        0 => Expr::Add(left, right),
        1 => Expr::Sub(left, right),
        2 => Expr::Mul(left, right),
        _ => Expr::Add(left, right),
    })
}

fn eval(e: &Expr) -> i64 {
    match e {
        Expr::Num(v) => *v,
        Expr::Add(l, r) => eval(l).wrapping_add(eval(r)),
        Expr::Sub(l, r) => eval(l).wrapping_sub(eval(r)),
        Expr::Mul(l, r) => eval(l).wrapping_mul(eval(r)),
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let depth: i32 = if args.len() > 1 { args[1].parse().unwrap_or(18) } else { 18 };
    let n: i32 = if args.len() > 2 { args[2].parse().unwrap_or(60) } else { 60 };
    let tree = build(depth, 1);

    let t0 = Instant::now();
    let mut cs: i64 = 0;
    for _ in 0..n {
        cs ^= eval(&tree);
    }
    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", cs);
    println!("ELAPSED_MS:{:.6}", ms);
}
