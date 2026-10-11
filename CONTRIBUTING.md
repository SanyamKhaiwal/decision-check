# Contributing to Decision Check

Thanks for helping. The most useful contributions to this project are evidence: real runs that show where the skill helps, where it doesn't, and why.

## Ways to contribute

| Contribution | How |
|---|---|
| **Share a comparison** | Ask the same coding question in Claude Code with and without the skill, and open an issue with the *Share a comparison* template. Wins and losses are equally welcome |
| **Report a problem** | The skill gave a wrong code claim, skipped a step, triggered when it shouldn't have, or produced a broken report: use the *Bug report* template |
| **Suggest an improvement** | A new check, a better prompt, a clearer report section: use the *Improvement idea* template first, so we can discuss it before you write it |
| **Improve the docs** | Typos and clarifications can go straight to a pull request |

## How the skill is organised

| File | What it controls |
|---|---|
| `SKILL.md` | The workflow Claude follows, step by step |
| `references/code.md` | The coding gates (mapping, ownership, placement, conventions, security, claims ledger, rollout) and the code reviewer prompt |
| `references/triage.md` | When to answer directly vs write a report, and the "ask first" rules |
| `references/research.md` | What gets researched, the researcher prompt and source rules |
| `references/lenses.md` | The five lenses, change test, single-answer floor and red-team |
| `references/report.md` | The report template and confidence rules |

## Changing the skill

Every change to `SKILL.md` or `references/` should come with evidence that it helps:

1. **Say what failed.** Link the run or issue that shows the problem.
2. **Make the smallest change** that addresses it, in the file that owns that behaviour (see the table above). Don't restate rules in more than one place.
3. **Re-run it.** Run the same question with the changed skill in Claude Code and include the before/after in the pull request. For changes to the coding gates, use a real repository.
4. **Keep the description under 1024 characters** (the `description` field in `SKILL.md`).
5. **Update `benchmarks/`** if your change came with a new test result.

## Style

- Plain English, short sentences, concrete examples.
- Instructions say *what to do and why*, not just what not to do.
- No claims in the README that the benchmark log doesn't support.

## Pull requests

Keep them focused on one change, describe the problem and the evidence, and fill in the pull request template. By contributing, you agree your work is released under the [MIT License](LICENSE).
