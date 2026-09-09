# Fact-Check Report: New Scientist Story Ideas — Artificial Intelligence — September 2026
**Checked:** 2026-09-09 | **Studies reviewed:** 15
**Publication:** New Scientist | **Section:** New Scientist Mind

---

# Fact-Check Report — New Scientist Mind digest, run date 2026-09-09

### Study 1: People feel less judged when comfort comes from a machine than from another human
**PMID:** 42691276 | **Verdict:** ✅ Accurate

No factual errors found. N (3,341), study count (six studies, five preregistered, plus pilot), the two distinct mediating pathways (lower fear of negative evaluation → well-being; expectation-exceeding empathy → perceived support effectiveness), and the mix of simulated and real interactions all match the abstract. Framing is consistent: the "expectations may rise" extension in *Why it matters* is explicitly speculative ("could evaporate"), and the caveats correctly limit the claim to minor aversive events. NS fit of 8/10 is defensible for six mostly preregistered experimental studies with a large total N.

---

### Study 2: ChatGPT spots eating disorders that human clinicians miss in higher-weight patients
**PMID:** 42068161 | **Verdict:** ⚠️ Minor issues

All numbers check out: 100%/100%/90% identification by weight condition vs 47%/21%/16% for clinicians; 100% specialist-care recommendation vs 35%/19%/17%; 20 prompt administrations per vignette; Gemini-3 and Claude-4.5 replication; conflict of interest correctly disclosed.

**Issue A. Absolute claim about absence of bias** — Severity: Minor

- **As written:** "here the language models simply did not show it — a rare case of AI looking less prejudiced than the professionals"
- **Abstract says:** "showing little evidence of common biases observed in human samples"
- **Problem:** The abstract's claim is "little evidence," not "none," and ChatGPT's own numbers do drop slightly at higher weight (100% → 90%). "Simply did not show it" hardens a hedged conclusion.
- **Suggested fix:** "here the language models showed little sign of it — a rare case of AI looking less prejudiced than the professionals"

**Issue B. NS fit score slightly high for the design** — Severity: Minor

- **As written:** "NS fit: 8/10 — a clean benchmark against published human data showing AI lacked the weight bias clinicians displayed"
- **Abstract says:** Two vignettes, 20 prompt administrations each, compared against *previously published* clinician and community benchmark data.
- **Problem:** The comparison is historical rather than head-to-head, the stimulus set is two vignettes, and no real patients are involved. That is a striking result but a thin, uncontrolled evidence base for an 8.
- **Suggested fix:** "NS fit: 7/10 — striking benchmark result, but two vignettes against previously published human data rather than a head-to-head comparison"

---

### Study 3: The people most likely to accept an AI therapist are the ones who struggle most with human relationships
**PMID:** 41549774 | **Verdict:** ⚠️ Minor issues

N=1,612, Prolific recruitment, the three cluster labels, the direction of the effect (both vulnerable clusters higher AI acceptance; Secure-trusting-healthy lowest AI / highest teletherapy), and the therapy-experience finding all match.

**Issue A. "Denying" overstates a hypothesized cost** — Severity: Minor

- **As written:** "while denying them the relational repair that psychotherapy is partly thought to work through"
- **Abstract says:** "those vulnerable people might also miss out on the relational learning that takes place in human-based therapies"
- **Problem:** The abstract offers this as a possibility ("might also miss out"); "denying" asserts it as an established consequence, which cross-sectional acceptance data cannot show.
- **Suggested fix:** "while potentially leaving them without the relational learning that psychotherapy is partly thought to work through"

**Issue B. NS fit score on cross-sectional, hypothetical self-report** — Severity: Minor

- **As written:** "NS fit: 7/10 — large sample and a genuinely paradoxical pattern"
- **Abstract says:** Cluster analysis of survey data measuring acceptance of AI-based interventions versus teletherapy; no uptake or outcome data.
- **Problem:** Every variable — symptoms, attachment, epistemic trust, acceptance — is self-reported at one time point, and the outcome is a hypothetical preference. A 7 is generous for that; the sample size is the only real strength.
- **Suggested fix:** "NS fit: 6/10 — large sample and a genuinely paradoxical pattern, but entirely cross-sectional self-report measuring hypothetical acceptance"

---

### Study 4: Describing your mood in your own words predicts sick leave better than a questionnaire does
**PMID:** 40974258 | **Verdict:** ⚠️ Minor issues

Development N=963, prospective N=145, the four response formats, the Sequential Evaluation with Model Pre-Registration design, r = .60–.79, and the 9-of-12 external validity comparison are all accurate. The founder conflict of interest is correctly flagged.

**Issue A. Headline converts "higher or equal" into "better"** — Severity: Minor

- **As written:** "Describing your mood in your own words predicts sick leave better than a questionnaire does"
- **Abstract says:** "the text-format yielded the strongest correlations (being higher/equal to rating scales for 9 of 12 cases)"
- **Problem:** The finding is that free text matched or beat rating scales in 9 of 12 comparisons, against *self-reported* sick leave and healthcare visits — not that it outperformed them outright. The body text gets this right; the headline does not.
- **Suggested fix:** "Describing your mood in your own words matches or beats a questionnaire at tracking self-reported sick leave"

**Issue B. Sub-sample claim not in the abstract** — Severity: Minor

- **As written:** "Prospective validation sample under 100 for some comparisons (N=145 overall)"
- **Abstract says:** Only "a prospective sample (N = 145)."
- **Problem:** The claim that some comparisons rested on fewer than 100 participants is unverifiable from abstract only.
- **Suggested fix:** "Prospective validation sample of 145; per-comparison sample sizes not reported in the abstract"

---

### Study 5: Asking an AI to summarize medical notes destroys the information needed to predict violence
**PMID:** 42671866 | **Verdict:** ⚠️ Minor issues

Case/control counts (277 events, 2,758 matched controls), site, date range, F1 and AUROC values, the ranking of Llama-3.1-8B and MedGemma-27B below Clinical-Longformer, poor zero-shot performance, and the mental-health-flag subgroup finding all match.

**Issue A. "Destroys" overstates the size of the drop** — Severity: Moderate

- **As written:** "Asking an AI to summarize medical notes destroys the information needed to predict violence"
- **Abstract says:** "Replacing original notes with general or entity-guided summaries reduced performance (F1 = 0.465 and 0.510)"; "Summaries of clinical notes may compress or alter cues needed for discrimination"
- **Problem:** Performance fell substantially but summaries retained meaningful discriminative signal (F1 ≈ 0.47–0.51). "Destroys" is hype language for a hedged "may compress or alter," and the body's "slashed" compounds it.
- **Suggested fix:** "Asking an AI to summarise medical notes strips out much of the signal needed to predict violence" — and in the body, "cut performance sharply (F1 = 0.465 and 0.510)"

---

### Study 6: Psychopathy predicts who will use generative AI to bully people, six months in advance
**PMID:** 42374878 | **Verdict:** ✅ Accurate

No factual errors found. N=1,019, two waves, six-month interval, Dark Tetrad measures, the psychopathy-and-male-gender result surviving control for baseline behavior, sadism dropping to nonsignificance, and null effects for Machiavellianism, narcissism and age all match the abstract. The *Why it matters* inference ("a familiar population handed a more powerful tool") is appropriately hedged with "suggests," and the caveats correctly note self-report and the two-wave design. NS fit of 6/10 is defensible.

---

### Study 7: A home video of a toddler at play, plus machine learning, flags autism with 91% accuracy
**PMID:** 42695515 | **Verdict:** ⚠️ Significant issues

N=170, age range 16–30 months, ICC = 0.87, AUC/sensitivity/specificity of 0.91, and RF outperforming total-score and logistic regression approaches all match.

**Issue A. Pitch implies no specialist input is needed** — Severity: Moderate

- **As written:** "The hook is how little material is needed — a short phone video of a parent and child playing, no clinic, no specialist."
- **Abstract says:** "Parent-child interaction videos were recorded at home and subsequently coded using the SCS scheme"; "Trained coders then reviewed the videos and assessed the child's early social communication behaviors"
- **Problem:** The machine learning operated on human-coded SCS items plus demographics — not on the raw video. A trained coder is still required, so "no specialist" misdescribes the pipeline, and the headline's "plus machine learning" invites readers to imagine automated video analysis. This is the kind of assumption a pitch would collapse under.
- **Suggested fix:** "The hook is how little material is needed — a short phone video of a parent and child playing, scored remotely by a trained coder, with no clinic visit."

**Issue B. "Flags autism with 91% accuracy"** — Severity: Minor

- **As written:** "flags autism with 91% accuracy"
- **Abstract says:** "Autism likelihood (Elevated vs. Low) was defined using the ADOS-2 classifications"; "AUC = 0.91; sensitivity = 0.91; specificity = 0.91"; "Further validation ... against clinical diagnoses is needed"
- **Problem:** The model classified ADOS-2-defined *elevated versus low likelihood*, not diagnosed autism, and AUC 0.91 is not "accuracy." The caveats acknowledge the diagnosis point, but the headline does not.
- **Suggested fix:** "A home video of a toddler at play, plus machine learning, flags elevated autism likelihood with 91% sensitivity and specificity"

---

### Study 8: Giving students an AI tutor does nothing much — unless you teach them how to study with it
**PMID:** 42600450 | **Verdict:** ⚠️ Significant issues

N=266, industrial engineering undergraduates at a Chinese university, seven weeks, class-level assignment, the SRL scaffold components, the vocabulary and enjoyment results, and the low-baseline-enjoyment moderation all match.

**Issue A. Claims an AI-versus-no-AI comparison the study never made** — Severity: Moderate

- **As written:** "Giving students an AI tutor does nothing much" / "Lead with the control group: students given free access to AI learned no more and enjoyed it no more than before."
- **Abstract says:** Students were "assigned at the class level to an experimental group receiving the SRL intervention or a control group using AI autonomously"; the control group "showed no significant change" in enjoyment.
- **Problem:** Both arms used AI — there is no non-AI comparison group, so nothing here can show that AI access "does nothing much" for learning. The enjoyment half of the claim is supported (no significant pre-post change in the control group); the "learned no more" half is not: the abstract reports only that the control group scored lower than the intervention group at post-test, not that it failed to improve.
- **Suggested fix:** Headline: "An AI tutor only helps if you teach students how to study with it." Pitch: "Lead with the control group: students left to use the same AI tools on their own scored lower on the vocabulary post-test and showed no significant lift in enjoyment. Note that both groups used AI — the study isolates the pedagogy, not the tool, and cannot say what AI adds over no AI at all."

---

### Study 9: ChatGPT's abortion advice is usually acceptable and almost never complete
**PMID:** 40550012 | **Verdict:** ✅ Accurate

No factual errors found. Ten fact-based and ten clinical-scenario questions, ChatGPT-3.5, three complex family planning physician graders, the acceptable/unacceptable and complete/incomplete rubric, the ACOG/SFP/PubMed benchmarks, 65% acceptable and 8% complete, and fact-based questions outperforming clinical ones all match. The caveats correctly flag the tiny question set, the outdated model version, and the judgment-based outcomes, and the pitch avoids treating chatbot output as clinical advice.

---

### Study 10: Chatbots are becoming part of how teenagers form an identity — and nobody is tracking it
**PMID:** 42664282 | **Verdict:** ⚠️ Minor issues

The developmental-task framing, the listed benefits, the call for longitudinal, use-case-specific, youth-involved research, and the "review, not primary research" caveat all match.

**Issue A. Pitch sets aside a risk the paper actually lists** — Severity: Minor

- **As written:** "the question is not whether chatbots expose teenagers to bad content but whether they quietly do the developmental work"
- **Abstract says:** "Risks include increasing social isolation, undermining distress tolerance, distorting expectations for human relationships, compromising identity and purpose development, **and exposing youth to biased, inaccurate, or sexually inappropriate content**"
- **Problem:** The digest's risk list swaps "increasing social isolation" for "displaced developmental experiences" and drops inappropriate-content exposure entirely, then the pitch frames content exposure as the wrong question. The authors treat it as one risk among several, so the reframe is sharper than the paper.
- **Suggested fix:** "the question is not only whether chatbots expose teenagers to bad content — a risk the authors also flag — but whether they quietly do the developmental work"

---

### Study 11: AI helps you generate more ideas — and makes everyone's ideas look the same
**PMID:** 42705114 | **Verdict:** ⚠️ Minor issues

The outcome/process distinction, the four moderators (timing, interaction design, task characteristics, user expertise), and the list of costs (homogenization, authenticity and ownership, independent engagement, team collaboration) all match. The caveat correctly identifies it as a narrative review.

**Issue A. "Reliably" and "every writer" harden a hedged review claim** — Severity: Minor

- **As written:** "Generative AI reliably increases the number of ideas" / "Lead on the paradox: every writer gets better ideas"
- **Abstract says:** "While GenAI **can** increase the number of ideas, enhance idea quality, accelerate idea generation, and reduce cognitive load, it **may also** lead to idea homogenization..."
- **Problem:** The review reports conditional effects moderated by four factors — that is the paper's central point — so "reliably" and "every writer" contradict the abstract's own framing.
- **Suggested fix:** "Generative AI can increase the number of ideas..." / "Lead on the paradox: AI can lift any one person's idea output, while the pool of ideas across people narrows"

---

### Study 12: Telling epilepsy patients about the risk of sudden death does not appear to harm them
**PMID:** 42673770 | **Verdict:** ⚠️ Minor issues

Date range, 23,584 authors screened, 1,381 posts by 789 individuals, the discovery-through-own-searching finding, the emotional reactions, the betrayal-and-mistrust link to absent counseling, and the protective-behavior associations all match. The Semalytix employment conflict is correctly disclosed for three authors.

**Issue A. Novelty label misdescribes what is being contradicted** — Severity: Minor

- **As written:** "Novelty: Overturns prior research"
- **Abstract says:** "Despite clinicians' reluctance to discuss SUDEP due to fear of increasing patient anxiety, this study shows that knowledge about SUDEP may lead to proactive risk management without long-term emotional harm."
- **Problem:** The paper contradicts a *clinical practice norm*, not a body of published findings, and it does so with unsolicited online posts. "Overturns prior research" oversells the evidential status.
- **Suggested fix:** "Novelty: Challenges current clinical practice"

**Issue B. Causal verbs in Why it matters** — Severity: Minor

- **As written:** "the withholding is what damages trust, while the knowledge drives protective behavior"
- **Abstract says:** "Lack of counseling ... was linked to feelings of betrayal and mistrust"; "Knowledge about SUDEP promoted adherence ... and use of preventive tools"
- **Problem:** These are associations inferred from self-selected public posts. "Damages" and "drives" read as demonstrated causation, and the body text's more careful "was associated with" is undercut.
- **Suggested fix:** "patients' own accounts link the withholding to lost trust, and knowledge to more protective behaviour"

---

### Study 13: Machine learning can guess who will still be depressed after eating disorder treatment — but not who will fail to improve
**PMID:** 42117565 | **Verdict:** ⚠️ Minor issues

N=1,412, inpatient/day-hospital setting, elastic net and extreme gradient boosting, AUC 0.64–0.65 for nonimprovement versus 0.73–0.77 for residual depression, the important predictors, and the "substantial portion still notably depressed" conclusion all match.

**Issue A. Omits the decision curve analysis, which softens the "failure" frame** — Severity: Minor

- **As written:** "a preregistered, transparently reported partial failure in a field prone to overclaiming"
- **Abstract says:** "Decision curve analysis indicated that **all models** provided greater net benefit than treating all or no patients across clinically relevant thresholds."
- **Problem:** The authors report that even the poorly discriminating nonimprovement models offered net clinical benefit over treat-all/treat-none strategies. Leaving that out makes the result sound like a flat null and would leave a writer exposed if a reviewer raised it.
- **Suggested fix:** Add to the body: "Decision curve analysis nonetheless found all models offered greater net benefit than treating all or no patients across clinically relevant thresholds."

---

### Study 14: When AI helps you choose dinner, the values being optimized may not be yours
**PMID:** 42705481 | **Verdict:** ✅ Accurate

No factual errors found. The advisor → decision partner → ambient influence continuum, the four named mechanisms (preference offloading, responsibility reallocation, confidence calibration, food-decision skill erosion), the compounding argument grounded in frequent habitual eating decisions, and the draw on consumer psychology, automation research and cognitive science all match. The caveats correctly state that boundary conditions remain untested in food contexts and that there are no empirical results. NS fit of 4/10 for a conceptual review is appropriately modest.

---

### Study 15: Negotiating through a screen — or an AI — makes it easier not to notice you are behaving badly
**PMID:** 42697057 | **Verdict:** ⚠️ Minor issues

The ethical fading definition, the three proposed processes (psychological distance, cognitive offloading, displaced accountability), the technologies covered, and the authors' own statement that the evidence base is limited all match.

**Issue A. Specific tactics attributed to the paper** — Severity: Minor

- **As written:** "Together, these are argued to make misrepresentation and hardball tactics feel like technical choices rather than ethical ones."
- **Abstract says:** "we explore the impact that technology and AI have on ethical fading and unethical negotiating behavior"
- **Problem:** The abstract refers generically to "unethical negotiating behavior"; the specific naming of misrepresentation and hardball tactics is unverifiable from abstract only.
- **Suggested fix:** "Together, these are argued to make unethical negotiating behaviour feel like a technical choice rather than an ethical one."

---

## Issue Summary

| Study # | Headline | Verdict | Notes |
|---------|----------|---------|-------|
| 1 | People feel less judged when comfort comes from a machine | ✅ Accurate | N, design, both mediation pathways verified |
| 2 | ChatGPT spots eating disorders clinicians miss | ⚠️ Minor issues | "Simply did not show it" hardens "little evidence"; NS fit 8 → 7 |
| 3 | People most likely to accept an AI therapist | ⚠️ Minor issues | "Denying" overstates "might miss out"; NS fit 7 → 6 |
| 4 | Own words predict sick leave better than a questionnaire | ⚠️ Minor issues | Headline turns "higher/equal in 9 of 12" into "better"; sub-sample caveat unverifiable |
| 5 | AI summaries destroy violence-prediction information | ⚠️ Minor issues | "Destroys" is hype for a substantial-but-partial performance drop |
| 6 | Psychopathy predicts generative-AI bullying | ✅ Accurate | All trait findings and controls verified |
| 7 | Home video plus machine learning flags autism | ⚠️ Significant issues | ML ran on human-coded SCS items, so "no specialist" misdescribes pipeline; outcome is ADOS-2 likelihood, not diagnosis |
| 8 | AI tutor does nothing much without study training | ⚠️ Significant issues | Both arms used AI; no non-AI control supports "learned no more" |
| 9 | ChatGPT's abortion advice acceptable, rarely complete | ✅ Accurate | 65%/8%, model version and grader design verified |
| 10 | Chatbots and teenage identity formation | ⚠️ Minor issues | Pitch sidelines the inappropriate-content risk the authors list |
| 11 | AI generates more ideas, homogenizes them | ⚠️ Minor issues | "Reliably" / "every writer" contradict the review's conditional framing |
| 12 | Telling epilepsy patients about SUDEP risk | ⚠️ Minor issues | Novelty label overreaches; causal verbs for social-listening associations |
| 13 | ML predicts residual depression, not nonimprovement | ⚠️ Minor issues | Omits decision curve analysis showing net benefit for all models |
| 14 | AI as dinner decision partner | ✅ Accurate | Continuum and four mechanisms verified; caveats appropriate |
| 15 | Screens and AI enable ethical fading | ⚠️ Minor issues | Named tactics unverifiable from abstract |

**Total issues:** 16 (13 Minor, 3 Moderate, 0 Major)
**Entries requiring revision:** 11
**Entries cleared:** 4