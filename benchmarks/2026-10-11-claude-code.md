> **Note:** the skill was renamed from *llm-council* to *decision-check* after these tests. Runs below refer to it by its old name.

# Benchmark runs: Claude Code, 2026-10-11

Model: Claude Opus 5.5 in Claude Code, sub-agents. One run per cell, scored by the author.
Tokens are sub-agent tokens as reported by the harness. They exclude the orchestrator's own work (framing, evidence searches, Gate A/B), so the council's true cost is somewhat higher.

| Test | Question | Run | Calls | Tokens | Ratio | Verdict |
|---|---|---|---|---|---|---|
| T0 | Drone racer: physics authority for ranked races | Model alone (reads code itself) | 1 | 61.6k | 1× | Hybrid: client physics + server validation + replay audit |
| T0 | same | Council, Full (4 advisors, 2 reviewers, chairman) | 7 | 295k | 4.8× | Same direction; Medium confidence |
| T1 | same | Model alone **given the council's Evidence Brief** | 1 | 38.6k | 0.6× | Same direction |
| T2 | SQLite vs Postgres, personal habit tracker | Model alone | 1 | 32.7k | 1× | SQLite |
| T2 | same | Council, Quick (3 advisors, 0 reviewers, chairman) | 4 | 153k | 4.7× | SQLite; Medium confidence |
| T3 | Career: stable MNC vs Series A fintech offer (Bengaluru) | Model alone | 1 | 33.3k | 1× | Lean take, if runway/licence/people check out |
| T3 | same | Council, Standard (4 advisors, 0 reviewers, chairman) | 5 | 196k | 5.9× | CONDITIONAL: take if 18+ months runway, licence path, ESOP terms in writing |

## What each comparison showed

**T0 vs T1: where the value came from.** Given the same Evidence Brief, the model alone found nearly everything the council found: the listen-server host can't be trusted with rankings, drone-to-drone collisions are live, turbulence needs a seed, the config needs a hash check, input bots pass any physics check. The council's unique additions were smaller: gating the replay audit on a measured drift test, the 60 Hz vs 120 Hz input gap, the ranked-demand question, and a calibrated confidence. Conclusion: on this question the **evidence pass** carried most of the value, not the number of agents.

**T2: simple question.** Same answer. The council added a timezone/day-boundary warning and the "live `cp` corrupts SQLite" backup warning; the model alone added the ephemeral-disk caveat. Not worth 4.7×. Note the council ran only because the prompt used a trigger phrase, which forces at least Quick; scored on its own merits the question is Direct tier (0 extra calls).

**T3: real-life decision.** Same direction. The council's evidence pass checked ESOP tax rules (exercise is taxed as salary even if unsellable; deferral needs an 80-IAC IMB certificate, not just DPIIT recognition) and the 2026 funding climate; the model alone mentioned exercise tax but not the deferral rule, and stated unchecked figures (e.g. "rehired at ₹40L+"). The model alone gave more practical tips (negotiation, health insurance). CLARIFY did **not** fire: the chairman judged that the unstated goals (dependents, stability) wouldn't flip the choice and put them under "What would change this", calling it borderline.

## Gaps not covered
- No dollar costs yet (token counts only).
- One run per cell; no blind scoring.
- CLARIFY still not observed in a run.

## Model comparison: same inputs, cheaper models

Same framed questions and Evidence Briefs as above; only the sub-agent model changed.

| Question | Opus council | Cheaper council | Tokens (Opus → cheaper) | Deviation |
|---|---|---|---|---|
| SQLite vs Postgres (Quick) | SQLite, Medium | **Haiku**: SQLite, Medium | 153k → 162k | Same verdict. Haiku's plan says to back up by copying the database file; Opus warned that copying a live SQLite file can corrupt it and said use `sqlite3 .backup`. Missed the timezone/day-boundary point. Small but real. |
| Career offer (Standard) | Conditional: take if 18+ months runway, licence, ESOP terms | **Sonnet**: same conditional | 196k → 205k | None material. Sonnet added two points Opus missed: check what the ₹24 LPA includes (bonus, stock), and label the 18-month bar as a judgment, not a fact. |
| Drone authority (Full) | Hybrid, Medium, 7 calls | **Sonnet**: hybrid with a re-sim test as the decision gate, Medium, 8 calls | 295k → 333k | Same direction. Sonnet advisors split (one argued for full server authority), so Gate B ran 3 reviewers instead of 2. Final report equally thorough: dedicated server prerequisite, collisions off, input-level cheats, pre-set tolerance. It listed the engine version as open, but that came from the shared Evidence Brief (written before the "search twice" rule), not from Sonnet. |

**Token counts barely change with the model.** Each sub-agent pays a similar fixed setup cost (~35k tokens here) whatever the model, so a cheaper model saves money through its price per token, not through fewer tokens.

**Routing adopted** (see `references/triage.md`): Quick = Haiku advisors + Sonnet chairman; Standard = Sonnet throughout; Full = Sonnet advisors and reviewers + Opus chairman.

## v2: verify-first ladder (same questions, same Evidence Briefs)

The new design answers directly, or drafts an answer and has one verifier sub-agent try to break it, and adds advisors one at a time only on a material finding. The draft was written by a fresh agent with only the question and brief (standing in for the main session, which in real use writes it; same cost), so prior council results couldn't leak in.

| Question | Gate A | Path taken | Sub-agents beyond the draft | Tokens | vs single answer | vs old council |
|---|---|---|---|---|---|---|
| SQLite vs Postgres | 1/8 | Direct | 0 | ~33k | ~1× | 153k → ~33k |
| Career offer | 5/8 | Verified → **CLARIFY** | 1 verifier (Sonnet) | 80k | 2.4× | 196k → 80k (−59%) |
| Drone authority | 7/8, high stakes | Verified → escalated: +Executor → chairman | 3 (verifier and chairman Opus, Executor Sonnet) | 176k | 2.9× | 295k → 176k (−40%) |

**Career.** The verifier marked three findings material: the downside wasn't weighed against staying, negotiation wasn't considered, and the draft assumed no dependents. The first two are fixable in a sentence, so they don't escalate. The third is something only the user knows and it flips the answer, so Gate V asked one question: "Do you have dependents or a big financial commitment in the next two years?" **First CLARIFY in any run.**

**Drone.** The verifier marked two findings material: inputs arrive unreliably at 60 Hz against a 120 Hz sim, and drone-to-drone contact happens against proxies the server can't reproduce. High stakes means any material finding escalates. One advisor (the Executor, blind to the draft) resolved it: don't make re-simulation the main check; use plausibility checks plus sequenced input logs, with re-sim as an audit only. The Opus chairman accepted all six verifier findings and adopted the Executor's ordering. The final report covers everything the old 7-agent council found (dedicated server for ranked, collisions off, sequenced inputs, seeds, config hash, input-level bots, Medium confidence) plus the re-sim-as-audit correction, at 60% of its cost. It still listed the engine version as open, because the shared Evidence Brief did.

**Caveat.** The drone draft was the "single answer + evidence brief" run, which had already found the host-trust problem, so the verifier didn't need to. On a question where the draft misses something that big, escalation would add more advisors and cost would rise toward the 4–5× ceiling, as designed.

## Stress test: v2 on four fresh scenarios, blind-judged

Each scenario ran twice: a single answer (Opus, with full tool access, as a user gets without the skill) and the v2 skill (evidence pass, draft, verifier, escalation only on material findings). An Opus judge scored each pair blind (A/B shuffled by code; the skill's audit notes stripped).

| Scenario | Gate A | Skill path | Single answer | Skill | Cost | Blind verdict | Material difference? |
|---|---|---|---|---|---|---|---|
| Coding: add a fixed-wing to the UE5 drone codebase | 6, high stakes | Verified → escalated (+Executor) → chairman | 42.0k | 168.2k | 4.0× | Tie | No. Skill better calibrated (the single answer stated unchecked code details, one doubtful) |
| System design: 50k events/day delivery | 4 | Verified; 2 material findings fixed in place | 36.5k | 77.0k | 2.1× | Skill, slightly | No. Skill caught that SKIP LOCKED alone breaks per-customer ordering and added a lease; same build |
| Real life: buy a ₹1.25 cr flat vs rent | 7, high stakes | Verified; all findings minor | 36.8k | 75.2k | 2.0× | **Single answer** | **Yes, for the single answer.** It totalled upfront costs (₹42–50 L vs ₹35 L saved), so the plan is unfunded, and added Khata/OC checks, insurance, capital-gains tax on selling funds |
| AI development: RAG vs fine-tuning | 4 | Verified; all findings minor | 36.2k | 74.6k | 2.1× | Tie (single slightly more useful) | No. Same decision; single answer pointed to ready-made self-hostable tools |

Skill tokens = draft (stand-in for the main session) + verifier + any escalation agents; the orchestrator's evidence searches are not counted.

**Result: the skill did not beat a single strong answer in a way that matters on any of the four.** It won one narrowly, tied two, and lost the one material comparison. Its verifier did catch real flaws (the SKIP LOCKED ordering bug; the plane can't reuse a hover autopilot; a refactor committed before the dependency read), but the single answers mostly avoided those flaws on their own.

**Why the skill lost Q3.** The single answer searched the web itself and found registration, stamp duty and property-check facts. The skill's evidence pass for Q3 ran two searches and left those costs "not checked", and the draft could only use the brief. The verifier flagged the shortfall as minor. The skill was only as good as its evidence pass, and here the evidence pass was weaker than what one model with a search tool did unprompted.

**Caveats.** One run per cell; one judge from the same model family; the skill's draft agent was limited to the Evidence Brief, while in real use the main session can keep researching while it drafts.

## v3: decision-report redesign, same four scenarios, blind-judged on unique information

v3 drops the advisor debate. The main session finds the deciders, asks what only the user knows (here: "just decide", so it assumed and showed branches), runs two parallel researchers that must open primary sources, applies the five lenses itself, and writes a report led by new findings, a decision map, the option nobody listed and a pre-mortem. To avoid contamination, fresh agents played the main session (one planned, one wrote). The judge counted decision-changing items that appear in only one answer.

| Scenario | Single answer | v3 skill (planner + 2 researchers + writer) | Real-use estimate* | Unique HIGH / MEDIUM items: single vs skill | Winner |
|---|---|---|---|---|---|
| Coding: fixed-wing in UE5 | 42.0k | 204.6k (4.9×) | ~170k (4.0×) | 0/1 vs 0/3 | Skill (narrow) |
| System design: 50k events/day | 36.5k | 237.7k (6.5×) | ~203k (5.6×) | 0/0 vs **1**/3 | Skill |
| Real life: flat vs rent | 36.8k | 198.5k (5.4×) | ~164k (4.4×) | 0/1 vs **1**/4 | Skill |
| AI dev: RAG vs fine-tuning | 36.2k | 187.9k (5.2×) | ~153k (4.2×) | 0/2 vs **1**/1 | Skill (narrow) |
| **Total** | | | | **0/4 vs 3/11** | **Skill 4–0** |

*Planner and writer are one context in real use, so one fixed setup cost (~35k) is subtracted.

**HIGH items the single answer lacked, all spot-checked:**
- System design: Amazon SES has no idempotency token, so retries can double-send email and the team needs its own send ledger. The single answer stated the opposite (a material error). No official SES idempotency parameter found; AWS re:Post confirms duplicates on retry.
- Real life: the RBI raised the repo rate to 5.50% on 7 Oct 2026 (first hike since 2023), so floating EMIs are rising, plus an unsold-inventory glut that gives buyers room to negotiate. Rate hike confirmed in multiple reports.
- AI dev: CVE-2026-44560, Open WebUI's RAG retrieval skipped access checks before 0.9.0, and admins bypass knowledge-base restrictions by default. Confirmed in NVD-derived entries (OSV, CERT-HR).

**Same headline decision in all four.** The skill's value was current, checked facts and risks, not a different verdict. The judge rated the extra length justified in all four.

**Cost is over budget.** The design targeted ≤3×; measured real use is about 4–5.5×. Researchers cost 47–77k each (12–19 searches and page reads), not the ~35k assumed. The single answer kept one unique point the skill missed (capital-gains tax on selling funds, flat scenario) and, in AI dev, useful tool pointers.

Caveats: one run per cell; one judge from the same model family; the skill was Answer B in all four pairs by random draw.

## v4: freshness-first research (same four scenarios, blind-judged)

Change from v3: only "fresh or specific" deciders are researched (rates, versions, advisories, exact API capabilities, local rules), deepest on the one most likely to flip the decision, about 8 tool calls per researcher, one researcher when the fresh deciders fit one area. One agent played the whole main session (planned, then was resumed to write), so its fixed cost counts once.

| Scenario | Single answer | v4 skill | Cost | vs v3 real use | Unique HIGH/MEDIUM: single vs skill | Pass bar (≥1 HIGH or ≥3 MEDIUM)? | Winner |
|---|---|---|---|---|---|---|---|
| Coding: fixed-wing in UE5 | 42.0k | 112.4k (main 64.1k + 1 researcher 48.3k) | **2.7×** | 170k → 112k | 0/1 vs 0/4 | Yes | Skill |
| System design: 50k events/day | 36.5k | 168.1k (main 54.9k + 2 researchers) | 4.6× | 203k → 168k | 0/3 vs 0/5 | Yes | Skill (narrow) |
| Real life: flat vs rent | 36.8k | 155.6k (main 56.2k + 2 researchers) | 4.2× | 164k → 156k | 1/3 vs 1/5 | Yes | Skill |
| AI dev: RAG vs fine-tuning | 36.2k | 149.1k (main 54.4k + 2 researchers) | 4.1× | 153k → 149k | 0/3 vs **2**/2 | Yes | Skill |
| **Total** | | | | | **1/10 vs 3/16** | **4 of 4** | **Skill 4–0** |

**Quality held.** The skill won all four blind and cleared the bar in all four. HIGH items unique to the skill: the flat's day-one cash gap with the 7 Oct 2026 rate hike and registration-fee change (S3); Onyx keeps per-document permission sync in its paid edition, and 2026 vulnerabilities in Ollama, vLLM and Open WebUI (S4). Some v3 wins didn't recur (the SES idempotency gap, the specific Open WebUI CVE) and others appeared, so which fresh facts get found varies run to run.

**Cost only partly fixed.** With one researcher the report hit 2.7×. With two it stayed at 4.1–4.6×: researchers ignored the ~8-call budget (11–14 calls, 47–60k each), and the main session costs ~55k (reading the skill files) against ~37k for a plain answer.

**Next lever:** one researcher by default with at most 5 questions; two only on high stakes. On this run that would put S2 and S4 near 2.8×; S3 (high stakes) would stay near 4×.

The single answer still held items the skill lacked in every scenario (for example term life and health insurance before signing in S3; ready-made job libraries in S2).

## v5: one researcher by default (two only on high stakes)

Reran the two non-high-stakes scenarios with one researcher (at most 5 ranked questions, hard limit of 8 tool calls). Same single answers, blind judge, plus an item-by-item check against v4's two-researcher reports.

| Scenario | Single answer | v5 skill | Cost (v4 → v5) | Unique HIGH/MEDIUM: single vs skill | Pass bar? | Winner |
|---|---|---|---|---|---|---|
| System design: 50k events/day | 36.5k | 103.6k (main 53.2k + researcher 50.4k) | 4.6× → **2.8×** | 0/3 vs **1**/3 | Yes | Skill (narrow) |
| AI dev: RAG vs fine-tuning | 36.2k | 100.1k (main 52.7k + researcher 47.4k) | 4.1× → **2.8×** | 0/3–4 vs **2**/2 | Yes | Skill |

**What one researcher kept and lost (vs v4's two):**
- **AI dev: no decision-changing loss.** Both HIGH findings kept: Onyx's free edition doesn't sync document permissions, so everyone sees every document; 2026 vulnerabilities in vLLM (unauthenticated remote code execution) and Ollama. Lost one MEDIUM (Open WebUI advisories). Gained a model-licence check and the `trust_remote_code` setting.
- **System design: lost four MEDIUM findings** (the Lambda + SQS FIFO reordering trap, pgmq not installable on RDS, Svix strict ordering only on Enterprise, the "are events written in the same transaction?" check). The researcher hit the budget before its lower-ranked questions. **Gained one HIGH** that v4 lacked: AWS warns that a dead-letter queue on SQS FIFO breaks exact ordering, so SQS forces a choice between blocking a customer and losing order. The recommendation didn't change.

**Result:** at ~2.8× (down from 4.1–4.6×), both reports still beat the single answer and cleared the bar with at least one HIGH finding each. One researcher keeps the top-ranked finds and drops the tail, so ranking the questions well matters.

Caveat: in this round the judge also saw the retention files, which contained the same skill text, so Part 1 wasn't fully blind (the judge reported this). One run each.

## v6: change test, single-answer floor, numbers over adjectives

Added three main-session checks (no extra sub-agents): a change test for technical decisions (which future changes the design absorbs, extends or breaks, with breaking points), a single-answer floor (include what a strong quick answer would say), and numbers over adjectives (calculate the figures the decision turns on). Reran coding, system design and the flat, blind-judged against the same single answers.

| Scenario | Path | Cost | Unique HIGH/MEDIUM: single vs skill | Previous round (single vs skill) | Long-term view | Winner |
|---|---|---|---|---|---|---|
| Coding: fixed-wing in UE5 | Gate scored high stakes this time: 1 researcher + red-team | 178k (**4.2×**) | 0/3 vs **2**/5 | 0/1 vs 0/4 (v4) | Skill: specific with numbers, changed the plan; single: generic | Skill |
| System design: 50k events/day | 1 researcher | ~106k (**~2.9×**, main session cut short by a usage limit after saving its report) | 0/3 vs 0/5 | 0/3 vs 1/3 (v5) | Skill: specific with numbers, didn't change the plan | Skill (narrow) |
| Real life: flat vs rent | High stakes: 2 researchers | 158k (**4.3×**) | 0/2 vs **2**/6 | 1/3 vs 1/5 (v4) | n/a | Skill |
| **Total** | | | **0/8 vs 4/16** | v4/v5 same scenarios: 1/7 vs 2/12 | | **Skill 3–0** |

**What worked**
- **Numbers over adjectives** produced the flat's two HIGH items: banks lend at most 75% on loans above ₹75 L, so the planned ₹25 L down payment isn't allowed (~₹31 L needed); and registration charges of ~₹11–12 L. The single answer's figures were out of date and ignored the lending cap.
- **Red-team + change test** produced the coding HIGH items: the full base-class refactor needs ~17 engineer-weeks against 16 available, so the verdict changed to "interface first, base class after the plane flies"; and a breaking point for checkpoints and net smoothing at plane speeds.
- **The single answer's HIGH items are gone** (it had one in the previous flat run; none this time).

**What didn't**
- **The single-answer floor barely moved the single answer's own MEDIUM items** (7 before, 8 now). They were mostly implementation detail: a working table schema, separate ordering for email and webhooks, SQS FIFO limits, phased interiors. None would flip a choice, but the report still isn't a full superset.
- **The change test added length without changing the plan in system design.**
- **Cost:** high-stakes paths ran at 4.2–4.3×; the normal path stayed near 3×. The gate scored the coding question as high stakes this run (5/8 last time), which added the red-team.

## End-to-end tests with the installed skill (2026-10-12)

Each test agent received only the user's message and used the installed skill on its own (no orchestration).

| Test | Prompt | Result |
|---|---|---|
| 1. Simple | "council this: tabs or spaces for personal Python scripts?" | Pass. Triggered, gated as simple, answered directly; 0 sub-agents, ~36k tokens (~1×). Gave a plain reason rather than the gate score. |
| 2. Should not trigger | "Time complexity of sorted()?" | Pass. Skill not used; cited the skill's own exclusion. |
| 3. Ask first | "council this" on Vercel vs Hetzner vs Cloudflare | Pass. Asked three questions only the user could answer (bandwidth makeup, who runs a server, Vercel features used) before spending anything. |
| 4. Full pipeline (first run) | Test 3 continued with the user's answers | **Partial.** Sensible recommendation, 1 Sonnet researcher, report saved, but the session skipped `report.md` and `lenses.md` (5 tool calls in total): a 201-word report with none of the template sections. |
| 4b. Full pipeline after fix | Same question, answers given up front | **Pass.** Read all four reference files; full template (new findings, assumptions, decision map, option not listed, Will it last?, pre-mortem, footer); 1 Sonnet researcher; report saved. Main session 50.8k tokens. |
| 5. Trigger without the phrase | "I'm torn between learning Rust or Go…" | Pass. Triggered, gated as a real decision, asked three questions first. |

**Fix applied after test 4:** SKILL.md now marks each reference file as a required **Read:** at its step, tells the main session to pass the researcher prompt word for word, and lists the required report headings inline so the structure survives even if a file is skipped.

**Spot-check of 4b's freshest claim:** Hetzner's 15 June 2026 cloud price increase (CPX about 2.4–2.75×, CX/CAX about 1.3×) is confirmed by Northflank, heise and others.

**Still open:** researchers went over the 8-call limit in both full runs (10 calls); single-agent mode (no sub-agents) not tested with this design.

## Coding benchmark: real codebases, real skill runs (2026-10-12)

Four coding decisions on two real repositories: a UE5 C++ drone simulator (~10,500 lines; 3,855-line main class) and ui-ux-pro-max (Python + TypeScript, ~35,000 lines). Each was answered by Claude Code with no skill (full repository access) and by the installed skill run end to end. A blind judge (Claude Opus) with read access to the repositories verified each answer's code claims and counted decision-changing items unique to each side.

| # | Decision | Round 1 (skill before coding gates) | Round 2 (with coding gates) |
|---|---|---|---|
| C1 | UE5: race replays and ghost racing | Plain won | Plain won → **skill won** after the saved-report fix |
| C2 | UE5: split the 3,855-line pawn now or later | Plain won | **Skill won** |
| C3 | Python/TS: consolidate three copies of scripts | Plain won | **Skill won** (narrow) |
| C4 | Python/TS: where to build an MCP server | Plain won | **Skill won** |
| | **High-value items only one side had** | Plain 3, skill 0 | **Skill 3, plain 0** |

**Round 1 defects (skill lost 0–4):**
- Misread ownership: planned to record replays on the server, but movement is client-authoritative (C1).
- Placement: put the MCP server in a folder the sync script copies into every user install (C4).
- Missed framework convention: world/match state belongs in GameState/PlayerState (C2).
- Inflated count: "about 40 replicated properties" (the code registers 22) (C2).
- Wrote one report before its researcher returned (C2).
- Web research was spent where the codebase held the deciding facts.

**Fixes (new `references/code.md`, gates G1–G6):** map the codebase first (entry points, build/sync/publish paths, tests, versions); trace ownership and data flow; placement and propagation check; framework conventions; counts from searches; verification and rollout; an independent **code reviewer** sub-agent re-reads the repository and attacks the draft (web research only when a library or version fact decides it); sub-agents always run in the foreground.

**After round 2, three more fixes:** the saved report must contain the full chat text (one file held a placeholder, which lost C1); every code claim carries `file:line` proof; a concrete build (week-by-week schedule, interfaces). C1 was rerun after these and won.

**Round 2 findings the plain answer missed, verified in the code:**
- C1: nothing in the C++ calls `StartCourse()`, so a recorder hooked to `OnCourseStarted` may never start; the save file stores a plaintext password (`UserSaveGame.h:22`), so recordings get their own slot.
- C2: graphics functions are BlueprintCallable (`QuadcopterPawn.h:743, 785`), so moving them can break Blueprints with no compile error; race progress belongs in a new PlayerState; the server accepts any ring claim.
- C3: a fourth copy syncs the other way (sub-skills from `.claude/skills` into `cli/assets/skills`, `sync-assets.mjs:22-28`); the CI check doesn't watch the sub-skill folders.
- C4: nothing publishes to PyPI yet, so `uvx` would serve stale data; `core.py:15` finds data by relative path, so the package must keep the folder layout; anything in `scripts/` is synced into every install.

**Remaining issues the judge noted:** occasional overstated conclusions (one wrong claim about a CI path filter in C3), and self-certified confidence.

**Cost:** main session 58–65k tokens vs 39–45k for the plain answer; the code reviewer sub-agent's tokens aren't reported separately, so the total is estimated at roughly 2.5×.

## Large-repository benchmark: Outline (357,834 lines of TypeScript/JavaScript)

Cloned [outline/outline](https://github.com/outline/outline) (commit 17ad514e1). Three realistic decisions, each answered by Claude Code with no skill (full repository access) and by the installed skill end to end, after adding five more coding fixes (big-repo search method, the repo's own rules, precedent, git history, claims ledger). A blind judge (Claude Opus) with repository access verified code claims.

| Decision | Skill's key finding (verified in the code) | High-value only one side had: skill / plain | Quality (of 8): skill / plain | Winner |
|---|---|---|---|---|
| D1 Enterprise audit log | Most of it already exists: an admin `auditLog` filter on `events.list` (`events.ts:40-45`) that no UI calls; `views.create` (`View.ts:83`) is missing from the audit list; retention is hard-coded at 365 days and deletes at most 100k rows per run, which can fall behind once views are logged | 1 / 0 | 8 / 7 | **Skill** (narrow) |
| D2 Collaboration latency at 3,000 editors | Splitting the service and Redis scaling are existing config switches (`env.ts:350-356`, `collaboration.ts:51-58`); Redis without per-document routing multiplies full-document saves; the per-document connection limit is per server; saves use the default Redis client, a hidden shared dependency (`PersistenceExtension.ts:135`) | 2 / 0 | 8 / 6 | **Skill** |
| D3 Jira integration | Copy `plugins/linear` (13 files, 945 lines); a Jira-side panel needs a Forge app because Atlassian Connect is closed to new apps (Connect support ends 31 Jan 2027); remote issue links need no Jira app | 1 / 1 | 8 / 7 | **Skill** |

Code-claim accuracy: skill all correct; plain answer one wrong claim (D3, about which hooks the Linear plugin registers).

**Weaknesses the judge found in the skill, and the fix:** it missed security and integrity points the plain answer caught (a shared token leaking private issue titles in previews, CSV formula injection, cascade deletes breaking a retention promise), and gave thresholds without a basis. Added gate G4b (security and data integrity) to `code.md` and to the code reviewer's checklist, and required every estimate to show its basis.

**Cost:** main session 59–73k tokens vs 40–46k for the plain answer (1.5–1.6×); with the code reviewer (and in D3 a web researcher) the total is estimated at roughly 2.5–3.5×, since sub-agent tokens aren't reported separately.

## Bias checks on the large-repository benchmark

To test whether the judge's verdicts were real or artefacts, each Outline pair was rejudged twice by fresh Opus judges: once with A and B swapped, once with both answers compressed by a neutral editor to about the same length (642–751 words, keeping every fact and step).

| Decision | Original | Order swapped | Length matched | Conclusion |
|---|---|---|---|---|
| D1 Audit log | Skill (narrow) | Plain | Plain | **Tie / leans plain.** The skill won only when it was Answer B |
| D2 Collaboration scaling | Skill | Skill | Skill | **Skill**, robust to order and length |
| D3 Jira integration | Skill | Skill | Skill (narrow) | **Skill**, robust to order and length |

**Position bias is real:** Answer B won 7 of the 9 judgments. Results that don't survive an order swap shouldn't be reported as wins. Earlier rounds in this log used a single random order, so their narrow wins (C3 and the original D1) should be read as uncertain.

**Honest headline:** on a fresh 358k-line repository, the skill was preferred in 2 of 3 decisions under every check; the third was a tie.

## Human review (blind)

The three Outline pairs, in their equal-length versions, were shown on a review page in a fresh random order with no labels; the answer key was kept outside the page. Reviewers picked the answer they'd rather hand to an engineering team.

| Decision | Reviewer 1 (the skill's author) | AI judge after bias checks |
|---|---|---|
| D1 Audit log | **Skill** | Tie |
| D2 Collaboration scaling | **Skill** | Skill |
| D3 Jira integration | **Skill** | Skill |

Picks were A, B, B, so not a position pattern. Caveat: reviewer 1 wrote the skill and may recognise its report style even unlabelled. An independent developer's review is still to come.
