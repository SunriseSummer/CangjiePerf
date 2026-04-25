// Binary trees — allocation pressure benchmark (C++).
//
// Build & check many small balanced binary trees. Uses raw new/delete on
// purpose so we measure heap-allocator pressure (paralleling Python/Cangjie
// GC pressure).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

struct Node {
    Node* l;
    Node* r;
};

static Node* make_tree(int depth) {
    Node* n = new Node();
    if (depth == 0) {
        n->l = nullptr;
        n->r = nullptr;
    } else {
        n->l = make_tree(depth - 1);
        n->r = make_tree(depth - 1);
    }
    return n;
}

static int64_t check_tree(const Node* n) {
    if (n->l == nullptr) return 1;
    return 1 + check_tree(n->l) + check_tree(n->r);
}

static void free_tree(Node* n) {
    if (n == nullptr) return;
    free_tree(n->l);
    free_tree(n->r);
    delete n;
}

int main(int argc, char** argv) {
    int max_depth = (argc > 1) ? std::atoi(argv[1]) : 14;
    int min_depth = 4;
    int stretch_depth = max_depth + 1;

    auto t0 = std::chrono::steady_clock::now();

    Node* stretch_tree = make_tree(stretch_depth);
    int64_t stretch = check_tree(stretch_tree);
    free_tree(stretch_tree);

    Node* long_lived = make_tree(max_depth);

    int64_t total = stretch;
    for (int d = min_depth; d <= max_depth; d += 2) {
        int64_t iterations = 1LL << (max_depth - d + min_depth);
        int64_t s = 0;
        for (int64_t i = 0; i < iterations; ++i) {
            Node* t = make_tree(d);
            s += check_tree(t);
            free_tree(t);
        }
        total ^= (iterations * 1000003LL + s);
    }
    total ^= check_tree(long_lived);
    free_tree(long_lived);

    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(total));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
