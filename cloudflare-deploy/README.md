# cloudflare-deploy

Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services. Use when the user asks to deploy, host, publish, or set up a project on Cloudflare.

## Portable Entry Point

- Start here if you are using this repository from a non-Codex agent.
- The original Codex-oriented source remains in `SKILL.md` for reference.
- Run bundled scripts relative to this folder, for example `./cloudflare-deploy/scripts/...` from the repo root.

## Adapted Instructions

# Cloudflare Deploy

Consolidated skill for building on the Cloudflare platform. Use decision trees below to find the right product, then load detailed references.

## Prerequisites

- When sandboxing blocks the deployment network calls, rerun with `sandbox_permissions=require_escalated`.
- The deployment might take a few minutes. Use appropriate timeout values.

## Authentication (Required Before Deploy)

Verify auth before `wrangler deploy`, `wrangler pages deploy`, or `npm run deploy`:

```bash
npx wrangler whoami    # Shows account if authenticated
```

Not authenticated? 鈫?`references/wrangler/auth.md`
- Interactive/local: `wrangler login` (one-time OAuth)
- CI/CD: Set `CLOUDFLARE_API_TOKEN` env var

## Quick Decision Trees

### "I need to run code"

```
Need to run code?
鈹溾攢 Serverless functions at the edge 鈫?workers/
鈹溾攢 Full-stack web app with Git deploys 鈫?pages/
鈹溾攢 Stateful coordination/real-time 鈫?durable-objects/
鈹溾攢 Long-running multi-step jobs 鈫?workflows/
鈹溾攢 Run containers 鈫?containers/
鈹溾攢 Multi-tenant (customers deploy code) 鈫?workers-for-platforms/
鈹溾攢 Scheduled tasks (cron) 鈫?cron-triggers/
鈹溾攢 Lightweight edge logic (modify HTTP) 鈫?snippets/
鈹溾攢 Process Worker execution events (logs/observability) 鈫?tail-workers/
鈹斺攢 Optimize latency to backend infrastructure 鈫?smart-placement/
```

### "I need to store data"

```
Need storage?
鈹溾攢 Key-value (config, sessions, cache) 鈫?kv/
鈹溾攢 Relational SQL 鈫?d1/ (SQLite) or hyperdrive/ (existing Postgres/MySQL)
鈹溾攢 Object/file storage (S3-compatible) 鈫?r2/
鈹溾攢 Message queue (async processing) 鈫?queues/
鈹溾攢 Vector embeddings (AI/semantic search) 鈫?vectorize/
鈹溾攢 Strongly-consistent per-entity state 鈫?durable-objects/ (DO storage)
鈹溾攢 Secrets management 鈫?secrets-store/
鈹溾攢 Streaming ETL to R2 鈫?pipelines/
鈹斺攢 Persistent cache (long-term retention) 鈫?cache-reserve/
```

### "I need AI/ML"

```
Need AI?
鈹溾攢 Run inference (LLMs, embeddings, images) 鈫?workers-ai/
鈹溾攢 Vector database for RAG/search 鈫?vectorize/
鈹溾攢 Build stateful AI agents 鈫?agents-sdk/
鈹溾攢 Gateway for any AI provider (caching, routing) 鈫?ai-gateway/
鈹斺攢 AI-powered search widget 鈫?ai-search/
```

### "I need networking/connectivity"

```
Need networking?
鈹溾攢 Expose local service to internet 鈫?tunnel/
鈹溾攢 TCP/UDP proxy (non-HTTP) 鈫?spectrum/
鈹溾攢 WebRTC TURN server 鈫?turn/
鈹溾攢 Private network connectivity 鈫?network-interconnect/
鈹溾攢 Optimize routing 鈫?argo-smart-routing/
鈹溾攢 Optimize latency to backend (not user) 鈫?smart-placement/
鈹斺攢 Real-time video/audio 鈫?realtimekit/ or realtime-sfu/
```

### "I need security"

```
Need security?
鈹溾攢 Web Application Firewall 鈫?waf/
鈹溾攢 DDoS protection 鈫?ddos/
鈹溾攢 Bot detection/management 鈫?bot-management/
鈹溾攢 API protection 鈫?api-shield/
鈹溾攢 CAPTCHA alternative 鈫?turnstile/
鈹斺攢 Credential leak detection 鈫?waf/ (managed ruleset)
```

### "I need media/content"

```
Need media?
鈹溾攢 Image optimization/transformation 鈫?images/
鈹溾攢 Video streaming/encoding 鈫?stream/
鈹溾攢 Browser automation/screenshots 鈫?browser-rendering/
鈹斺攢 Third-party script management 鈫?zaraz/
```

### "I need infrastructure-as-code"

```
Need IaC? 鈫?pulumi/ (Pulumi), terraform/ (Terraform), or api/ (REST API)
```

## Product Index

### Compute & Runtime
| Product | Reference |
|---------|-----------|
| Workers | `references/workers/` |
| Pages | `references/pages/` |
| Pages Functions | `references/pages-functions/` |
| Durable Objects | `references/durable-objects/` |
| Workflows | `references/workflows/` |
| Containers | `references/containers/` |
| Workers for Platforms | `references/workers-for-platforms/` |
| Cron Triggers | `references/cron-triggers/` |
| Tail Workers | `references/tail-workers/` |
| Snippets | `references/snippets/` |
| Smart Placement | `references/smart-placement/` |

### Storage & Data
| Product | Reference |
|---------|-----------|
| KV | `references/kv/` |
| D1 | `references/d1/` |
| R2 | `references/r2/` |
| Queues | `references/queues/` |
| Hyperdrive | `references/hyperdrive/` |
| DO Storage | `references/do-storage/` |
| Secrets Store | `references/secrets-store/` |
| Pipelines | `references/pipelines/` |
| R2 Data Catalog | `references/r2-data-catalog/` |
| R2 SQL | `references/r2-sql/` |

### AI & Machine Learning
| Product | Reference |
|---------|-----------|
| Workers AI | `references/workers-ai/` |
| Vectorize | `references/vectorize/` |
| Agents SDK | `references/agents-sdk/` |
| AI Gateway | `references/ai-gateway/` |
| AI Search | `references/ai-search/` |

### Networking & Connectivity
| Product | Reference |
|---------|-----------|
| Tunnel | `references/tunnel/` |
| Spectrum | `references/spectrum/` |
| TURN | `references/turn/` |
| Network Interconnect | `references/network-interconnect/` |
| Argo Smart Routing | `references/argo-smart-routing/` |
| Workers VPC | `references/workers-vpc/` |

### Security
| Product | Reference |
|---------|-----------|
| WAF | `references/waf/` |
| DDoS Protection | `references/ddos/` |
| Bot Management | `references/bot-management/` |
| API Shield | `references/api-shield/` |
| Turnstile | `references/turnstile/` |

### Media & Content
| Product | Reference |
|---------|-----------|
| Images | `references/images/` |
| Stream | `references/stream/` |
| Browser Rendering | `references/browser-rendering/` |
| Zaraz | `references/zaraz/` |

### Real-Time Communication
| Product | Reference |
|---------|-----------|
| RealtimeKit | `references/realtimekit/` |
| Realtime SFU | `references/realtime-sfu/` |

### Developer Tools
| Product | Reference |
|---------|-----------|
| Wrangler | `references/wrangler/` |
| Miniflare | `references/miniflare/` |
| C3 | `references/c3/` |
| Observability | `references/observability/` |
| Analytics Engine | `references/analytics-engine/` |
| Web Analytics | `references/web-analytics/` |
| Sandbox | `references/sandbox/` |
| Workerd | `references/workerd/` |
| Workers Playground | `references/workers-playground/` |

### Infrastructure as Code
| Product | Reference |
|---------|-----------|
| Pulumi | `references/pulumi/` |
| Terraform | `references/terraform/` |
| API | `references/api/` |

### Other Services
| Product | Reference |
|---------|-----------|
| Email Routing | `references/email-routing/` |
| Email Workers | `references/email-workers/` |
| Static Assets | `references/static-assets/` |
| Bindings | `references/bindings/` |
| Cache Reserve | `references/cache-reserve/` |

## Troubleshooting

### Escalated Network Access

If deployment fails due to network issues (timeouts, DNS errors, connection resets), rerun the deploy with escalated permissions (use `sandbox_permissions=require_escalated`). The deploy requires escalated network access when sandbox networking blocks outbound requests.

Example guidance to the user:

```
The deploy needs escalated network access to deploy to Cloudflare. I can rerun the command with escalated permissions鈥攚ant me to proceed?
```

## Resource Map

### References
- `references/agents-sdk/api.md`
- `references/agents-sdk/configuration.md`
- `references/agents-sdk/gotchas.md`
- `references/agents-sdk/patterns.md`
- `references/agents-sdk/README.md`
- `references/ai-gateway/configuration.md`
- `references/ai-gateway/dynamic-routing.md`
- `references/ai-gateway/features.md`
- `references/ai-gateway/README.md`
- `references/ai-gateway/sdk-integration.md`
- `references/ai-gateway/troubleshooting.md`
- `references/ai-search/api.md`
- `references/ai-search/configuration.md`
- `references/ai-search/gotchas.md`
- `references/ai-search/patterns.md`
- `references/ai-search/README.md`
- `references/analytics-engine/api.md`
- `references/analytics-engine/configuration.md`
- `references/analytics-engine/gotchas.md`
- `references/analytics-engine/patterns.md`
- `references/analytics-engine/README.md`
- `references/api/api.md`
- `references/api/configuration.md`
- `references/api/gotchas.md`
- `references/api/patterns.md`
- `references/api/README.md`
- `references/api-shield/api.md`
- `references/api-shield/configuration.md`
- `references/api-shield/gotchas.md`
- `references/api-shield/patterns.md`
- `references/api-shield/README.md`
- `references/argo-smart-routing/api.md`
- `references/argo-smart-routing/configuration.md`
- `references/argo-smart-routing/gotchas.md`
- `references/argo-smart-routing/patterns.md`
- `references/argo-smart-routing/README.md`
- `references/bindings/api.md`
- `references/bindings/configuration.md`
- `references/bindings/gotchas.md`
- `references/bindings/patterns.md`
- `references/bindings/README.md`
- `references/bot-management/api.md`
- `references/bot-management/configuration.md`
- `references/bot-management/gotchas.md`
- `references/bot-management/patterns.md`
- `references/bot-management/README.md`
- `references/browser-rendering/api.md`
- `references/browser-rendering/configuration.md`
- `references/browser-rendering/gotchas.md`
- `references/browser-rendering/patterns.md`
- `references/browser-rendering/README.md`
- `references/c3/api.md`
- `references/c3/configuration.md`
- `references/c3/gotchas.md`
- `references/c3/patterns.md`
- `references/c3/README.md`
- `references/cache-reserve/api.md`
- `references/cache-reserve/configuration.md`
- `references/cache-reserve/gotchas.md`
- `references/cache-reserve/patterns.md`
- `references/cache-reserve/README.md`
- `references/containers/api.md`
- `references/containers/configuration.md`
- `references/containers/gotchas.md`
- `references/containers/patterns.md`
- `references/containers/README.md`
- `references/cron-triggers/api.md`
- `references/cron-triggers/configuration.md`
- `references/cron-triggers/gotchas.md`
- `references/cron-triggers/patterns.md`
- `references/cron-triggers/README.md`
- `references/d1/api.md`
- `references/d1/configuration.md`
- `references/d1/gotchas.md`
- `references/d1/patterns.md`
- `references/d1/README.md`
- `references/ddos/api.md`
- `references/ddos/configuration.md`
- `references/ddos/gotchas.md`
- `references/ddos/patterns.md`
- `references/ddos/README.md`
- `references/do-storage/api.md`
- `references/do-storage/configuration.md`
- `references/do-storage/gotchas.md`
- `references/do-storage/patterns.md`
- `references/do-storage/README.md`
- `references/do-storage/testing.md`
- `references/durable-objects/api.md`
- `references/durable-objects/configuration.md`
- `references/durable-objects/gotchas.md`
- `references/durable-objects/patterns.md`
- `references/durable-objects/README.md`
- `references/email-routing/api.md`
- `references/email-routing/configuration.md`
- `references/email-routing/gotchas.md`
- `references/email-routing/patterns.md`
- `references/email-routing/README.md`
- `references/email-workers/api.md`
- `references/email-workers/configuration.md`
- `references/email-workers/gotchas.md`
- `references/email-workers/patterns.md`
- `references/email-workers/README.md`
- `references/hyperdrive/api.md`
- `references/hyperdrive/configuration.md`
- `references/hyperdrive/gotchas.md`
- `references/hyperdrive/patterns.md`
- `references/hyperdrive/README.md`
- `references/images/api.md`
- `references/images/configuration.md`
- `references/images/gotchas.md`
- `references/images/patterns.md`
- `references/images/README.md`
- `references/kv/api.md`
- `references/kv/configuration.md`
- `references/kv/gotchas.md`
- `references/kv/patterns.md`
- `references/kv/README.md`
- `references/miniflare/api.md`
- `references/miniflare/configuration.md`
- `references/miniflare/gotchas.md`
- `references/miniflare/patterns.md`
- `references/miniflare/README.md`
- `references/network-interconnect/api.md`
- `references/network-interconnect/configuration.md`
- `references/network-interconnect/gotchas.md`
- `references/network-interconnect/patterns.md`
- `references/network-interconnect/README.md`
- `references/observability/api.md`
- `references/observability/configuration.md`
- `references/observability/gotchas.md`
- `references/observability/patterns.md`
- `references/observability/README.md`
- `references/pages/api.md`
- `references/pages/configuration.md`
- `references/pages/gotchas.md`
- `references/pages/patterns.md`
- `references/pages/README.md`
- `references/pages-functions/api.md`
- `references/pages-functions/configuration.md`
- `references/pages-functions/gotchas.md`
- `references/pages-functions/patterns.md`
- `references/pages-functions/README.md`
- `references/pipelines/api.md`
- `references/pipelines/configuration.md`
- `references/pipelines/gotchas.md`
- `references/pipelines/patterns.md`
- `references/pipelines/README.md`
- `references/pulumi/api.md`
- `references/pulumi/configuration.md`
- `references/pulumi/gotchas.md`
- `references/pulumi/patterns.md`
- `references/pulumi/README.md`
- `references/queues/api.md`
- `references/queues/configuration.md`
- `references/queues/gotchas.md`
- `references/queues/patterns.md`
- `references/queues/README.md`
- `references/r2/api.md`
- `references/r2/configuration.md`
- `references/r2/gotchas.md`
- `references/r2/patterns.md`
- `references/r2/README.md`
- `references/r2-data-catalog/api.md`
- `references/r2-data-catalog/configuration.md`
- `references/r2-data-catalog/gotchas.md`
- `references/r2-data-catalog/patterns.md`
- `references/r2-data-catalog/README.md`
- `references/r2-sql/api.md`
- `references/r2-sql/configuration.md`
- `references/r2-sql/gotchas.md`
- `references/r2-sql/patterns.md`
- `references/r2-sql/README.md`
- `references/realtime-sfu/api.md`
- `references/realtime-sfu/configuration.md`
- `references/realtime-sfu/gotchas.md`
- `references/realtime-sfu/patterns.md`
- `references/realtime-sfu/README.md`
- `references/realtimekit/api.md`
- `references/realtimekit/configuration.md`
- `references/realtimekit/gotchas.md`
- `references/realtimekit/patterns.md`
- `references/realtimekit/README.md`
- `references/sandbox/api.md`
- `references/sandbox/configuration.md`
- `references/sandbox/gotchas.md`
- `references/sandbox/patterns.md`
- `references/sandbox/README.md`
- `references/secrets-store/api.md`
- `references/secrets-store/configuration.md`
- `references/secrets-store/gotchas.md`
- `references/secrets-store/patterns.md`
- `references/secrets-store/README.md`
- `references/smart-placement/api.md`
- `references/smart-placement/configuration.md`
- `references/smart-placement/gotchas.md`
- `references/smart-placement/patterns.md`
- `references/smart-placement/README.md`
- `references/snippets/api.md`
- `references/snippets/configuration.md`
- `references/snippets/gotchas.md`
- `references/snippets/patterns.md`
- `references/snippets/README.md`
- `references/spectrum/api.md`
- `references/spectrum/configuration.md`
- `references/spectrum/gotchas.md`
- `references/spectrum/patterns.md`
- `references/spectrum/README.md`
- `references/static-assets/api.md`
- `references/static-assets/configuration.md`
- `references/static-assets/gotchas.md`
- `references/static-assets/patterns.md`
- `references/static-assets/README.md`
- `references/stream/api-live.md`
- `references/stream/api.md`
- `references/stream/configuration.md`
- `references/stream/gotchas.md`
- `references/stream/patterns.md`
- `references/stream/README.md`
- `references/tail-workers/api.md`
- `references/tail-workers/configuration.md`
- `references/tail-workers/gotchas.md`
- `references/tail-workers/patterns.md`
- `references/tail-workers/README.md`
- `references/terraform/api.md`
- `references/terraform/configuration.md`
- `references/terraform/gotchas.md`
- `references/terraform/patterns.md`
- `references/terraform/README.md`
- `references/tunnel/api.md`
- `references/tunnel/configuration.md`
- `references/tunnel/gotchas.md`
- `references/tunnel/networking.md`
- `references/tunnel/patterns.md`
- `references/tunnel/README.md`
- `references/turn/api.md`
- `references/turn/configuration.md`
- `references/turn/gotchas.md`
- `references/turn/patterns.md`
- `references/turn/README.md`
- `references/turnstile/api.md`
- `references/turnstile/configuration.md`
- `references/turnstile/gotchas.md`
- `references/turnstile/patterns.md`
- `references/turnstile/README.md`
- `references/vectorize/api.md`
- `references/vectorize/configuration.md`
- `references/vectorize/gotchas.md`
- `references/vectorize/patterns.md`
- `references/vectorize/README.md`
- `references/waf/api.md`
- `references/waf/configuration.md`
- `references/waf/gotchas.md`
- `references/waf/patterns.md`
- `references/waf/README.md`
- `references/web-analytics/configuration.md`
- `references/web-analytics/gotchas.md`
- `references/web-analytics/integration.md`
- `references/web-analytics/patterns.md`
- `references/web-analytics/README.md`
- `references/workerd/api.md`
- `references/workerd/configuration.md`
- `references/workerd/gotchas.md`
- `references/workerd/patterns.md`
- `references/workerd/README.md`
- `references/workers/api.md`
- `references/workers/configuration.md`
- `references/workers/frameworks.md`
- `references/workers/gotchas.md`
- `references/workers/patterns.md`
- `references/workers/README.md`
- `references/workers-ai/api.md`
- `references/workers-ai/configuration.md`
- `references/workers-ai/gotchas.md`
- `references/workers-ai/patterns.md`
- `references/workers-ai/README.md`
- `references/workers-for-platforms/api.md`
- `references/workers-for-platforms/configuration.md`
- `references/workers-for-platforms/gotchas.md`
- `references/workers-for-platforms/patterns.md`
- `references/workers-for-platforms/README.md`
- `references/workers-playground/api.md`
- `references/workers-playground/configuration.md`
- `references/workers-playground/gotchas.md`
- `references/workers-playground/patterns.md`
- `references/workers-playground/README.md`
- `references/workers-vpc/api.md`
- `references/workers-vpc/configuration.md`
- `references/workers-vpc/gotchas.md`
- `references/workers-vpc/patterns.md`
- `references/workers-vpc/README.md`
- `references/workflows/api.md`
- `references/workflows/configuration.md`
- `references/workflows/gotchas.md`
- `references/workflows/patterns.md`
- `references/workflows/README.md`
- `references/wrangler/api.md`
- `references/wrangler/auth.md`
- `references/wrangler/configuration.md`
- `references/wrangler/gotchas.md`
- `references/wrangler/patterns.md`
- `references/wrangler/README.md`
- `references/zaraz/api.md`
- `references/zaraz/configuration.md`
- `references/zaraz/gotchas.md`
- `references/zaraz/IMPLEMENTATION_SUMMARY.md`
- `references/zaraz/patterns.md`
- `references/zaraz/README.md`

### Assets
- `assets/cloudflare-small.svg`
- `assets/cloudflare.png`

## Source

- Original skill definition: `SKILL.md`
