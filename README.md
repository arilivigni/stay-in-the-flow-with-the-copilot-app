# Stay in the Flow with the Copilot App

Build a supervised daily issue-triage automation without writing code.

## Welcome

- **Who this is for:** Product managers, scrum masters, program managers, content managers, and other GitHub collaborators.
- **What you'll learn:** Use Work IQ, Plan Mode, Canvas, local automations, and session history while keeping a human approval boundary.
- **What you'll build:** A daily assistant that summarizes new issues and recommends priorities and labels for review.
- **Prerequisites:** Access to the GitHub Copilot app, Work IQ, local automations, and permission to comment on and label issues in the copied repository.
- **How long:** About 45 minutes.

> [!IMPORTANT]
> The automation recommends actions. It must not silently apply labels, close issues, assign people, or publish workplace data.

## Start the exercise

1. Create a repository from this template.
2. Open **Actions** and run **Step 0** if setup does not start automatically.
3. Open **Exercise: Build your daily triage assistant** and follow its first instruction.

Setup is idempotent: rerunning Step 0 does not replace or duplicate exercise issues.

## Retry or reset

Edit the same marked learner comment after feedback. Corrected comments and labels are graded automatically. For a complete reset, create a fresh repository from the template.

## Responsible use

Only post sanitized planning criteria. Never paste credentials, private paths, customer information, restricted links, or raw workplace messages.

## Maintainer validation

Run `python3 .github/actions/grade-structured-block/grade.py --self-test`. In a fresh template copy, also run Step 0 twice, submit one incomplete block, and confirm the stable feedback comment is updated before a valid block advances the exercise.
