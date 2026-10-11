> Example decision record produced by the skill, unedited, for a question asked inside [Outline](https://github.com/outline/outline) (commit 17ad514e1): *"A large self-hosted customer has about 3,000 concurrent editors and sees latency spikes in real-time collaboration. Should we split collaboration into its own service, scale it horizontally with Redis, or optimize it in-process?"* File and line references point into that commit.

# Scaling Outline real-time collaboration for 3,000 concurrent editors

**Date:** 2026-10-12 · **Verdict:** Recommendation · **Confidence:** Medium

## Question
A large self-hosted customer has about 3,000 concurrent editors and sees latency spikes in collaboration. The options are to split collaboration into its own service, to scale it horizontally with Redis, or to optimize it in-process. The user said "just decide".

## Verdict: Do both. Run collaboration as its own processes with Redis and routing by document id, using config that already exists, after a one-week measurement.

**Confidence:** Medium. The code facts are verified, but the cause of the spikes hasn't been measured yet.

Splitting the service and scaling with Redis are not competing projects. Outline already supports both through configuration. The real work is routing every connection for a document to the same instance, and then tuning whatever the measurements show.

### What we found that changes the picture
- Splitting needs no new code. `SERVICES` (env.ts:350-356) defaults to all four services in one process. `--services=collaboration` runs collaboration alone (server/collaboration/Procfile), and docs/SERVICES.md:33-45 documents this.
- Redis scaling is a switch that is off by default. The Hocuspocus Redis extension loads only when `REDIS_COLLABORATION_URL` is set (collaboration.ts:51-58).
- Redis alone is not safe at scale. With Redis on, a document can be live on several instances at once, and each one runs its own store. Each store encodes the document's full state (PersistenceExtension.ts:178-186), and the dirty and failure tracking is per process (26-29, 127-128). So routing every connection for a document to the same instance is mandatory. The document id is the last path segment of the URL (collaboration.ts:81-85), so a load balancer can route on it.
- The per-document connection cap is per process (ConnectionLimitExtension.ts:19, 60-63). Without document-id routing, the real cap becomes N times the configured value.
- Persistence writes editor attribution through the default Redis client, not the collaboration Redis (PersistenceExtension.ts:135, 197). That is a hidden shared dependency and a likely source of spikes.
- Hocuspocus is pinned at 1.1.3 (package.json:79-82). Save timing is debounce 3s and maxDebounce 10s (collaboration.ts:47-49).

### Blast radius
The change is deployment config only: the `SERVICES` env var, `REDIS_COLLABORATION_URL`, `COLLABORATION_URL`, and load-balancer rules. No source files change for steps 1–4. The in-process tuning step touches collaboration.ts and PersistenceExtension.ts.

### What we assumed about you
- The customer runs a single process or a few combined processes today. If they already split, skip to routing and measurement.
- Spikes come from load on one process: the event loop, the full-state encode on save, or DB locks. If a few huge documents with hundreds of editors cause them, horizontal scaling won't help, because one document stays on one instance. Then the in-process work (save cost, document size) becomes the main work.

### Decision map
| Option | Bets on | Cheapest test |
|---|---|---|
| Dedicated collaboration processes | Contention with web, worker and websockets causes the spikes | Set `--services=collaboration` on one node and compare p99 latency |
| Redis and N instances, routed by document | Load is spread over many documents | Count concurrent editors per document from the metrics |
| In-process optimization | Hot documents or the save path are the bottleneck | Profile the event loop and time onStoreDocument during a spike |
| Building a new service | Nothing. The service already exists | — |

### The option you didn't list
Upgrade Hocuspocus from 1.1.3. This is unverified: the changelogs were not checked. Treat it as a later candidate, not a fix.

### Will it last?
| Future change | Verdict | Why / breaking point |
|---|---|---|
| 10× editors (30k) | Extends | Add instances and scale Redis |
| One document with 500+ editors | Breaks | It stays on one instance, so per-document save cost is the limit |
| Second region | Breaks | Routing and Redis are single-region |
| More tenants on the same deployment | Absorbs | Routing by document spreads them |

**Foundation or quick fix:** Foundation for load spread across many documents. Hot single documents need the in-process work.

### Pre-mortem
- **Redis is on but routing isn't, and saves multiply.** Warning sign: DB write rate rises with the instance count. Check: day 1 after rollout.
- **Default Redis saturates from attribution writes.** Warning sign: default Redis latency rises during spikes. Check: during week 1 measurement.
- **Spikes continue because of hot documents.** Warning sign: p99 is concentrated on a few document ids. Check: week 1.

### Rollout
1. Week 1: aggregate MetricsExtension across instances (they are per instance, MetricsExtension.ts:52). Add event-loop lag, store duration and Redis latency. Find the top documents by editor count. Size: S.
2. Run 2+ processes with `--services=collaboration` and set `COLLABORATION_URL`. Size: S.
3. Set up a dedicated collaboration Redis via `REDIS_COLLABORATION_URL`, plus load-balancer hash routing on the document id. Size: S–M.
4. Scale out to N instances. As an estimate, start at about 300–500 connections per instance, so 6–10 instances for 3,000 editors. Tune from the metrics.
5. Do in-process work only if step 1 shows hot documents or slow saves: save cost, maxDebounce, attribution writes. Timebox: 2 weeks.

Exit criterion: p99 sync latency below target for 1 week, then stop.

### Next step
Ship the measurement this week. The cost of the per-document spread decides how much in-process work is needed.

## Plan
1–5 as in Rollout.

## Findings and sources
- All findings above come from the repository, with file:line references. They were verified by an independent code reviewer, who confirmed every ledger claim and added the routing, connection-cap, default-Redis and per-instance-metrics findings.
- Hocuspocus upgrade benefits: Not found (not researched).

## Audit
Gate score: stakes 2, reversibility 1, complexity 2, uncertainty 1, total 6, so a decision report. "Just decide" was given, so no questions were asked and the assumptions are shown above. The decision was in the files, so no web researcher was used. One code reviewer ran (Sonnet), and all of its MATERIAL findings were accepted.

Not read: client provider, websockets service, ViewsExtension, APIUpdateExtension internals.

---
<sub>Report: 1 code reviewer; 0 questions asked; 6 new findings</sub>
