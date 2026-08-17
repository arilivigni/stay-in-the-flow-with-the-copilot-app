## Step 4: Configure the local automation

1. Create a daily local automation from the approved plan, restricted to new issues here.
2. Use the rubric to draft a summary, priority, topic label, rationale, and uncertainty note.
3. Send output to a review surface and prohibit unapproved repository changes.
4. Post only this attestation.

```text
<!-- step-4-automation:start -->
Schedule: daily
Scope: new issues in this exercise repository
Outputs: summary, priority, topic label, rationale, uncertainty
Review surface: <configured review surface>
Guardrail: recommendations only; no repository mutation without human approval
<!-- step-4-automation:end -->
```

> [!IMPORTANT]
> Do not paste credentials, private paths, workplace content, or an exported configuration.
