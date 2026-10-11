# Report

The report is ordered by what a single answer doesn't give. The verdict is short; the value is in the sections after it. Every section must earn its place: omit any section that has nothing decision-changing to say, and never pad.

## Chat report

400–700 words. Use this template; omit empty sections.

```markdown
## Verdict: <the decision in one plain sentence, 25 words at most>

**Confidence:** <High | Medium | Low>, <one short reason>

<Two sentences: why this option, for this user.>

### What we found that changes the picture
- <A new, sourced fact and what it means for the decision. Lead with the one that matters most.>
- <...>
<If research found nothing that changes the picture, say so in one line. Otherwise no summary line: the findings speak for themselves.>

### What we assumed about you
- <Assumption, and what changes if it's wrong.> (Omit if the user answered everything that mattered.)

### Decision map
| Option | Bets on | Cheapest test |
|---|---|---|
| <option in plain words> | <the assumption that must hold for it to win> | <how to check it, ideally within a week> |

### The option you didn't list
<Only if one survived research and the lenses: what it is, why it might beat the listed options, and what it bets on.>

### Will it last? (technical decisions only)
| Future change | Verdict | Why / breaking point |
|---|---|---|
| <change specific to this product> | Absorbs / Extends / Breaks | <reason; the documented limit and warning sign if one exists> |

**Foundation or quick fix:** <one line: which, and if a quick fix, when it runs out and what replaces it>

### Pre-mortem
- **<Failure story, one line>** · Warning sign: <what you'd see first> · Check: <when>
- <two or three in total; the most likely and the most damaging>

### Next step
<One concrete action this week.>

---
<sub>Report: <direct | 1 researcher | 2 researchers | researcher + red-team>; <N> questions asked; <M> new findings</sub>
```

## Verdict types and confidence

The verdict is one of:

- **Recommendation:** the evidence supports one option; remaining uncertainty doesn't change the choice.
- **Conditional:** choose X if Y holds, otherwise Z. Y must be something the user can check cheaply, and the decision map says how. Never make Y the user's own goals: ask instead.
- **Not enough to decide:** name the missing information and the action that gets it. Still say which way it leans.

Confidence, one word plus a reason:

- **High:** the choice rests on Confirmed findings or facts the user stated, and nothing found points the other way.
- **Medium:** sound reasoning, but at least one decider is unverified.
- **Low:** a close call, or mostly assumptions. Still make the call.

Caps: if no Confirmed finding backs the deciding claim, at most Medium. "Industry practice" or "well known" without a source is an assumption.

## Rules

- Lead with the answer. Plain language. Name options by what they are, never "Option A".
- Explain a technical term the first time it appears, in a few plain words.
- Say how you know: "AWS's pricing page says..." rather than citing IDs in the chat report.
- No mention of the machinery (researchers, lenses, gates) in the chat report except the footer.
- Never present an unchecked claim as checked. Never invent a number; label estimates as estimates and show the inputs.
- Specific to this user. No generic advice.
- Put the key figures in numbers, with their inputs (see "Numbers over adjectives" in `lenses.md`).

## Saved report

After showing the chat report, save `decision-reports/YYYY-MM-DD-<short-slug>.md` (add `-2` if the name exists) in the working directory, creating the folder if needed:

```markdown
# <Short title of the decision>

**Date:** <YYYY-MM-DD> · **Verdict:** <Recommendation | Conditional | Not enough to decide> · **Confidence:** <High | Medium | Low>

## Question
<The decision and the context that matters, including the user's answers to questions. Leave out private details not needed to understand it.>

<The full text of the chat report, from "## Verdict" through "Next step", pasted in, without the footer. Never write a placeholder or a pointer such as "see chat report": the saved file is read on its own, months later, by people who never saw the chat.>

## Plan
1. <3-8 concrete steps in order; for a Conditional verdict, start with the test>

## Findings and sources
- R1: <finding> (<Confirmed | Partial | Conflicting | Not found>) — <source, publisher, date>
- <every finding, including ones that didn't change the decision>

## Audit
<Gate score; deciders and how each was handled (asked, researched, checked in files, assumed); red-team findings accepted or rejected, with reasons; anything skipped and why.>

---
<the footer line>
```

Tell the user where it was saved in one line. If the user said not to save files, or the workspace is read-only, skip it and say so.
