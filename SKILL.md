---
name: decision-check
description: "Turn a real decision, first of all a coding decision in your codebase (feature design, refactor, migration, where code should live, which library), but also tools, vendors, build vs buy and money or life decisions, into a decision report a single answer doesn't give: what's actually in your code, checked by an independent reviewer; the facts that flip it, from primary sources; the questions only the user can answer, asked first; a decision map of what each option bets on; the option nobody listed; and a pre-mortem with warning signs. Simple questions get a direct answer at no extra cost; a full report costs about 3x a single answer. MANDATORY TRIGGERS: 'decision check this', 'check this decision', 'pressure-test this', 'stress-test this', 'council this'. STRONG TRIGGERS (with a real decision or tradeoff): 'should I X or Y', 'which option', 'is this the right move', 'I can't decide', 'I'm torn between'. Do NOT trigger on factual lookups, creation tasks, or casual questions with no real tradeoff."
---

# Decision Check

A single strong answer already gets most decisions right. Testing showed that a council of advisors debating the same question with the same facts mostly produces the same answer at several times the cost. So this skill doesn't try to produce a "better verdict". It produces what a single answer structurally leaves out:

1. **What's actually in your code.** For coding decisions it maps the codebase, traces who owns the state and where code ships, counts from real searches, and has an independent code reviewer re-check every claim before you see the report.
2. **Facts it didn't look up.** A researcher checks current versions, prices, rules and known issues from primary sources.
3. **Facts only the user knows.** The ones that would flip the decision are asked up front instead of guessed.
4. **The shape of the decision.** What each option bets on, and the cheapest test for each bet.
5. **The option nobody listed**, if one survives the research.
6. **How it fails, and whether it lasts.** A pre-mortem with warning signs, and a test against likely future changes.

**Budget rule and bar:** a simple question uses no sub-agents (~1×). A decision report uses one sub-agent (a code reviewer for coding decisions, a researcher otherwise), two on high stakes, and should cost about 3× a single answer (up to about 4× on high stakes). For that cost, it must contain decision-changing information a single answer wouldn't have: at least one finding that could prevent a costly mistake or flip the choice, or several that change the plan or the checks. If research doesn't clear that bar, say so plainly and keep the report short; never pad it to look worth the cost.

## Workflow

**Read each reference file with the Read tool when you reach its stage, every time. Do not work from memory or from this summary: the reference files hold the prompts, checks and template that make the report worth its cost.** The required reads are marked **Read:** below. "Sub-agent" means any independent model call your environment provides; if there are none, see Failure modes.

1. **Scan context.** If the decision is about a codebase (a feature, refactor, migration, placement, library or architecture choice), it is a **coding decision**: **Read:** `references/code.md` now and apply its gates G0–G6 throughout (big-repo search method, the repo's own rules, precedent, git history, ownership tracing, placement, conventions, security and data integrity, counted blast radius, claims ledger, rollout). Most decisions in Claude Code are coding decisions; for them the codebase is the main evidence, not the web. Otherwise read only files that bear on the decision. Don't read past reports in `decision-reports/` unless asked; if asked, treat them as hypotheses.
2. **Gate.** **Read:** `references/triage.md`. Decide whether this is a real decision with stakes or a question with a clear answer. Clear answer → answer directly and offer a report ("Say 'full report' to dig deeper"). Stop. See `references/triage.md`.
3. **Find the deciders.** Write the 3–5 facts or assumptions that would flip the decision if they turned out differently. Sort each one: **known well** (answer from knowledge, no search), **fresh or specific** (could have changed or memory could get the detail wrong: research it), **in the files** (workspace), or **only the user knows**. See `references/triage.md`.
4. **Ask first.** If any "only the user knows" decider would flip the answer, ask up to three of them in one short message before researching. If the user says "just decide", assume the most likely answer, say so, and show both branches in the report. See `references/triage.md`.
5. **Research.** **Read:** `references/research.md`. **Coding decisions:** do the codebase gates yourself (G0–G5 in `code.md`), then use the sub-agent as a **code reviewer** on your draft (prompt in `code.md`); add a web researcher only when a library, framework or version fact could flip the choice. **Run every sub-agent in the foreground and wait for its result; never write the report before it returns.** Other decisions: give each researcher its "Researcher prompt" filled in, word for word, including the 8-call limit. Check the "in the files" deciders yourself. Give only the **fresh or specific** deciders to researchers: **one researcher by default** (at most 5 questions, ranked by how much each could flip the decision), **two in parallel only on high stakes**. Each has a hard limit of 8 tool calls. On high stakes with little left to look up, the second sub-agent can be a red-team instead (`references/lenses.md`). See `references/research.md`.
6. **Apply the lenses and checks yourself.** **Read:** `references/lenses.md`. Run the five-lens checklist, then the three checks: the **change test** for technical decisions (which plausible future changes the design absorbs, extends or breaks, with breaking points), the **single-answer floor** (nothing a strong quick answer would say is missing), and **numbers over adjectives** (calculate the figures the decision turns on). All in your own notes, at no extra sub-agent cost. See `references/lenses.md`.
7. **Write the report.** **Read:** `references/report.md`, and follow its template exactly. The chat report must use these headings, omitting only those with nothing decision-changing to say:
   - `## Verdict:` with **Confidence**
   - `### What we found that changes the picture` (sourced findings; for coding decisions, lead with what was found in the code, each claim with its file:line)
   - `### Blast radius` (coding decisions: files and systems touched, counts from searches)
   - `### What we assumed about you`
   - `### Decision map` (table: option, bets on, cheapest test)
   - `### The option you didn't list`
   - `### Will it last?` (technical decisions: the change-test table and foundation-or-quick-fix line)
   - `### Pre-mortem` (failure, warning sign, when to check)
   - `### Rollout` (coding decisions: ordered steps that keep things working, sizes, timebox, exit criterion)
   - `### Next step`
   - the footer line

   Then save the full decision record to `decision-reports/` in the "Saved report" format: the complete chat report text pasted in (never a placeholder), plus the plan, every finding with its source, and the audit. Say where in one line.

## Cost discipline

- The cost is the number of sub-agents. Direct answer: 0. Decision report: 1 by default, 2 on high stakes. Nothing more, unless the user explicitly asks ("deep research").
- Asking the user costs nothing and often changes the answer more than research does. Ask before you spend.
- Researchers return short, sourced findings, not essays. Their prompts set a word limit.
- Pass long material as files where your environment allows it.

## Failure modes

- **A sub-agent can't be started** (for example the Agent tool is disabled): do the research yourself, and do the code-review step as a separate pass that re-checks every claim in the claims ledger against the code. Say so in the footer.
- **No search or file tools:** say which deciders couldn't be checked, mark them Unknown, and keep confidence at Medium or lower. Never present an unchecked claim as checked.
- **Research found nothing new:** say so in the report's first section and keep the report short. That's an honest outcome, not a failure.
- **A sub-agent returns something off-task:** re-run it once; if it fails again, continue without it and say so in the footer.
- **The user answers only some questions:** proceed, and treat the rest as assumptions shown with both branches.
