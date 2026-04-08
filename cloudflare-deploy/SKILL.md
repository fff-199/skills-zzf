---
name: cloudflare-deploy
description: Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services. Use when the user asks to deploy, host, publish, or set up a project on Cloudflare.
---

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

Not authenticated? â†?`references/wrangler/auth.md`
- Interactive/local: `wrangler login` (one-time OAuth)
- CI/CD: Set `CLOUDFLARE_API_TOKEN` env var

## Quick Decision Trees

### "I need to run code"

```
Need to run code?
â”œâ”€ Serverless functions at the edge â†?workers/
â”œâ”€ Full-stack web app with Git deploys â†?pages/
â”œâ”€ Stateful coordination/real-time â†?durable-objects/
â”œâ”€ Long-running multi-step jobs â†?workflows/
â”œâ”€ Run containers â†?containers/
â”œâ”€ Multi-tenant (customers deploy code) â†?workers-for-platforms/
â”œâ”€ Scheduled tasks (cron) â†?cron-triggers/
â”œâ”€ Lightweight edge logic (modify HTTP) â†?snippets/
â”œâ”€ Process Worker execution events (logs/observability) â†?tail-workers/
â””â”€ Optimize latency to backend infrastructure â†?smart-placement/
```

### "I need to store data"

```
Need storage?
â”œâ”€ Key-value (config, sessions, cache) â†?kv/
â”œâ”€ Relational SQL â†?d1/ (SQLite) or hyperdrive/ (existing Postgres/MySQL)
â”œâ”€ Object/file storage (S3-compatible) â†?r2/
â”œâ”€ Message queue (async processing) â†?queues/
â”œâ”€ Vector embeddings (AI/semantic search) â†?vectorize/
â”œâ”€ Strongly-consistent per-entity state â†?durable-objects/ (DO storage)
â”œâ”€ Secrets management â†?secrets-store/
â”œâ”€ Streaming ETL to R2 â†?pipelines/
â””â”€ Persistent cache (long-term retention) â†?cache-reserve/
```

### "I need AI/ML"

```
Need AI?
â”œâ”€ Run inference (LLMs, embeddings, images) â†?workers-ai/
â”œâ”€ Vector database for RAG/search â†?vectorize/
â”œâ”€ Build stateful AI agents â†?agents-sdk/
â”œâ”€ Gateway for any AI provider (caching, routing) â†?ai-gateway/
â””â”€ AI-powered search widget â†?ai-search/
```

### "I need networking/connectivity"

```
Need networking?
â”œâ”€ Expose local service to internet â†?tunnel/
â”œâ”€ TCP/UDP proxy (non-HTTP) â†?spectrum/
â”œâ”€ WebRTC TURN server â†?turn/
â”œâ”€ Private network connectivity â†?network-interconnect/
â”œâ”€ Optimize routing â†?argo-smart-routing/
â”œâ”€ Optimize latency to backend (not user) â†?smart-placement/
â””â”€ Real-time video/audio â†?realtimekit/ or realtime-sfu/
```

### "I need security"

```
Need security?
â”œâ”€ Web Application Firewall â†?waf/
â”œâ”€ DDoS protection â†?ddos/
â”œâ”€ Bot detection/management â†?bot-management/
â”œâ”€ API protection â†?api-shield/
â”œâ”€ CAPTCHA alternative â†?turnstile/
â””â”€ Credential leak detection â†?waf/ (managed ruleset)
```

### "I need media/content"

```
Need media?
â”œâ”€ Image optimization/transformation â†?images/
â”œâ”€ Video streaming/encoding â†?stream/
â”œâ”€ Browser automation/screenshots â†?browser-rendering/
â””â”€ Third-party script management â†?zaraz/
```

### "I need infrastructure-as-code"

```
Need IaC? â†?pulumi/ (Pulumi), terraform/ (Terraform), or api/ (REST API)
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
The deploy needs escalated network access to deploy to Cloudflare. I can rerun the command with escalated permissionsâ€”want me to proceed?
```
