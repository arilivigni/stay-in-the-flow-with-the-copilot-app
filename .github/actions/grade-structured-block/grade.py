#!/usr/bin/env python3
import argparse,re,sys
P={"P1","P2","P3"}; T={"onboarding","reliability","documentation","question"}
M={1:"step-1-context",2:"step-2-plan",3:"step-3-rubric",4:"step-4-automation",5:"step-5-approval",6:"step-6-summary"}
R={1:["priority","rationale","microsoft 365 source","source type","work iq attempted"],2:["schedule","scope","outputs","approval"],3:["p1","p2","p3","allowed labels","human check"],4:["schedule","scope","outputs","mcp boundary","review surface","guardrail"],5:["decision","evidence","rubric rule","human reviewer"],6:["automation","context","skill or agent","microsoft 365 source","mcp boundary","human review","future automation"]}
def result(ok,msg): print(msg.replace("\n"," ")); return 0 if ok else 1
def grade(step,text,labels="",issue=""):
 m=re.search(rf"<!--\s*{M[step]}:start\s*-->(.*?)<!--\s*{M[step]}:end\s*-->",text,re.I|re.S)
 if not m:return result(False,f"Add the Step {step} start and end markers to one comment, then retry.")
 c=m.group(1).strip(); d={k.strip().lower():v.strip() for k,v in re.findall(r"^([^:\n]+):\s*(.+)$",c,re.M)}; low=c.lower()
 for key in R[step]:
  if not d.get(key):return result(False,f"Add a non-empty `{key.title()}` field to the marked block.")
 if step in (1,4) and re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|-----begin [^-]+ private key-----|https?://[^\s/@]+:[^\s/@]+@",c,re.I):return result(False,"Remove and rotate the likely credential, then edit the same comment. The value is not repeated here.")
 if step==1:
  if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b|\b\d{3}[-. ]\d{3}[-. ]\d{4}\b",c):return result(False,"Remove personal contact information and use generic context.")
  if not any(x in d["work iq attempted"].lower() for x in ("yes","attempted","blocked")):return result(False,"Record that Work IQ was attempted or access was blocked.")
  if not any(x in d["microsoft 365 source"].lower() for x in ("teams","outlook","meeting","document","synthetic")):return result(False,"Name an allowed Microsoft 365 source type or the synthetic fallback.")
 if step==2:
  for term,desc in [("daily","daily schedule"),("new","new-issue scope"),("summary","summary output"),("priority","priority recommendation"),("label","label recommendation"),("human","human approval")]:
   if term not in low:return result(False,f"Revise the plan to include {desc}.")
 if step==3:
  bad={x.strip().lower() for x in d["allowed labels"].split(",")}-T
  if bad:return result(False,f"Remove unsupported label `{sorted(bad)[0]}`.")
 if step==4:
  for term,desc in [("daily","daily schedule"),("new","new-issue scope"),("summary","summary output"),("priority","priority output"),("label","label output"),("human","human approval")]:
   if term not in low:return result(False,f"Update the attestation to include {desc}.")
  if not any(x in d["guardrail"].lower() for x in ("without human","recommendations only","approval")):return result(False,"Prohibit repository mutation without human approval.")
  if not any(x in d["mcp boundary"].lower() for x in ("sanitized","read-only","no raw","synthetic")):return result(False,"Limit the MCP boundary to sanitized, read-only, or synthetic context.")
 if step==5:
  chosen=P.intersection(labels.split())
  if len(chosen)!=1:return result(False,"Apply exactly one priority label: P1, P2, or P3.")
  if "approved" not in d["human reviewer"].lower():return result(False,"Set `Human reviewer` to `approved` after review.")
  words=[w for w in re.findall(r"[a-z]{5,}",d["evidence"].lower()) if w not in {"issue","evidence","because"}]
  if issue and not any(w in issue.lower() for w in words):return result(False,"Cite specific evidence from the seeded issue body.")
 if step==6:
  for term,desc in [("daily","daily triage automation"),("context","sanitized context"),("human","human review"),("approval","future approval point")]:
   if term not in low:return result(False,f"Revise the summary to mention {desc}.")
  if "work iq" not in d["skill or agent"].lower():return result(False,"Identify Work IQ as the skill or agent used.")
  if not any(x in d["microsoft 365 source"].lower() for x in ("teams","outlook","meeting","document","synthetic")):return result(False,"Name the Microsoft 365 source type or synthetic fallback.")
  if not any(x in d["mcp boundary"].lower() for x in ("sanitized","read-only","no raw","synthetic","least privilege")):return result(False,"Describe how the MCP boundary limited workplace content.")
 return result(True,f"Step {step} passed. Continue with the next instruction.")
def selftest():
 s={1:"Priority: reliability\nRationale: launch\nMicrosoft 365 source: Teams\nSource type: planning update\nWork IQ attempted: yes",2:"Schedule: daily\nScope: new issues\nOutputs: summary priority label\nApproval: human approval",3:"P1: blocker\nP2: significant\nP3: routine\nAllowed labels: onboarding\nHuman check: evidence",4:"Schedule: daily\nScope: new issues\nOutputs: summary priority label\nMCP boundary: sanitized context only\nReview surface: app\nGuardrail: recommendations only with human approval",5:"Decision: P1\nEvidence: signup confirmation blocks onboarding\nRubric rule: blocker\nHuman reviewer: approved",6:"Automation: daily triage\nContext: sanitized context\nSkill or agent: Work IQ\nMicrosoft 365 source: Teams\nMCP boundary: sanitized context only\nHuman review: completed\nFuture automation: weekly digest with approval"}
 for n,b in s.items():
  if grade(n,f"<!-- {M[n]}:start -->\n{b}\n<!-- {M[n]}:end -->","P1" if n==5 else "","signup confirmation blocks onboarding"):return 1
 print("All grader self-tests passed.");return 0
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--step",type=int);a.add_argument("--body-file");a.add_argument("--labels",default="");a.add_argument("--issue-body-file",default="");a.add_argument("--self-test",action="store_true");x=a.parse_args()
 if x.self_test:sys.exit(selftest())
 if not x.step or not x.body_file:a.error("--step and --body-file are required")
 body=open(x.body_file,encoding="utf-8").read();issue=open(x.issue_body_file,encoding="utf-8").read() if x.issue_body_file else "";sys.exit(grade(x.step,body,x.labels,issue))
