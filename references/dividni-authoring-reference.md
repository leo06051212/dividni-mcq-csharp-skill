# Dividni MCQ authoring forms

## Evidence and limits

In a validated flat ZIP of 18 `.cs` files, two files each contained one shared instruction and several MCQs. Its generated PDF showed that shared instructions do not consume displayed question numbers. Numbering started at 1 for that partial upload even though method names referred to later questions, so never derive visible numbering from a method name or `q.Id`.

The validated set has `TruthQuestion` examples only: each question has one `AddCorrects` value and four `AddIncorrects` values. It has no image examples. A legacy sample contains `XyzQuestion` and HTML `<img>` examples, but does not establish that the current online service accepts their assets.

The [official Dividni tutorial](https://dividni.com/tutorial/) documents `.cs` question generators, multiple source files, HTML `<img>`, and shared instructions. The [online MCQ Exam Generator](https://dividni.online/McqExamGen/) currently asks for a Questions ZIP, offers a preview with question ordering, and advertises a 5 MB upload limit. Recheck the site when preparing a real upload.

## Observed five-option form

The validated files use `namespace Utilities.Courses` and `public partial class QHelper : IQHelper`. A representative factory has this shape:

```csharp
using System;

namespace Utilities.Courses
{
    public partial class QHelper : IQHelper
    {
        public static QuestionBase RectangleAreaQ(Random random, bool isProof)
        {
            var q = new TruthQuestion(random, isProof);
            q.Id = "RectangleArea";
            q.Marks = 1;
            q.Stem = "<p>A rectangle is 3 cm by 4 cm. What is its area?</p>";
            q.AddCorrects("12 cm<sup>2</sup>");
            q.AddIncorrects("7 cm<sup>2</sup>", "14 cm<sup>2</sup>",
                            "24 cm<sup>2</sup>", "1 cm<sup>2</sup>");
            return q;
        }
    }
}
```

This is an authoring pattern, not a compilation result from the current host. Preserve the target project's namespace and style when editing an existing paper. Do not put fixed A–E labels in option strings; Dividni may reorder options.

## Shared stem and global numbering

In validated shared-stem examples, one factory returns `InstructionalItem`: it constructs `new InstructionalItem(random, isProof)`, assigns `p.Instruction`, then returns `p`. Separate `QuestionBase` factories follow. Keep the instruction before its children in the uploaded order. It has no separate marks or displayed question number. Check the preview for the intended whole-paper sequence, because the upload may be a partial paper and the UI can reorder questions.

## Images

Use HTML `<img>` in `q.Stem` for a single question or `p.Instruction` for a shared diagram. On 2026-10-03, an online test with `<img src='./ResourceAllocationGraph.svg'>` and a flat ZIP containing both `.cs` and SVG generated HTML that preserved the relative `src`, but the resolved image URL returned 404 and the PDF showed a broken-image icon. Changing the spelling of the relative path is not a useful next step for that service behavior.

A second test used Dividni's publicly hosted SVG URL and the generated PDF displayed it. A third test embedded the same synthetic RAG SVG in the C# HTML as `<img src='data:image/svg+xml;base64,...' style='width: 12cm;' />`; the online PDF displayed the complete diagram. For a compact original diagram, base64-encode the SVG bytes without line breaks, insert the resulting data URI into the C# string, and keep the `.svg` source as a separate editable deliverable. The Questions ZIP then needs only the `.cs` file. Inspect the actual PDF after generation; this test does not establish support for every SVG feature, raster data URI, or future service version. The official [Dividni sample ZIP](https://dividni.com/tutorial/samples.zip) also uses a public HTTPS SVG URL, but a public URL is unsuitable for confidential exam artwork.
