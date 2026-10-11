# Lenses and red-team

The old council ran five advisors as five sub-agents. With the same model and the same facts they mostly agreed, at five times the cost. The perspectives were useful; the separate agents weren't. So the main session applies the five lenses itself, as a checklist, after research and before writing the report. It costs no sub-agents.

## The five-lens checklist

Answer each in a few lines of working notes. Keep anything that changes the decision, the map, the pre-mortem or the plan; drop the rest.

1. **Risk.** What is most likely to go wrong, and which failure would be fatal rather than merely costly? Feed the pre-mortem.
2. **First principles.** What is the user actually trying to achieve? Is the question framed around the wrong choice? If yes, that's a candidate for "the option you didn't list".
3. **Upside.** If this goes better than expected, what becomes possible? Is there an option with more upside that nobody named? Each upside needs a mechanism, not hype.
4. **Outsider.** What would someone with no context find confusing, risky or obviously missing? What does the user take for granted?
5. **Execution.** What happens first, what is the cheapest test, what blocks it, and in what order? Feed the plan and the decision map's tests.

Then run three checks, still in your own notes (no sub-agent):

### Change test (technical decisions only)

For architecture, infrastructure, data or codebase decisions, test the recommended design against the future instead of declaring it "scalable".

1. List 4–5 plausible future changes **specific to this product**: load growth (10× and 100× of the stated numbers), a new feature or entity type that stresses the design, a new deployment shape (second region, dedicated server, on-prem), team growth, a new compliance or audit need. Generic changes ("traffic grows") don't count.
2. Rate each against the recommended design: **Absorbs** (no structural change), **Extends** (additive work only), or **Breaks** (redesign needed: say what and why).
3. Add **breaking points with numbers** where a documented limit exists (from research or the files): the limit, today's figure, and the warning sign to watch.
4. Give a verdict: **Foundation** or **Quick fix**. If two or more likely changes break it, say so plainly and either name the design that would absorb them, or say the user is choosing a short-term fix and when it runs out.

Skip it for non-technical decisions.

### Single-answer floor

Before writing the report, write in your notes the answer a strong single response would give without research: the obvious tools or products, standard precautions, practical first steps, common mistakes. Then compare it with your draft. Anything useful the draft lacks goes into the plan, risks or pre-mortem. In testing, single answers kept winning small practical points (insurance before signing, ready-made libraries, off-the-shelf tools) that the research-focused report dropped. The report should be a superset: everything a good single answer says, plus what research found.

### Numbers over adjectives

Calculate the 2–4 figures the decision turns on instead of describing them: the cash needed on day one, the payment on one income, each option's cost floor, capacity headroom, the timeline in engineer-weeks. Show the inputs, and label estimates as estimates. In testing, one of the most valuable findings was plain arithmetic (a home purchase needing more cash than the family had).

Then check your draft against the research: does any finding contradict it? Does any lens point to something the research didn't cover? If so, say it plainly as an open question rather than guessing.

## Red-team (high stakes only)

When `research.md` calls for it, the second sub-agent attacks your draft instead of researching. It runs after the draft exists.

```
You are the red-team for a decision report. Below are the decision, the
research findings, and a draft recommendation. Your only job is to find
what is wrong with the draft or what it missed. If you find nothing that
would change the recommendation or the plan, say so plainly. Do not
invent problems or facts.

DECISION AND CONTEXT:
---
[decision, user context, user's answers]
---
RESEARCH FINDINGS:
---
[R1..Rn]
---
DRAFT:
---
[draft]
---

Look for: the plausible future change that breaks this design; a finding the draft ignores or contradicts; a serious risk it
doesn't answer; an option it didn't weigh that could beat it; an
assumption it depends on without support; a plan step that is unsafe or
wouldn't work; a failure mode missing from the pre-mortem.

Output, under 250 words:
VERDICT_HOLDS: yes | no | partly
FINDINGS:
- [MATERIAL | MINOR] <finding, and why it matters>
IF_NOT_HOLDS: <what should be recommended instead, in two sentences>
```

Fold every correct finding into the report. A material finding changes the verdict, the map, the pre-mortem or the plan; note in the audit which you accepted and which you rejected, with a reason.
