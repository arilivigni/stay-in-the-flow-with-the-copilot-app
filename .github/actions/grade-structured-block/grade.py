#!/usr/bin/env python3
import argparse
import re
import sys

PRIORITIES = {"P1", "P2", "P3"}
TOPIC_LABELS = {"onboarding", "reliability", "documentation", "question"}
MARKERS = {
    1: "step-1-context",
    2: "step-2-plan",
    3: "step-3-rubric",
    4: "step-4-automation",
    5: "step-5-approval",
    6: "step-6-summary",
}
REQUIRED_FIELDS = {
    1: ["priority", "rationale", "microsoft 365 source", "source type", "work iq attempted"],
    2: ["schedule", "scope", "outputs", "approval"],
    3: ["p1", "p2", "p3", "allowed labels", "human check"],
    4: ["schedule", "scope", "outputs", "mcp boundary", "review surface", "guardrail"],
    5: ["decision", "evidence", "rubric rule", "human reviewer"],
    6: ["automation", "context", "skill or agent", "microsoft 365 source", "mcp boundary", "human review", "future automation"],
}


def result(ok, message):
    print(message.replace("\n", " "))
    return 0 if ok else 1


def grade(step, text, labels="", issue=""):
    match = re.search(
        rf"<!--\s*{MARKERS[step]}:start\s*-->(.*?)<!--\s*{MARKERS[step]}:end\s*-->",
        text,
        re.I | re.S,
    )
    if not match:
        return result(False, f"Add the Step {step} start and end markers to one comment, then retry.")

    content = match.group(1).strip()
    if re.search(r"<[^>\n]+>", content):
        return result(False, "Replace every angle-bracket placeholder with your own exercise result, then retry.")

    fields = {
        key.strip().lower(): value.strip()
        for key, value in re.findall(r"^([^:\n]+):\s*(.+)$", content, re.M)
    }
    lower_content = content.lower()
    for key in REQUIRED_FIELDS[step]:
        if not fields.get(key):
            return result(False, f"Add a non-empty `{key.title()}` field to the marked block.")

    if step in (1, 4) and re.search(
        r"gh[pousr]_[A-Za-z0-9]{20,}|-----begin [^-]+ private key-----|https?://[^\s/@]+:[^\s/@]+@",
        content,
        re.I,
    ):
        return result(False, "Remove and rotate the likely credential, then edit the same comment. The value is not repeated here.")

    if step == 1:
        if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b|\b\d{3}[-. ]\d{3}[-. ]\d{4}\b", content):
            return result(False, "Remove personal contact information and use generic context.")
        if not any(value in fields["work iq attempted"].lower() for value in ("yes", "attempted", "blocked")):
            return result(False, "Record that Work IQ was attempted or access was blocked.")
        if not any(value in fields["microsoft 365 source"].lower() for value in ("teams", "outlook", "meeting", "document", "synthetic")):
            return result(False, "Name an allowed Microsoft 365 source type or the synthetic fallback.")

    if step == 2:
        for term, description in [
            ("daily", "daily schedule"),
            ("new", "new-issue scope"),
            ("summary", "summary output"),
            ("priority", "priority recommendation"),
            ("label", "label recommendation"),
            ("human", "human approval"),
        ]:
            if term not in lower_content:
                return result(False, f"Revise the plan to include {description}.")

    if step == 3:
        unsupported = {value.strip().lower() for value in fields["allowed labels"].split(",")} - TOPIC_LABELS
        if unsupported:
            return result(False, f"Remove unsupported label `{sorted(unsupported)[0]}`.")

    if step == 4:
        for term, description in [
            ("daily", "daily schedule"),
            ("new", "new-issue scope"),
            ("summary", "summary output"),
            ("priority", "priority output"),
            ("label", "label output"),
            ("human", "human approval"),
        ]:
            if term not in lower_content:
                return result(False, f"Update the attestation to include {description}.")
        if not any(value in fields["guardrail"].lower() for value in ("without human", "recommendations only", "approval")):
            return result(False, "Prohibit repository mutation without human approval.")
        if not any(value in fields["mcp boundary"].lower() for value in ("sanitized", "read-only", "no raw", "synthetic")):
            return result(False, "Limit the MCP boundary to sanitized, read-only, or synthetic context.")

    if step == 5:
        chosen = PRIORITIES.intersection(labels.split())
        if len(chosen) != 1:
            return result(False, "Apply exactly one priority label: P1, P2, or P3.")
        selected = next(iter(chosen))
        if selected.lower() not in fields["decision"].lower():
            return result(False, f"Include the selected `{selected}` priority in the `Decision` field.")
        if "approved" not in fields["human reviewer"].lower():
            return result(False, "Set `Human reviewer` to `approved` after review.")

        issue_lower = issue.lower()
        expected = None
        if "blocks onboarding" in issue_lower or ("signup" in issue_lower and "prevent" in issue_lower):
            expected = "P1"
        elif "can continue" in issue_lower and ("clarification" in issue_lower or "checklist" in issue_lower):
            expected = "P3"
        if not expected:
            return result(False, "Review one of the supplied seeded issues so its expected priority can be checked.")
        if selected != expected:
            return result(False, f"The seeded issue evidence matches `{expected}`, not `{selected}`. Recheck the rubric and label.")

        ignored = {"because", "evidence", "issue", "report", "specific", "synthetic", "users"}
        evidence_words = {
            word for word in re.findall(r"[a-z]{5,}", fields["evidence"].lower()) if word not in ignored
        }
        issue_words = set(re.findall(r"[a-z]{5,}", issue_lower))
        if len(evidence_words.intersection(issue_words)) < 2:
            return result(False, "Cite at least two specific details from the seeded issue body.")
        rule = fields["rubric rule"].lower()
        if expected == "P1" and "block" not in rule:
            return result(False, "Connect the P1 decision to the rubric's blocker condition.")
        if expected == "P3" and not any(value in rule for value in ("routine", "question", "clarif")):
            return result(False, "Connect the P3 decision to the rubric's routine or question condition.")

    if step == 6:
        for term, description in [
            ("daily", "daily triage automation"),
            ("context", "sanitized context"),
            ("human", "human review"),
            ("approval", "future approval point"),
        ]:
            if term not in lower_content:
                return result(False, f"Revise the summary to mention {description}.")
        if "work iq" not in fields["skill or agent"].lower():
            return result(False, "Identify Work IQ as the skill or agent used.")
        if not any(value in fields["microsoft 365 source"].lower() for value in ("teams", "outlook", "meeting", "document", "synthetic")):
            return result(False, "Name the Microsoft 365 source type or synthetic fallback.")
        if not any(value in fields["mcp boundary"].lower() for value in ("sanitized", "read-only", "no raw", "synthetic", "least privilege")):
            return result(False, "Describe how the MCP boundary limited workplace content.")

    return result(True, f"Step {step} passed. Continue with the next instruction.")


def selftest():
    valid = {
        1: "Priority: reliability\nRationale: launch\nMicrosoft 365 source: Teams\nSource type: planning update\nWork IQ attempted: yes",
        2: "Schedule: daily\nScope: new issues\nOutputs: summary priority label\nApproval: human approval",
        3: "P1: blocker\nP2: significant\nP3: routine\nAllowed labels: onboarding\nHuman check: evidence",
        4: "Schedule: daily\nScope: new issues\nOutputs: summary priority label\nMCP boundary: sanitized context only\nReview surface: app\nGuardrail: recommendations only with human approval",
        5: "Decision: P1 reliability\nEvidence: signup confirmation blocks onboarding\nRubric rule: launch blocker\nHuman reviewer: approved",
        6: "Automation: daily triage\nContext: sanitized context\nSkill or agent: Work IQ\nMicrosoft 365 source: Teams\nMCP boundary: sanitized context only\nHuman review: completed\nFuture automation: weekly digest with approval",
    }
    issue = "Synthetic report: Signup confirmation fails and blocks onboarding for affected users."
    for step, body in valid.items():
        text = f"<!-- {MARKERS[step]}:start -->\n{body}\n<!-- {MARKERS[step]}:end -->"
        if grade(step, text, "P1" if step == 5 else "", issue):
            return 1

    placeholder = "<!-- step-1-context:start -->\nPriority: reliability\nRationale: <reason>\nMicrosoft 365 source: Teams\nSource type: update\nWork IQ attempted: yes\n<!-- step-1-context:end -->"
    if grade(1, placeholder) == 0:
        print("Placeholder answer unexpectedly passed.")
        return 1

    wrong_priority = valid[5].replace("P1 reliability", "P3 reliability")
    wrong_text = f"<!-- step-5-approval:start -->\n{wrong_priority}\n<!-- step-5-approval:end -->"
    if grade(5, wrong_text, "P3", issue) == 0:
        print("Incorrect seeded priority unexpectedly passed.")
        return 1

    print("All grader self-tests passed.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", type=int)
    parser.add_argument("--body-file")
    parser.add_argument("--labels", default="")
    parser.add_argument("--issue-body-file", default="")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(selftest())
    if not args.step or not args.body_file:
        parser.error("--step and --body-file are required")
    body = open(args.body_file, encoding="utf-8").read()
    issue_body = open(args.issue_body_file, encoding="utf-8").read() if args.issue_body_file else ""
    sys.exit(grade(args.step, body, args.labels, issue_body))
