# Decision Check

**A Claude Code skill for coding decisions: it reads your codebase, checks the facts, and tells you what will break before you build.**

https://github.com/user-attachments/assets/a21c22df-fd50-4425-9b8c-0b6d5719424e

> Inspired by [Andrej Karpathy's LLM Council](https://github.com/karpathy/llm-council).

Ask Claude "how should we build this?" and you get a sensible plan. What it often misses is in your own code: who actually owns the state, which folder gets copied into every user install, the event nothing calls, the function a Blueprint depends on. Decision Check traces those things, has an independent reviewer re-check the code, and gives you a decision report with a rollout plan.

---

## What it catches

Real coding decisions on three real codebases: a UE5 C++ game (~10,500 lines), a Python + TypeScript tool (~35,000 lines) and [Outline](https://github.com/outline/outline), an open-source team wiki (~358,000 lines). Each was answered by Claude Code on its own and with this skill.

| The decision | Claude Code on its own | With Decision Check |
|---|---|---|
| **Add race replays and ghost racing** to a UE5 multiplayer drone game | Record laps starting from the `OnCourseStarted` event, save best laps in the existing save file | **Nothing in the code calls `StartCourse()`**, so that event may never fire: start from the course timer instead. **The save file stores a plaintext password** (`UserSaveGame.h:22`), so keep recordings in their own slot. |
| **Split a 3,855-line class** before adding multiplayer features (2 engineers, no tests) | Split it into components, step by step | The graphics functions are **Blueprint-callable** (`QuadcopterPawn.h:743, 785`), so moving them can break Blueprints with no compile error: keep forwarding functions. Race progress belongs in a new **PlayerState**. The server accepts any checkpoint a client claims. |
| **Add an MCP server** to a design-data tool | Build it in Python as a separate package | Same choice, plus: **the repo has no way to publish to PyPI yet**, so `uvx` would serve stale data; the search engine finds its data by relative path (`core.py:15`), so the package must keep the folder layout. |
| **Consolidate three copies** of the same scripts | Keep the existing sync script and CI check | Same choice, plus: **a fourth copy syncs the other way** (`sync-assets.mjs:22-28`) and the CI check doesn't watch it. |
| **Scale real-time collaboration** to 3,000 concurrent editors (Outline) | Turn on Redis scaling and give collaboration its own Redis | Splitting the service and Redis are already config switches, but **Redis without routing each document to one server multiplies full-document saves**, and saving secretly uses the main Redis (`PersistenceExtension.ts:135`), so a dedicated Redis won't fix it. |
| **Add an enterprise audit log** (Outline) | Extend the existing Event model | Same choice, plus: **most of it already exists**: an admin audit filter no UI calls (`events.ts:40-45`); views are missing from the audit list; retention deletes at most 100k rows per run, which can fall behind once views are logged. |

The direction was usually the same. What changed was the bug you'd have hit in week 3.

---

## How it works

1. **Sizes the question.** Simple questions get a normal answer. Only real decisions get the full process.
2. **Maps your codebase.** Entry points, build and sync paths, what ships where, tests and CI, framework versions.
3. **Traces the change.** Who owns the state, where it's created, synced and used, and where the framework expects new code to live.
4. **Counts from real searches.** Every number and file reference in the report comes from a search or a file it read.
5. **Gets an independent code review.** A second agent re-reads the repository and attacks the draft before you see it.
6. **Plans the rollout.** Blast radius, steps that keep things working, how to check nothing broke, a timebox and an exit criterion.
7. **Saves the report** to `decision-reports/`.

It also checks current facts on the web when a library, version or service detail could change the choice, and asks you up to 3 questions only you can answer (or say "just decide").

### The report

| Section | What it tells you |
|---|---|
| **Verdict** | The decision in one sentence, and how confident it is |
| **What we found** | Findings from your code and from research, each with a file:line or source |
| **Blast radius** | Files and systems the change touches |
| **Decision map** | What each option is betting on, and the cheapest way to test it |
| **Will it last?** | Which future changes the design handles, and which break it |
| **Pre-mortem** | How it could fail, and the early warning sign |
| **Rollout** | Ordered steps, sizes, a timebox and when to stop |

---

## Results

Each pair of answers was compared by a separate reviewer that didn't know which came from the skill and checked code claims against the repository. On the large repo, every comparison was repeated with the answers' order swapped and again with both answers trimmed to the same length, to rule out a reviewer's bias toward position or length.

| Test | Result |
|---|---|
| **Fresh 358,000-line repo** (Outline, 3 decisions) | The skill's report was preferred in **2 of 3**, in every check (original, order swapped, equal length). The third was a **tie**: each answer won only when shown in the reviewer's favoured position |
| **Two smaller repos** (4 decisions) | The first version **lost all 4**. Those failures shaped the coding checks; with them, the skill **won all 4** on the same questions |
| **Blind human review** (3 Outline decisions) | The reviewer preferred the skill's answer in **3 of 3**, including the AI-judged tie. The reviewer is the skill's author; an independent review is still to come |
| **Wrong or overstated code claims** (all 7) | 2 in plain answers, 1 in the skill's |
| **Cost** | about 2.5–3.5× a plain answer |

See a full report in [`examples/`](examples/outline-collaboration-scaling.md). These are early results: one run per decision, and the reviewer is also a Claude model. The full test log, including the failures, is in [`benchmarks/`](benchmarks/2026-10-11-claude-code.md).

### Beyond code

It also handles other decisions where current facts matter, such as choosing a service or a big personal purchase:

| The question | Claude on its own | With Decision Check |
|---|---|---|
| A family with ₹35 L saved asks whether to buy a ₹1.25 crore flat | "Not yet. Check the costs first." | Banks lend at most 75% on loans this size, so they need ~₹31 L down and ~₹52 L on day one. **Save to ~₹50 L first.** |
| A team asks how to send 50,000 emails a day reliably | Said Amazon SES protects against duplicates | **SES has no duplicate protection**, so keep your own send log. |

---

## How it relates to Karpathy's LLM Council

Karpathy's project sends each question to several different AI models, has them review one another, and combines their answers. It's a great way to see how different models think. This skill keeps the idea of independent perspectives, here a separate agent that re-checks the work, but points it at one goal: getting a decision in your codebase right.

| | Karpathy's LLM Council | This skill |
|---|---|---|
| Approach | Several models answer and review each other | Reads your codebase, researches what it needs, and has the result independently reviewed |
| Effort per question | The same for every question | Scales with the question |
| Runs in | A local web app (OpenRouter key) | Claude Code (copy one folder) |

---

## Quick start

Copy this folder into your Claude Code skills folder:

| OS | Location |
|---|---|
| macOS / Linux | `~/.claude/skills/decision-check/` |
| Windows | `%USERPROFILE%\.claude\skills\decision-check\` |

```bash
git clone https://github.com/SanyamKhaiwal/decision-check.git ~/.claude/skills/decision-check
```

Then, inside your project, ask:

```text
decision check this: we want to add replays to our game. Build on the engine's replay
system or record our own data? Where should it live, and what's the plan?
```

It starts on `decision check this`, `check this decision`, `pressure-test this` or `stress-test this`, and on real decisions like "should we X or Y?" or "I'm torn between…". It stays out of the way for quick questions and for writing code; it plans the change, and your normal Claude Code session builds it.

---

## Good to know

- **Best for:** feature design, refactors, migrations, where new code should live, library and service choices, build vs buy.
- **Not for:** quick facts, or writing the code itself.
- **Early results:** one run per test, and the reviewer was also a Claude model.
- **Built for Claude Code:** it uses Claude Code's sub-agents for the independent review.

---

## Files

```text
decision-check/
├── SKILL.md          # the workflow
├── references/       # coding gates, research, checks and report template
├── examples/         # a real report, unedited
└── benchmarks/       # test log
```

## Contributing

The most useful contribution is a real comparison: ask the same coding question with and without the skill and [share what happened](../../issues/new?template=share-comparison.yml), win or lose. See [CONTRIBUTING.md](CONTRIBUTING.md).

MIT License · see [LICENSE](LICENSE)
