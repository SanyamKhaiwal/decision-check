# Coding decisions

Most decisions this skill sees are about code: a feature, a refactor, a migration, where something should live, which library to adopt. For these, the value isn't web research. It's **reading the codebase more carefully than a quick answer does**. In blind tests on real repositories, a plain answer beat an early version of this skill on every coding decision because it traced the code while the skill researched the web, and the skill misread the code in ways that would have cost weeks:

- It planned to record replays on the server, but movement in that codebase was client-authoritative, so the server only had a smoothed copy.
- It put a new MCP server in a folder a sync script copies into every user install, leaking a dependency into installs meant to have none.
- It moved world state into components when the framework's home for it is GameState and PlayerState.
- It said "about 40 replicated properties" when the code registers 22.

Apply every gate below to any decision about a codebase. Skip a gate only if it truly doesn't apply, and say so in the audit.

## The gates

### G0. Big repositories: search, don't read

For anything over roughly 20k lines you can't read everything, and skimming misses what matters. Work outward from the question:

1. **Find the boundaries** from build and package files (workspaces, modules, packages, targets), not by listing folders.
2. **Search for the symbols the question names** (and their obvious synonyms) and list the files that hit.
3. **Read only the files on the change path**: where the state lives, where it's created and consumed, and the entry points. Read the relevant functions, not whole large files.
4. **Record what you didn't read** in the audit, so the code reviewer knows where to look and the reader knows the limits.

### G1. Map before deciding

Before writing anything, find and note:

- **Entry points** for the area in question (main classes, modules, commands).
- **How code moves:** build scripts, packaging, sync or copy steps, generated folders, what ships to users and from where. Read the scripts, not just the folder names.
- **Safety nets:** tests, CI workflows, linters, smoke checks. Note what exists and what doesn't.
- **Engine, framework and language versions** (build files, manifests, lockfiles, target files).

### G1b. The repo's own rules

Read the project's written rules before recommending anything: CLAUDE.md or AGENTS.md, CONTRIBUTING, architecture docs or ADRs, lint and formatter configs, CI workflows, CODEOWNERS. A recommendation that breaks a rule the team already wrote down is wrong, however good it looks in general. Cite the rule.

### G1c. Precedent: has this repo solved this before?

Search for the closest existing example of the same kind of change (another feature with a similar shape, an earlier migration, an existing extension point, a pattern used three times already). Prefer extending that pattern over inventing a new one, and name the files. If you depart from it, say why.

### G1d. Git history (when there's a `.git` folder)

A few commands, not a project:

- `git log --oneline -15 -- <files on the change path>`: is this area changing right now, and is there a refactor in flight?
- `git log --format='%an' -50 -- <path> | sort | uniq -c | sort -rn | head`: who works here?
- High churn in the files you'll touch is a risk to name in the pre-mortem.

Skip it if there's no history, and say so.

### G2. Trace the change end to end

For the state or behaviour the decision touches, follow it through the code:

- **Who owns it and who is authoritative?** Which process, machine, thread or module creates the truth, and which ones only hold copies (replicated, cached, smoothed, derived)?
- **Where is it produced, transformed, sent, stored and consumed?** Name the functions.
- Any recommendation that records, moves, caches or validates that state must sit where the truth is, or say why not.

### G3. Placement and propagation check

For every new file, folder, dependency or service the recommendation adds:

- Will a build, sync, copy, bundle or publish step carry it somewhere it shouldn't go (user installs, other targets, production bundles)?
- Does it add a runtime dependency to something that is meant to have none?
- Does it cross a boundary the repo already enforces (a rule in CLAUDE.md, a CI check, a lint)?

### G4. Framework conventions

Ask where the framework itself expects this kind of code to live, and compare with where the recommendation puts it. Examples: Unreal's GameState, PlayerState, subsystems and components; Django apps; React hooks and context; Python packages and entry points; monorepo package boundaries. If the recommendation departs from the convention, say why.

### G4b. Security and data integrity

For every new data flow, endpoint, integration, export or stored record, check:

- **Who can see it?** Does it respect existing permissions, or could a shared token, cache, preview or admin bypass show data to someone who shouldn't see it?
- **What can be injected?** Untrusted input reaching queries, HTML, shell commands, file paths, or CSV/spreadsheet cells (formula injection).
- **What gets deleted, and when?** Retention, cascade deletes (deleting a team, user or parent record), backups, and whether that matches the promise being made (for example "kept for 1 year").
- **What's stored that shouldn't be?** Secrets, credentials or personal data in logs, save files, analytics or third-party calls.

In testing, a plain answer caught a permission leak, CSV formula injection and a cascade delete that broke a retention promise, all of which the report missed. Put anything found here in the pre-mortem or the plan.

### G5. Blast radius from searches, not estimates

List the files and symbols the change touches, using real searches. Every count in the report (call sites, methods, properties, lines, files) must come from a command or a file you read; keep the command in the audit (for example `grep -c "DOREPLIFETIME" QuadcopterPawn.cpp`). If you didn't count it, write "estimate" next to it and give the basis in a few words ("estimate: ~2 KB per row × 1M rows a day"). A threshold with no basis ("switch at 50M rows") is a guess; either ground it or call it one.

### G5b. Every code claim carries its proof (the claims ledger)

Each statement about the repository in the report (a file does X, a function exists, a workflow checks Y, a folder must stay) gets a `file:line` reference or the command that shows it. State only what the code shows: "the installer reads `cli/assets` at runtime (init.ts:25, 183)", not "cli/assets must stay committed". If the conclusion goes beyond the evidence, say it is a judgment and why. Before writing, re-check any claim about configuration filters, paths or globs against the file itself; they are easy to misread.

Keep a **claims ledger** in the saved report's audit: one line per code claim the verdict depends on, with the `file:line` or command that proves it. Give the ledger to the code reviewer, who verifies it. A claim that isn't in the ledger doesn't go in the report.

### G6. Verification and rollout

- **How will the team know nothing broke?** Use the existing tests and CI; if there are none, name the cheapest safety net to add first (characterization tests, a smoke checklist, a recorded baseline).
- **Order of work:** steps that keep the codebase working after each one, each with a rough size, plus a timebox and an exit criterion ("stop after step 3 if…").
- Check the plan against the team size and deadline, in numbers.
- **Make the build concrete:** a week-by-week schedule for anything longer than a week, and the interface of anything new (class or component names and responsibilities, tool or API signatures, data format with a version field). A plan a team can start on Monday beats a list of principles.

## The code reviewer (replaces the web researcher for code)

For a coding decision, the sub-agent's job changes. If the deciding facts are in the repository, run a **code reviewer** instead of a web researcher, after you have a draft. It re-reads the repository independently and attacks the draft's claims about it. Run a web researcher as well only when a library, framework or version fact could flip the choice (for example "does this SDK support X", "is this API deprecated in our version"). On high stakes, both are allowed.

### Code reviewer prompt

```
You are the code reviewer for a decision report about this repository:
[repo path]. You may read files and run read-only searches. Do not modify
anything.

DECISION AND CONTEXT:
---
[the decision, constraints, user's answers]
---
DRAFT RECOMMENDATION AND PLAN:
---
[draft]
---
CLAIMS LEDGER:
---
[each code claim with its file:line or command]
---
FILES NOT READ (big repos):
---
[list]
---

Check the draft against the code, independently:
1. Verify the claims ledger: every claim the verdict depends on. Mark each
   correct / wrong / overstated / unverifiable, with the file:line or
   command you used. Re-run counts and re-read any path or glob filters.
1b. Precedent and rules: is there an existing pattern in the repo, or a
   written rule (CLAUDE.md, CONTRIBUTING, ADRs, lint, CI), the draft
   ignored or contradicts?
2. Authority and data flow: does the recommendation put recording,
   validation, caching or ownership where the truth actually lives?
3. Placement: will any new file or dependency be carried by a build,
   sync, copy or publish step somewhere it shouldn't go?
4. Framework conventions: is there an idiomatic home for this the draft
   ignored?
4b. Security and integrity: can anyone see data they shouldn't (shared
   tokens, caches, previews, admin bypass)? Any injection path (including
   CSV formulas)? Does any delete or retention rule break a promise?
5. Blast radius and safety: what else does the change touch that the draft
   didn't list? What would break, and how would the team notice?

Do not invent problems. If the draft holds, say so.

Output, under 300 words:
VERDICT_HOLDS: yes | no | partly
CLAIMS: <claim — correct/wrong/unverifiable — evidence>
FINDINGS:
- [MATERIAL | MINOR] <finding, with file:line evidence>
IF_NOT_HOLDS: <what should be recommended instead, in two sentences>
```

Fold every correct finding into the report. A wrong code claim in the draft must be fixed, not footnoted.

## What changes in the report

For coding decisions, the report adds or sharpens these:

- **What we found in the code** leads "What we found": owner and authority, propagation paths, existing safety nets, with file:line references.
- **Blast radius:** a short list of the files and systems the change touches, with counts from searches.
- **Rollout:** ordered steps that keep things working, with sizes, a timebox and the exit criterion. This replaces a generic plan.
- **Will it last?** stays, using the codebase's own growth paths (new entity types, more players, new targets).
