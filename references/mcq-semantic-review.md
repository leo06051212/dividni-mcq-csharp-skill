# MCQ semantic review

Use this when an answer, diagram, program trace, or distractor could be interpreted in more than one way. The user's supplied course definitions and answer key are evidence to examine, not a substitute for checking the options.

For each option, write the reasoning that makes it correct or incorrect before assigning it to `AddCorrects` or `AddIncorrects`. Check the stem's polarity (`TRUE`, `FALSE`, `NOT`, `EXCEPT`), units, rounding, boundaries, unstated assumptions, and whether two options are equivalent. For code questions, check language/version assumptions, evaluation order, undefined behavior, alternate valid programs or commands, and renaming of temporary registers. For diagrams, read labels and edge directions from the actual asset; do not reconstruct an unreadable graph from a key.

For a shared stem, check that every child can be answered from the same displayed material and that no child silently requires a different diagram state. If the diagram is generated, verify that the picture, stem, key, and distractors all derive from the same state. For parameterised questions, sample enough seeds to expose collisions and edge cases; a unique string is not necessarily a unique meaning.

Stop before finalising if there is no correct option, more than one unintended correct option, a key conflict, or a missing convention that changes the answer. State the smallest concrete issue and ask one focused question. If the user explicitly requests a review draft, mark the affected question `// REVIEW REQUIRED` and explain that it is not exam-ready.
