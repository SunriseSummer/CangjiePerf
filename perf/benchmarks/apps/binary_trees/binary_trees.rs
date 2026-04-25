// Binary trees — heap-allocation pressure benchmark (Rust).
//
// Uses Box<Node> directly so we exercise the heap allocator on every node,
// paralleling the C++/Cangjie/Go versions (which all build many small heap
// nodes). This is the point of the benchmark.
use std::env;
use std::time::Instant;

struct Node {
    l: Option<Box<Node>>,
    r: Option<Box<Node>>,
}

fn make_tree(depth: i32) -> Box<Node> {
    if depth == 0 {
        Box::new(Node { l: None, r: None })
    } else {
        Box::new(Node {
            l: Some(make_tree(depth - 1)),
            r: Some(make_tree(depth - 1)),
        })
    }
}

fn check_tree(n: &Node) -> i64 {
    match &n.l {
        None => 1,
        Some(l) => match &n.r {
            None => 1,
            Some(r) => 1 + check_tree(l) + check_tree(r),
        },
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let max_depth: i32 = if args.len() > 1 { args[1].parse().unwrap_or(14) } else { 14 };
    let min_depth: i32 = 4;
    let stretch_depth: i32 = max_depth + 1;

    let t0 = Instant::now();

    let stretch = check_tree(&make_tree(stretch_depth));
    let long_lived = make_tree(max_depth);

    let mut total: i64 = stretch;
    let mut d = min_depth;
    while d <= max_depth {
        let iterations: i64 = 1i64 << (max_depth - d + min_depth) as i64;
        let mut s: i64 = 0;
        for _ in 0..iterations {
            s += check_tree(&make_tree(d));
        }
        total ^= iterations.wrapping_mul(1000003).wrapping_add(s);
        d += 2;
    }
    total ^= check_tree(&long_lived);

    let ms = t0.elapsed().as_nanos() as f64 / 1_000_000.0;
    println!("CHECKSUM:{}", total);
    println!("ELAPSED_MS:{:.6}", ms);
}
