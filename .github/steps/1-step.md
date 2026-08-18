## Step 1: Establish safe triage context

Every safe automation starts with a clear data boundary. You will reduce workplace context to a source type and sanitized planning signal before anything reaches GitHub.

### 📖 Theory: minimize context before automation

Work IQ can provide useful planning context, but an issue tracker is not the place for raw workplace content. Keep only what the triage decision needs, and use the synthetic fallback when access is unavailable.

### ⌨️ Activity: establish safe triage context

1. In Work IQ, choose one Microsoft 365 source: a Teams conversation, Outlook email thread, meeting, or planning document.
2. Ask: `Find one recent planning signal about the onboarding launch. Return only a one-sentence summary and the source type. Do not quote people, include names, or return links.`
3. Remove names, identifiers, private quotations, restricted links, customer details, and unsupported claims.
4. Comment on this tracking issue with the block below. If Work IQ or tenant consent is unavailable, use `.github/exercise/synthetic-planning-brief.md` and record the synthetic fallback.

```text
<!-- step-1-context:start -->
Priority: onboarding reliability
Rationale: <sanitized reason>
Microsoft 365 source: <Teams, Outlook, meeting, document, or synthetic fallback>
Source type: <planning update or synthetic planning brief>
Work IQ attempted: yes
<!-- step-1-context:end -->
```

> [!NOTE]
> Work IQ may run as a Copilot skill or through its MCP server. In either case, bring only the sanitized result into this repository.

> [!TIP]
> Edit this same marked comment when retrying.
