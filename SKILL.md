---
name: generating-dividni-mcq-csharp
description: Use when creating, converting, or reviewing Dividni C# generators for multiple-choice exam questions from text, PDFs, screenshots, diagrams, or answer keys, including shared stems, figures, and upload ZIPs for any course. Excludes non-MCQ questions.
---

# Generate Dividni MCQ C#

Turn human-authored MCQs into reviewable Dividni question generators. The supplied question, answer key, and course conventions are the assessment source; independently check every option before coding. Never infer a course-specific convention from an old exam.

## Workflow

1. Read the complete source, including diagrams, answer key, existing code, and any whole-paper numbering or style rules. Record the stem, options, intended answer, marks, assets, assumptions, and whether variants are requested. If marks are omitted, use `1` and disclose the assumption.
2. Solve and classify each option independently. Check negation, units, boundary cases, equivalent expressions or programs, and alternate valid answers. Read [MCQ semantic review](references/mcq-semantic-review.md) when the answer is subtle.
3. Resolve a material defect from supplied evidence. If the key conflicts with the question, the diagram is unreadable, or the correct set is ambiguous, ask one focused question before producing a final generator. Create a `// REVIEW REQUIRED` draft only if the user requests one.
4. Follow the target exam's C# convention. For five-option, single-correct MCQs, use `TruthQuestion` with one correct and four incorrect options, as in the approved examples. Use `XyzQuestion` for three independent statements only when the target Dividni setup supports it. Read [Dividni authoring forms](references/dividni-authoring-reference.md) before writing code.
5. For several MCQs sharing a stem or diagram, place one unnumbered `InstructionalItem` immediately before their question factories. Each child remains a separate MCQ in the exam-wide sequence. Do not add local numbering such as 1–3 or 11a–11c. The source method name and `q.Id` are identifiers; verify displayed numbers from the generated preview.
6. Keep textual code as escaped HTML text, not a screenshot. For a genuine diagram, deliver its editable source image. For the online generator, encode a compact SVG as a base64 `data:image/svg+xml` URI inside an HTML `<img>` in `q.Stem` or the shared `InstructionalItem.Instruction`; see the tested pattern in [Dividni authoring forms](references/dividni-authoring-reference.md). Inspect the generated PDF for the diagram, labels, scale, and pagination. A same-directory relative image path failed in the online preview during testing; recheck if the service changes.
7. Preserve a fixed question unless variants are requested. For variants, derive the answer and distractors from one generated state, reject collisions, and inspect multiple seeds for comparable difficulty.

## Delivery and verification

Deliver `.cs` files plus editable image sources. A shared-stem group may occupy one `.cs` file; standalone questions normally use one file each. Check that question IDs are distinct across the full set. If preparing for [MCQ Exam Generator](https://dividni.online/McqExamGen/), prepare a flat Questions ZIP of the `.cs` files; an inline image needs no separate ZIP asset. Keep the upload under the page's stated 5 MB limit. The user controls the final upload and question order.

Run the bundled `scripts/validate_dividni_mcq.py` using its path relative to this `SKILL.md`, with `<file.cs> --mode standalone` for a single-question file or `--mode existing` for a shared group or combined file. Compile or preview in the actual Dividni environment when available, inspect images, page layout, and exam-wide numbering, and manually confirm the answer classification. The script cannot establish C# compilation, subject correctness, or website compatibility. Report what was verified and what remains unverified; do not paste full source into chat unless asked.
