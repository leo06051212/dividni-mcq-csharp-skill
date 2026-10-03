# Dividni MCQ C# skill

A Codex skill for writing and reviewing C# question generators for [Dividni's MCQ Exam Generator](https://dividni.online/McqExamGen/). It works with MCQs for any course. Source material can be text, a PDF, a screenshot, a diagram, existing C#, or an answer key.

The skill checks each answer option before coding, follows the target exam's C# conventions, and produces generators that can be reviewed before upload. It covers single questions, diagrams, and groups of questions sharing one stem. It does not cover non-MCQ question types.

## Install

Clone this repository into your Codex skills directory, using the skill name as the folder name:

```bash
git clone https://github.com/leo06051212/dividni-mcq-csharp-skill.git ~/.codex/skills/generating-dividni-mcq-csharp
```

On Windows PowerShell:

```powershell
git clone https://github.com/leo06051212/dividni-mcq-csharp-skill.git (Join-Path $env:USERPROFILE '.codex\skills\generating-dividni-mcq-csharp')
```

If you use a custom `CODEX_HOME`, put the repository in its `skills/generating-dividni-mcq-csharp` directory instead.

## Use

In Codex, invoke `$generating-dividni-mcq-csharp` and provide the questions, answer key, relevant figures, and any exam-specific conventions. State whether you want fixed questions or generated variants. If a shared stem covers several MCQs, identify the children and their order.

For the common five-option, single-correct form, the skill uses `TruthQuestion`. It uses `XyzQuestion` for independent statements only when the target Dividni setup supports it. One `InstructionalItem` can hold a shared stem or diagram; its child MCQs remain separate questions in the exam-wide numbering sequence. Check the rendered preview for displayed numbers and order.

For diagrams in the online generator, the skill can embed a compact SVG as a base64 `data:image/svg+xml` URI in the generated C# HTML. A synthetic SVG diagram rendered successfully in an online PDF preview on 2026-10-03. A same-directory relative image path produced a missing image in that test. Keep the editable SVG source with your working materials and inspect every real generated PDF; the observation does not establish support for all SVG features or future service versions.

## Check a generated file

From this repository's root, run the bundled Python 3 static checker:

```sh
python scripts/validate_dividni_mcq.py path/to/question.cs --mode standalone
python scripts/validate_dividni_mcq.py path/to/shared-group.cs --mode existing
```

Use `standalone` for a file containing one MCQ and `existing` for a shared-stem group or combined file. The checker reports structural issues such as missing question factories, duplicate literal IDs within a file, and invalid base64 image data. It does **not** compile C#, verify the correct answer, render the PDF, or confirm website compatibility. Review answer semantics manually and compile or preview in the actual Dividni environment when available.

## Upload workflow

1. Review the generated `.cs` files and verify IDs are distinct across the full question set.
2. Make a flat Questions ZIP containing the generated `.cs` files. An SVG embedded as a data URI needs no separate ZIP asset. Keep editable image sources outside the upload ZIP.
3. Upload the ZIP to the [MCQ Exam Generator](https://dividni.online/McqExamGen/), then check the preview's answers, diagrams, page layout, and global question numbering before generating the final PDF. Recheck the website's current upload requirements, including its size limit.

## Repository contents

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Codex workflow and delivery rules |
| [`references/dividni-authoring-reference.md`](references/dividni-authoring-reference.md) | C# forms, shared stems, and image guidance |
| [`references/mcq-semantic-review.md`](references/mcq-semantic-review.md) | Answer and distractor review checklist |
| [`scripts/validate_dividni_mcq.py`](scripts/validate_dividni_mcq.py) | Conservative static checker |

## License

MIT. See [`LICENSE`](LICENSE).
