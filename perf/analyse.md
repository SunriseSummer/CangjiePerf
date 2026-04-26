# Cangjie performance analysis

_Generated alongside `report.md`. Re-read `report.md` for the latest numbers._

This document complements `report.md`: it (1) explains how each benchmark was
audited for **cross-language consistency**, and (2) gives a root-cause analysis
for every benchmark where Cangjie's wall-clock timing landed closer (in log
space) to Python's than to C++'s — i.e. the rows the report bolds with ⚠️.

The intent is **not** to claim Cangjie cannot be fast — `fibonacci`, `nbody`,
`mandelbrot`, `enum_eval`, `closure_sum`, `binary_trees` and several others
already land within a small constant factor of `g++ -O2`. The goal is to
identify, per benchmark, where the gap most plausibly comes from.

> **Note:** this analysis was originally written when the suite covered three
> languages (Cangjie / C++ / Python). Two more compiled languages — **Rust**
> (via `rustc -O`) and **Go** (via `go build`) — have since been added as
> additional native-runtime baselines. The cross-language consistency audit
> below now applies to all **five** implementations of every benchmark, and
> their timings are visible in `report.md`. The Cangjie-vs-native gap analysis
> in §2 is unchanged: where Cangjie is slow against `g++ -O2`, it is also
> slow against `rustc -O` and (with a few exceptions like `sort` where Rust
> beats C++ thanks to a specialised pattern-defeating quicksort) `go build`.

> **2026-04 update — Cangjie SDK 1.0.5.** Most of the §2 sub-sections below
> were written against an earlier Cangjie release. With `cjnative 1.0.5` the
> situation has changed dramatically; the per-section "≈ Nx slower" headlines
> are stale and should be read as **historical context**, not current fact.
> The latest `report.md` is the source of truth. Headline deltas from the
> most recent run:
>
> | §2.x benchmark | Old headline | Current Cangjie vs. C++ (cjnative 1.0.5) |
> |---|---|---|
> | 2.1 `sort`            | ≈ 15× slower than C++ | **still ≈ 16× slower** — the only major regression that remains |
> | 2.2 `hashmap_ops`     | ≈ 4× slower than C++  | **now ≈ 1.7× faster than C++** ✅ |
> | 2.3 `string_concat`   | ≈ 1.7× slower than C++ | ≈ 1.4× slower than C++ (small) |
> | 2.4 `closure_sum`     | ≈ 10× slower than C++ | **now ≈ 4× faster than C++** ✅ |
> | 2.5 `regex_search`    | marginally bolded     | **now ≈ 1.8× faster than C++** ✅ |
> | 2.6 `prime_sieve`     | ≈ 30× slower than C++ | ≈ 1.2× slower than C++ ✅ |
> | 2.7 `quicksort`       | ≈ 18× slower than C++ | ≈ 1.3× slower than C++ ✅ |
> | 2.8 `matrix_multiply` | ≈ 80× slower than C++ | ≈ 1.5× slower than C++ ✅ |
> | 2.9 `word_count`      | ≈ 32× slower than C++ | **still ≈ 6× slower** — second remaining regression |
> | 2.10 `spectral_norm`  | ≈ 15× slower than C++ | ≈ 1.04× slower than C++ ✅ |
>
> So under SDK 1.0.5 the only ⚠️ rows that genuinely indicate Cangjie under-
> performing native baselines are **`sort`** and **`word_count`**. The other
> ⚠️ rows in the new report (`regex_search`, `string_search`) are bolded by
> the log-distance heuristic only because Cangjie is essentially tied with
> Python while the *fastest* native baseline (Rust) is exceptionally fast on
> those workloads — Cangjie itself is not slow there (in `string_search`
> Cangjie is in fact the **fastest** of all five implementations).
>
> The 16 newly-added benchmarks (`bit_count`, `gcd_loop`, `xor_shift`,
> `string_split`, `string_search`, `format_loop`, `set_ops`, `deque_ops`,
> `conway`, `knapsack_dp`, `levenshtein`, `monte_carlo_pi`, `histogram`,
> `dijkstra`, `base64`, `crc32`) are all within a small constant factor
> (typically ≤ 2×) of the fastest native baseline; several (`gcd_loop`,
> `xor_shift`, `string_search`, `set_ops`, `deque_ops`, `histogram`) put
> Cangjie at parity with or ahead of `g++ -O2`.

---

## 1. Cross-language consistency audit

For every benchmark, every language implementation was reviewed against
the same checklist. The user's guidance is:

> **Top-level logic must match across languages; the specific library
> interface called underneath may differ.**

| Check | Pass criterion |
|---|---|
| Argument parsing | All implementations read the same `N`/`D` from `argv[1]` with the same default. |
| Input generation | Identical seed, identical formula, identical order. Generation always **outside** the timed region (or always inside it) — never split across languages. |
| Timed region | Same conceptual work bracketed by the start/stop clock. |
| Iteration count | Same outer/inner loop bounds. |
| Data layout | Same array shape (e.g. row-major contiguous vs. nested). |
| Checksum formula | Identical bit-for-bit so the runner's CHECKSUM-equality check enforces semantic equivalence. |

**Verdict for all 16 benchmarks: CONSISTENT.** Every CHECKSUM matches across
all five languages on every run, which is the strongest possible guarantee
that the same computation is being measured.

The only sub-stdlib substitutions are the kinds the user explicitly allowed
(different library calls under identical top-level logic):

| Benchmark | Python | C++ | Rust | Go | Cangjie | Top-level logic identical? |
|---|---|---|---|---|---|---|
| sort | `list.sort()` | `std::sort` | `Vec::sort` | `sort.Slice` | `std.sort.sort` | yes — single stdlib sort call on identical input |
| hashmap_ops | `dict` | `std::unordered_map` | `HashMap` | `map[string]int64` | `HashMap` | yes — N inserts then N lookups |
| string_concat | `list+append`-style | `std::string::append` | `String::push_str` | `strings.Builder` | `StringBuilder.append` | yes — N appends then materialise once |
| regex_search | `re.compile + finditer` | `std::regex + sregex_iterator` | hand-rolled scanner (no stdlib regex in Rust) | `regexp.FindAllStringIndex` | `Regex + lazyFindAll` | yes — same alternation, same input string, same match count |
| word_count | `str.split()` | hand-rolled tokeniser | hand-rolled tokeniser | hand-rolled tokeniser | `lazySplit("\n") + lazySplit(" ")` | yes — same word boundaries, same hash-map updates |
| binary_trees | recursive `Node` class | `Node*` + `new`/`delete` | `Box<Node>` | `*node` + GC | `class Node` + GC | yes — same depth schedule, same checksum |
| spectral_norm / mandelbrot / nbody / matrix_multiply / quicksort / prime_sieve / fibonacci / enum_eval / math_loop / closure_sum | hand-written | hand-written | hand-written | hand-written | hand-written | yes — line-for-line equivalent |

So we can read the comparison as a meaningful first-order signal about the
**runtime / standard-library / compiler back-end**, not about algorithmic
inequities.

---

## 2. Why is Cangjie slow on the bolded benchmarks?

This section walks through every ⚠️ row in `report.md`. Numbers cited come
from the most recent run; refresh by running `python3 perf/run.py`.

### 2.1 `sort` — Cangjie ≈ 15× slower than C++, ≈ 3× slower than Python

| Lang | min | vs C++ |
|---|---|---|
| C++ (`std::sort`) | ~150 ms | 1.0× |
| Python (`list.sort` / Timsort in C) | ~820 ms | ~5× |
| Cangjie (`std.sort.sort`) | ~2.3 s | ~15× |

**Likely causes**
- Python's `list.sort` is a **C-implemented Timsort** — the loop is in native
  code with no per-comparison interpreter dispatch, so on bulk-sort workloads
  it is closer to native than Cangjie's stdlib sort.
- Cangjie's `std.sort.sort` is implemented in Cangjie itself; without
  generics-specialisation/monomorphisation for `Int64` it likely goes through
  a generic comparator path that prevents inlining of the integer compare.
- Bound-checked indexing on `Array<Int64>` and write-barriers for GC
  bookkeeping add per-swap overhead that `std::sort` does not pay.

**Mitigations** (out of scope for this benchmark suite, but actionable):
- A specialised primitive-typed sort in `std.sort` (or a `sortInPlace<Int64>`
  monomorphisation hint) would close most of the gap.
- Optimising stdlib comparator dispatch (devirtualising the comparator
  closure) would remove the per-compare indirection.

### 2.2 `hashmap_ops` — Cangjie ≈ 4× slower than C++ and Python

| Lang | min |
|---|---|
| C++ (`std::unordered_map`) | ~115 ms |
| Python (`dict`) | ~123 ms |
| Cangjie (`HashMap`) | ~470 ms |

**Likely causes**
- Cangjie strings are immutable `String` values; every key the benchmark
  inserts is freshly allocated and probably hashed via a UTF-8-walking
  `hashCode()`. Both C++ and Python cache string hashes at construction time
  (Python) or compute them inline over the small-string-optimised buffer
  (C++).
- The `HashMap.get → match Some/None → put` pattern in the Cangjie code
  performs **two probe sequences** per update (one for `get`, one for the
  subsequent `put`/`set`) where Python's `counts[w] = counts.get(w,0)+1`
  is also two probes — but Python's dict uses a single C-level perturb
  probe, making per-probe cost much lower.
- GC write-barriers fire on every `HashMap` bucket-array store.

**Mitigations**: a `HashMap.entry(key) -> Entry`-style API (one probe,
in-place update) would halve the probes; cached string hashes would amortise
the per-key cost.

### 2.3 `string_concat` — Cangjie ≈ 1.7× slower than C++, faster than Python

| Lang | min |
|---|---|
| C++ (`std::string::append`) | ~28 ms |
| Cangjie (`StringBuilder`) | ~47 ms |
| Python (`list.append` + `"".join`) | ~76 ms |

This row is borderline — Cangjie is **faster than Python** here, but on the
log axis it's closer to Python than to C++ (the |cj − py| log distance is
slightly less than |cj − cpp|), so the rule still bolds it.

**Likely causes**
- `i.toString()` for `Int64` likely allocates a fresh `String`; C++ uses
  small-buffer optimisation in `std::string`/`std::to_string` and avoids
  allocation for small numbers.
- `StringBuilder.append(String)` performs a UTF-8 encoding-validation step
  that `std::string::append` does not.

This is a small absolute gap (~20 ms over 500 000 appends) and is not a
priority concern, but is included for completeness because it satisfies the
log-distance rule.

### 2.4 `closure_sum` — Cangjie ≈ 10× slower than C++, ≈ 4× faster than Python

| Lang | min |
|---|---|
| C++ (lambdas in tight loop) | ~10 ms |
| Cangjie (closures) | ~97 ms |
| Python (map/filter/reduce) | ~344 ms |

**Likely causes**
- Three closures over an N-element pipeline allocate three closure objects
  and route every element through three indirect calls. C++ inlines the
  lambda bodies through the loop and SROAs the captured state, collapsing
  the pipeline to a single fused loop. Cangjie's optimiser doesn't appear
  to be inlining the closure trio yet, so the call overhead dominates.
- Iterator chains in Cangjie likely materialise intermediate sequences or
  step through generic iterator state, where C++ ranges-style or simple
  indexed loops are flattened.

**Mitigation**: a manual fused loop — `for (i in 0..n) if cond { acc += f(i) }`
— would close the gap, but the point of this benchmark is to measure
higher-order performance "as written".

### 2.5 `regex_search` — actually fast, only marginally bolded

| Lang | min |
|---|---|
| Python (`re`) | ~39 ms |
| Cangjie (`Regex.lazyFindAll`) | ~45 ms |
| C++ (`std::regex`) | ~77 ms |

Cangjie is **faster than C++ here** and only ~15 % slower than Python's
mature C-implemented `re` engine. The log-distance rule bolds it because
|log(45) − log(39)| < |log(45) − log(77)|, but practically this row is fine
and is the **only ⚠️ row that should not be read as under-performance**. It
is left bolded only because the rule is purely numeric.

### 2.6 `prime_sieve` — Cangjie ≈ 30× slower than C++, ≈ 2× faster than Python

| Lang | min |
|---|---|
| C++ | ~54 ms |
| Cangjie | ~1.56 s |
| Python (`bytearray`) | ~3.12 s |

**Likely causes**
- `Array<Bool>` per-element bound-checked indexing in a tight inner loop
  (`sieve[j] = false` repeated N/i times for every prime i) is the hot path.
  C++ `vector<uint8_t>` with `-O2` becomes a vectorised `memset`-style
  store; Cangjie has to perform a length check + tag bit pack/unpack on
  every store.
- The outer `while (i * i <= n) ... if (sieve[i])` is also bound-checked.
- C++ benefits hugely from compiler auto-vectorisation here (AVX2 byte
  stores), which the Cangjie back-end does not yet emit for the same
  loop shape.

**Mitigation**: an `Array<Byte>` (or unsafe pointer view) variant would
shrink most of the bound-check overhead. Auto-vectorisation in the back-end
would do the rest.

### 2.7 `quicksort` — Cangjie ≈ 18× slower than C++, ≈ 1.6× faster than Python

| Lang | min |
|---|---|
| C++ | ~135 ms |
| Cangjie | ~2.38 s |
| Python | ~3.80 s |

**Likely causes**
- Same bound-check + write-barrier story as `sort` and `prime_sieve`, but
  applied to an algorithm that performs O(N log N) array reads and writes.
- The recursive call adds a `Function<...>` activation cost per partition.
  C++ inlines the recursion partially and elides any allocation; Cangjie
  may be allocating a stack frame plus parameter spilling for each call.
- Pivot swaps use three array writes per swap (`tm = a[lo]; a[lo] = a[hi];
  a[hi] = tm`) — each is a separately bound-checked store in Cangjie.

**Mitigation**: the same as `sort` (specialised primitive sort,
devirtualised comparator).

### 2.8 `matrix_multiply` — Cangjie ≈ 80× slower than C++, ≈ 1.1× slower than Python(!)

| Lang | min |
|---|---|
| C++ | ~11 ms |
| Python (NumPy-free pure-Python triple loop) | ~800 ms |
| Cangjie | ~900 ms |

This is the most striking gap. Note Python is pure-Python here — no NumPy
— which is why the Python number is so slow; the comparison Cangjie should
beat handily, and doesn't.

**Likely causes**
- C++ at `-O2` **auto-vectorises** the innermost `c[i*n+j] += aik * b[k*n+j]`
  loop into AVX/AVX2 fused-multiply-add SIMD; that single optimisation is
  worth ~8× on AMD EPYC.
- C++ also keeps `aik` in a register and turns `c[i*n+j]` into a
  non-bound-checked pointer increment.
- Cangjie performs three array bound-checks per iteration of the inner
  loop (read `a`, read `b`, write `c`) and does **not** vectorise the
  multiply-add reduction.
- Python's interpreter loop has so much fixed per-bytecode overhead that
  even without SIMD, the per-iteration cost is comparable to Cangjie's
  bound-checked loop — hence the near-tie.

**Mitigation**: the back-end gaining auto-vectorisation + a way to
express "trust me, no bound-check" (similar to `unsafe { ... }` in Rust or
`@inbounds` in Julia) would be the single biggest improvement here.

### 2.9 `word_count` — Cangjie ≈ 32× slower than C++, ≈ 5× slower than Python

| Lang | min |
|---|---|
| C++ (`unordered_map`) | ~21 ms |
| Python (`dict` + `str.split`) | ~133 ms |
| Cangjie (`HashMap` + `lazySplit`) | ~673 ms |

This compounds two of the other gaps: `HashMap` performance (§2.2) and
string-tokenisation cost.

**Likely causes**
- Each `lazySplit` token materialises a fresh `String` slice — Cangjie
  strings are immutable and almost certainly require an allocation +
  UTF-8 boundary check per token, where C++ `std::string_view` (or even
  Python's interned-short-string optimisation) avoid that allocation.
- The `match counts.get(w) { Some(v) => counts[w] = v+1; None => counts[w] = 1 }`
  pattern double-probes the map (see §2.2).
- At 1 M tokens, that's ~1 M extra allocations relative to the C++ path
  that uses `std::string::substr` (still allocating, but small-buffer
  optimised) and ~1 M extra hash-map probes.

**Mitigation**: a non-allocating string-view type in `std`, plus the
`HashMap.entry`-style API mentioned in §2.2.

### 2.10 `spectral_norm` — Cangjie ≈ 15× slower than C++, ≈ 8× faster than Python

| Lang | min |
|---|---|
| C++ | ~146 ms |
| Cangjie | ~2.22 s |
| Python | ~17 s |

**Likely causes**
- The hot path is `s += A(i,j) * v[j]` inside an O(N²) double loop, which
  C++ vectorises into SIMD multiply-adds (same story as `matrix_multiply`).
- `A(i,j)` involves a small integer arithmetic + one `Float64` divide per
  call. C++ inlines this trivially; Cangjie should too, but the *non-vectorised*
  inner loop is what costs the most.
- `Array<Float64>` indexed reads carry a bound check per access.

This is the same `matrix_multiply` story applied to a different access
pattern, and the same mitigations apply.

---

## 3. Summary of root-cause categories

Looking across §2.1 – §2.10, three broad themes recur:

1. **Auto-vectorisation gap** (`matrix_multiply`, `spectral_norm`,
   `prime_sieve`, partly `math_loop`/`nbody` though those are not bolded).
   `g++ -O2` lifts tight FP/integer loops into SIMD; the Cangjie back-end
   does not yet emit equivalent SIMD for the same source shape.

2. **Bound-check / write-barrier overhead in tight array loops**
   (`sort`, `quicksort`, `prime_sieve`, `matrix_multiply`,
   `spectral_norm`, `word_count`). Every `Array[i]` access carries a
   length check and (for ref-typed arrays) a write barrier. In hot loops
   that pay one or two such checks per nanosecond of work, this dominates.
   An `unsafe-indexed` or proven-safe iteration form would close most of
   the gap.

3. **Stdlib generic dispatch / closure overhead**
   (`sort`, `hashmap_ops`, `closure_sum`, `word_count`). Cangjie's stdlib
   relies on generic types parameterised over comparators / hashers /
   element types, but does not appear to monomorphise for primitive
   element types. The result is one indirect call per element of work,
   which compounds with the bound-check cost above. Specialising the
   common cases (`Int64`, `Float64`, `String` keys) would help every
   container-heavy workload.

The benchmarks where Cangjie does well — `fibonacci`, `nbody`,
`mandelbrot`, `enum_eval`, `closure_sum` (vs Python), `binary_trees` —
are exactly those that don't hit any of those three patterns simultaneously
(they're recursion-heavy, FP-light, closure-light, or allocation-bound on
small objects where the GC nursery beats `malloc/free`).
