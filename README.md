# Stay in the Flow with the Copilot App

_Build a supervised daily issue-triage automation without writing code while keeping every repository change under human review._

## Welcome

- **Who is this for**: Product managers, scrum masters, program managers, content managers, and other GitHub collaborators.
- **What you'll learn**: Work IQ with Microsoft 365 sources, Plan Mode, Canvas, Automations, and session history, with clear MCP and human-approval boundaries.
- **What you'll build**: A daily assistant that summarizes new issues and recommends priorities and labels for review.
- **Prerequisites**:
  - Access to the GitHub Copilot app and Automations.
  - Permission to comment on and label issues in the copied repository.
  - Work IQ and Microsoft 365 tenant consent, or the included synthetic fallback.
- **How long**: Roughly **45 minutes**.

In this exercise, you will:

1. Establish safe triage context with Work IQ or synthetic data.
1. Plan a supervised daily issue-review workflow.
1. Build and test a priority rubric in Canvas.
1. Configure a recommendation-only Automation.
1. Review and approve one recommendation.
1. Summarize the completed workflow from session history.

> [!IMPORTANT]
> The automation recommends actions. It must not silently apply labels, close issues, assign people, or publish workplace data.

### How to start this exercise

Simply copy the exercise to your account, give your favorite Octocat (Mona) **about 20 seconds** to prepare the first lesson, then **refresh the page**.

[![Copy Exercise](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/new?template_owner=arilivigni&template_name=stay-in-the-flow-with-the-copilot-app&owner=%40me&name=skills-stay-in-the-flow-with-the-copilot-app&description=Exercise:+Stay+in+the+Flow+with+the+Copilot+App&visibility=public)

<details>
<summary>Having trouble? 🤷</summary><br/>

When copying the exercise, we recommend the following settings:

- For owner, choose your personal account or an organization to host the repository.
- We recommend creating a public repository, since private repositories will use Actions minutes.

If the exercise isn't ready in 20 seconds, check the [Actions](../../actions) tab. If no setup run appears, run **Step 0** manually.

- If a job is running, give Mona a little more time and refresh the page.
- If a job failed, open its logs for the actionable error and retry the run.

</details>

## Retry or reset

Edit the same marked learner comment after feedback. Corrected comments and labels are graded automatically. For a complete reset, create a fresh repository from the template.

## Responsible use

Only post sanitized planning criteria. Never paste credentials, private paths, customer information, restricted links, or raw content from Teams, Outlook, meetings, or Microsoft 365 documents.

## Maintainer validation

Step workflows reuse `skills/exercise-toolkit` (`start-exercise`, `find-exercise-issue`, `finish-exercise`) plus the shared step-feedback templates, and delegate answer checks to the `grade-structured-block` action.

Run `python3 .github/actions/grade-structured-block/grade.py --self-test`. In a fresh template copy, confirm setup starts automatically, an untouched answer fails with actionable feedback in the shared results table, and a valid answer advances exactly once.

---

&copy; 2026 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)
