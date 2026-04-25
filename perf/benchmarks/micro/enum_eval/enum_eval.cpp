// Enum / algebraic-data-type recursive pattern matching — micro-benchmark (C++).
//
// Mimics a sum type via a tagged class hierarchy: Num | Add | Sub | Mul.
// Builds a tree of depth D once, then evaluates it N times.
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>

enum class Tag { Num, Add, Sub, Mul };

struct Expr {
    Tag tag;
    int64_t v;                      // Num value
    std::unique_ptr<Expr> l, r;     // children
};

static std::unique_ptr<Expr> make_num(int64_t v) {
    auto e = std::make_unique<Expr>();
    e->tag = Tag::Num; e->v = v;
    return e;
}
static std::unique_ptr<Expr> make_op(Tag t,
                                     std::unique_ptr<Expr> l,
                                     std::unique_ptr<Expr> r) {
    auto e = std::make_unique<Expr>();
    e->tag = t; e->l = std::move(l); e->r = std::move(r);
    return e;
}

static std::unique_ptr<Expr> build(int depth, int64_t seed) {
    if (depth == 0) return make_num((seed & 0x3F) + 1);
    // Mask to keep `seed` non-negative and below 2^31, matching the Cangjie
    // and Python versions.
    int64_t s = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
    int tag = static_cast<int>((s >> 17) & 3);
    auto left  = build(depth - 1, s);
    auto right = build(depth - 1, s ^ 0xABCDEFLL);
    Tag t = (tag == 0) ? Tag::Add : (tag == 1) ? Tag::Sub
                                  : (tag == 2) ? Tag::Mul : Tag::Add;
    return make_op(t, std::move(left), std::move(right));
}

// Cast through unsigned to avoid signed-overflow UB while still wrapping
// like Cangjie's `wrappingAdd`/`wrappingMul`.
static int64_t wadd(int64_t a, int64_t b) {
    return static_cast<int64_t>(static_cast<uint64_t>(a) + static_cast<uint64_t>(b));
}
static int64_t wsub(int64_t a, int64_t b) {
    return static_cast<int64_t>(static_cast<uint64_t>(a) - static_cast<uint64_t>(b));
}
static int64_t wmul(int64_t a, int64_t b) {
    return static_cast<int64_t>(static_cast<uint64_t>(a) * static_cast<uint64_t>(b));
}

static int64_t evaluate(const Expr* e) {
    switch (e->tag) {
        case Tag::Num: return e->v;
        case Tag::Add: return wadd(evaluate(e->l.get()), evaluate(e->r.get()));
        case Tag::Sub: return wsub(evaluate(e->l.get()), evaluate(e->r.get()));
        case Tag::Mul: return wmul(evaluate(e->l.get()), evaluate(e->r.get()));
    }
    return 0;
}

int main(int argc, char** argv) {
    int depth = (argc > 1) ? std::atoi(argv[1]) : 18;
    int n     = (argc > 2) ? std::atoi(argv[2]) : 60;

    auto tree = build(depth, 1);

    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = 0;
    for (int i = 0; i < n; ++i) {
        cs ^= evaluate(tree.get());
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
