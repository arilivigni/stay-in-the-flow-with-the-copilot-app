## Step 4: Configure the local automation

1. Create a daily local automation from the approved plan, restricted to new issues here.
2. If your environment exposes Work IQ through MCP, allow the automation to request a source type and sanitized planning signal only. Otherwise, reuse the sanitized Step 1 context.
3. Use the rubric to draft a summary, priority, topic label, rationale, and uncertainty note.
4. Send output to a review surface and prohibit unapproved repository changes.
5. Post only this attestation.

```text
<!-- step-4-automation:start -->
Schedule: daily
Scope: new issues in this exercise repository
Outputs: summary, priority, topic label, rationale, uncertainty
MCP boundary: sanitized Work IQ context only; no raw Microsoft 365 content
Review surface: <configured review surface>
Guardrail: recommendations only; no repository mutation without human approval
<!-- step-4-automation:end -->
```

> [!IMPORTANT]
> Do not paste credentials, private paths, workplace content, or an exported configuration.
