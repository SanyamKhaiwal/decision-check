# Triage: gate, deciders, questions

Everything here is done by the main session. None of it spawns a sub-agent.

## Gate: answer directly or write a report

Score the question 0, 1 or 2 on each factor. Score from the facts in the question, not from how important it sounds.

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| **Stakes** | Trivial cost if wrong | Meaningful cost if wrong | Large money, security, legal, health or reputation exposure |
| **Reversibility** | Undo within a day | Weeks of work to undo | Hard or impossible to undo |
| **Complexity** | One main factor | Several interacting factors | Many systems, people or domains |
| **Uncertainty** | One option is plausibly clear | A real tradeoff | Options are close, or key facts are unknown |

- **0–2: Direct.** Answer it yourself. Show the score in one line and offer: "Say 'full report' to dig deeper." A trigger phrase doesn't change this.
- **3–8: Decision report.** Continue below.
- **High stakes:** Stakes or Reversibility scored 2, or getting it wrong could cause material security, legal, safety or data-loss harm. High stakes allows a second researcher, or a red-team in its place (`research.md`). Everything else uses one researcher.

The user can override: "full report" forces a report; "just answer" forces Direct.

Tell the user the path in one line, for example:

> Decision report: hard to undo, real tradeoff. I'll check what could flip it, research it in parallel, and map the options.

## Find the deciders

A decider is a fact or assumption that, if it turned out differently, would change which option is right. Write 3–5 of them. Test each one: "If this were false, would I recommend something else?" If not, it isn't a decider; drop it.

Sort each decider:

| Kind | Examples | Who handles it |
|---|---|---|
| **Known well** | How a pattern works, standard tradeoffs, textbook principles, things that haven't changed in years | You, from knowledge. **No search.** |
| **Fresh or specific** | Anything that changes or is exact: current rates and prices, recent policy or rate changes, versions and their known issues, security advisories, a specific API's capabilities and limits, local laws and fees, current market conditions | Researchers (`research.md`) |
| **In the files** | Code structure, configs, dependency versions, the user's own data | You, before writing the report |
| **Only the user knows** | Their goals, timeline, obligations, risk tolerance, team skills, constraints they didn't state | Ask (below) |

The test for "fresh or specific": could your memory be out of date, or wrong in a detail that matters? In testing, every finding that would have prevented a costly mistake was of this kind: a rate change from that week, a 2026 security advisory, an email API lacking a feature the single answer assumed it had. Searching what you already know well costs tokens and finds nothing a single answer wouldn't say.

Rank the fresh deciders by how much they could flip the decision. Research goes deepest on the top one or two.

Also note what the user **didn't list**: an option, a constraint or a cost that the question takes for granted. Note it as a candidate for the report's "option you didn't list"; research decides whether it survives.

## Ask first

If any "only the user knows" decider would flip the answer, ask before researching. Asking is free; research is not, and it may be researching the wrong branch.

- **At most three questions**, in one message, each answerable in a sentence.
- Say in one line why you're asking: "These change the answer, so I'd rather ask than guess."
- Put the most decisive question first.
- Don't ask what you can look up or find in the files.
- If the user says "just decide" or doesn't answer: assume the most likely answer, say which assumption you made, and show in the report what changes if it's wrong.

## Choosing models (only where you can pick one per sub-agent)

| Role | Model |
|---|---|
| Researchers | Sonnet |
| Red-team (high stakes) | Opus |

Researchers mostly search and summarize, which a mid-tier model does well; the red-team's job is judgment. Every sub-agent pays a similar fixed token cost whatever the model, so a cheaper model saves through its price per token. The user can override.
