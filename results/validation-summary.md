# Final deterministic validation summary

All seven suites and all thirteen unit tests passed in the final retained campaign.
The checks are finite implementation evidence, not a representative workload study,
a formal proof assistant, or independent peer review.

## Reconciled counts

| Suite | Exact retained obligation |
|---|---|
| Relations | 1,056 graph views; 2,048 independent replay rows; 526,336 environment/repair-extension edges |
| Complete-state padding | 510 graphs; 4,080 repaired-environment rows |
| Translated circuits | 128 graphs; 40,960 independent replay rows; seed 1729 |
| General DAGs | 256 observer-specific graph views; 32,768 independent replay rows; seed 65537 |
| Adaptive/uniform gaps | 8 tight sizes; shared-input composition has joint A=1, separate maxima sum=2, U=2 |
| Baselines | 12 tight invalidation sizes; 128 random DAGs; 2,072 soundness rows; 1,024 refinement rows; seed 104729 |
| Negative controls | 24/24 intended faults detected |

The independent semantic comparison total is
2,048 + 40,960 + 32,768 = **75,776**. Padding's 4,080 rows are checked
against the closed-form mismatch characterization and are not double-counted as
independent bit-evaluator/replay comparisons.

## Baseline distribution

For the 128 fixed-seed random complete-state DAGs, descendant invalidation was
strictly larger than the semantic optimum in 53 cases and equal in 75 cases. Three cases had positive syntactic cost but zero semantic optimum; they are excluded from multiplicative-ratio summaries. Among the 120 positive-optimum cases, the mean ratio was 1.299 and the maximum was 4. Mean syntactic and semantic costs were 2.594 and 2.086.

The exact (syntactic cost, semantic optimum) frequency table is:

| Pair | Count |
|---|---:|
| (0, 0) | 5 |
| (1, 1) | 20 |
| (2, 0) | 2 |
| (2, 1) | 10 |
| (2, 2) | 17 |
| (3, 0) | 1 |
| (3, 1) | 3 |
| (3, 2) | 17 |
| (3, 3) | 21 |
| (4, 1) | 1 |
| (4, 2) | 3 |
| (4, 3) | 16 |
| (4, 4) | 12 |

## Resource observations

The seven suite processes used 5.275 recorded CPU seconds and 5.290
recorded wall seconds in aggregate; maximum reported resident set size was
94,508 KiB. These measurements describe this run only and are not equality
targets for reproduction. Each child used one CPU with the documented virtual
address-space, CPU-time, wall-time, and row-admission guards.

## Controls and interpretation

The 24 negative controls cover graph schema, certificate canonicality and domain
coverage, trace/cache/output mutation, non-prefix repair, unsupported effects,
cycle/topology violations, the escape-chain off-by-one error, adaptive/uniform
quantifier swapping, and an unsafe union-of-adaptive-masks shortcut. They are
owned benign toy mutations, not offensive testing.

A passing campaign shows that the delivered implementation satisfies the listed
finite obligations under the documented interpreter. It does not show browser
correctness, representative performance, or the truth of the unbounded prose
proofs by itself.
