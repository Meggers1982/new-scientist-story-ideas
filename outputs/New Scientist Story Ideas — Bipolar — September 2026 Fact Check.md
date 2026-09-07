# Fact-Check Report: New Scientist Story Ideas — Bipolar — September 2026
**Checked:** 2026-09-07 | **Studies reviewed:** 11
**Publication:** New Scientist | **Section:** New Scientist Mind

---

### Study 1: Genes for addiction — not for drinking or smoking as such — explain why bipolar disorder and substance problems travel together
**PMID:** 42636965 | **Verdict:** ⚠️ Minor issues

**Issue A. "Why it matters" makes a claim the design cannot test** — Severity: Moderate

- **As written:** "It undercuts the intuitive story that people with bipolar disorder drink and smoke more because of the illness, and suggests instead an inherited liability specific to dependence"
- **Abstract says:** "By dissecting the genetic liability to SUD and SU and investigating their relationship with BIP we find a genetic signature correlated with substance dependence but not substance use more broadly."
- **Problem:** The study partitions shared genetic architecture; it does not test whether the illness itself drives increased consumption. Finding that shared genetics loads onto dependence rather than use does not "undercut" a behavioral, illness-driven pathway to heavier drinking or smoking — the two explanations can coexist.
- **Suggested fix:** "It suggests that what bipolar disorder shares genetically with substance problems is a liability to dependence rather than to consumption itself — a distinction that matters for how comorbidity is conceptualized and studied."

**Issue B. Causal language in the pitch angle contradicts the digest's own caveat** — Severity: Moderate

- **As written:** "then show how the genetics reverses the arrow"
- **Abstract says:** Polygenic overlap, genetic correlations, GWAS-by-subtraction and PRS associations — no directional or causal analysis (e.g. no Mendelian randomization) is reported.
- **Problem:** "Reverses the arrow" asserts a direction of causation. The caveats correctly state the work "cannot establish causation," so the pitch line contradicts the caveat.
- **Suggested fix:** "then show how the genetics complicates that story: the shared liability sits with dependence, not with consumption."

**Issue C. Overstated dissociation** — Severity: Minor

- **As written:** "the genetic variants nudging people toward *having a drink* are not the ones that link to bipolar disorder"
- **Abstract says:** "We found extensive polygenic overlap between traits, with SUDs being more genetically correlated with BIP than SU traits… The unique SUD factor correlated positively with psychiatric disorders, whereas unique SU correlated negatively."
- **Problem:** Substance-use traits were still genetically correlated with bipolar disorder, just less so, and the residual "unique use" factor correlated *negatively* with psychiatric disorders — which is a link, not an absence of one. "Not the ones that link" reads as zero overlap.
- **Suggested fix:** "the genetic variants nudging people toward *having a drink* are only weakly related to bipolar disorder — and once dependence liability is subtracted out, they point mildly in the opposite direction."

*Note:* The first name "Kevin" for O'Connell KS is unverifiable from the abstract alone (the abstract gives initials only).

---

### Study 2: Serotonin abnormality blamed on borderline personality disorder turns out to belong to depression
**PMID:** 42173043 | **Verdict:** ⚠️ Minor issues

**Issue A. NS fit score sits on a very small, post-hoc subgroup** — Severity: Minor

- **As written:** "**NS fit:** 7/10 — a neat reattribution of a well-known brain finding using rare PET data, though group sizes are modest."
- **Abstract says:** "comorbid BPD (n = 21)… the groups differed significantly in binding potential (BPF)… (F = 3.64; p = 0.03). Planned post-hoc analyses found that these differences… were driven by higher binding associated with mood disorder, and not with BPD."
- **Problem:** The central claim rests on a 21-person comorbid subgroup and a planned post-hoc contrast off a borderline primary result (p = 0.03 across 13 a priori regions). That is thin support for a 7, even with objective PET measurement.
- **Suggested fix:** "**NS fit:** 6/10 — a neat reattribution of a well-known brain finding using rare PET data, but the key contrast is post-hoc and the comorbid group is only 21 people."

**Issue B. Prescribing claim not in the abstract** — Severity: Minor

- **As written:** "Open on the clinical reality that most people diagnosed with borderline personality disorder are prescribed antidepressants that barely help."
- **Abstract says:** Only that SSRIs "are effective for mood disorders but have limited efficacy for BPD."
- **Problem:** The "most people… are prescribed" prevalence claim is Unverifiable from abstract only, and would need separate sourcing before it appears in a pitch.
- **Suggested fix:** "Open on the clinical puzzle that SSRIs, widely used in borderline personality disorder, show limited efficacy for it [sourcing needed for prescribing rates]."

---

### Study 3: More data beats smarter algorithms when predicting bipolar disorder in children
**PMID:** 42600789 | **Verdict:** ⚠️ Minor issues

**Issue A. "Direct evidence" overstates a hedged, within-study conclusion** — Severity: Moderate

- **As written:** "It is direct evidence that the bottleneck in psychiatric prediction is the diversity of data, not the sophistication of the model"
- **Abstract says:** "Within the present study, increasing model complexity did not improve external performance, whereas training on pooled data improved performance on held-out samples from the heterogeneous pooled cohort. These findings suggest that training-data diversity may provide greater practical benefit…"
- **Problem:** The authors twice hedge ("within the present study", "may provide"). Crucially, pooled training improved performance on held-out samples *from the pooled cohort* — not demonstrated cross-setting transfer — so "the bottleneck is diversity of data" is an inference, not a direct demonstration.
- **Suggested fix:** "Within these two datasets, added model complexity bought nothing externally, while training on pooled data helped on held-out samples from the combined cohort — which the authors read as evidence that data diversity may matter more than model sophistication."

**Issue B. Pitch hook rests on a comparison the abstract doesn't report** — Severity: Moderate

- **As written:** "a neural network was no better at spotting bipolar disorder in children than a questionnaire a parent fills in"
- **Abstract says:** "all models showed good internal discrimination in the academic dataset… Across models and training strategies, PGBI-10M was consistently identified as the most important predictor."
- **Problem:** Being the top-ranked predictor inside multivariable models is not the same as a head-to-head test of PGBI-10M alone against the multilayer perceptron. The abstract reports no such single-item-versus-deep-learning comparison.
- **Suggested fix:** "a deep-learning model did no better than a simple clinical nomogram or plain logistic regression, and in every model the single strongest predictor was a parent-completed questionnaire."

**Issue C. Direction of the generalization failure** — Severity: Minor

- **As written:** "All models performed well within the dataset they were trained on and dropped substantially when applied to the other setting… every model got worse the moment it left the clinic it was trained in"
- **Abstract says:** "all models showed good internal discrimination in the academic dataset, but external discrimination in the community dataset substantially declined."
- **Problem:** The abstract specifies one direction (academic → community). Whether the reverse transfer also degraded is Unverifiable from abstract only, so the bidirectional phrasing is unsupported.
- **Suggested fix:** "All models performed well in the academic dataset they were trained on, and discrimination dropped substantially when they were applied to the community clinic."

---

### Study 4: Most people with bipolar depression would not qualify for the trials that produced their treatment guidelines
**PMID:** 42575197 | **Verdict:** ⚠️ Minor issues

**Issue A. Composite-patient detail not sourced from the abstract** — Severity: Minor

- **As written:** "Open on a composite patient with the comorbidities — substance use, medical illness, suicidality — that get you excluded from trials."
- **Abstract says:** "The continuous TEI was associated with several psychiatric and medical characteristics in multivariable analysis."
- **Problem:** The specific exclusion drivers named (substance use, medical illness, suicidality) are not itemized in the abstract. Unverifiable from abstract only — plausible, but needs full text before it goes in a pitch.
- **Suggested fix:** "Open on a composite patient carrying the psychiatric and medical comorbidities that lowered TEI scores in this cohort [confirm specifics against full text]."

**Issue B. "Held across different eligibility thresholds" flattens a weak sensitivity result** — Severity: Minor

- **As written:** "a result that held across different eligibility thresholds"
- **Abstract says:** "Sensitivity analyses produced the same classification at a cutoff of 70 and preserved the direction of association at a cutoff of 80 (OR = 9.33, 95%CI 1.14–76.09; p = 0.013)."
- **Problem:** At the 80 cutoff the confidence interval runs from 1.14 to 76.09 — the direction survives but the estimate is extremely imprecise. "Held" implies robustness the numbers don't quite support.
- **Suggested fix:** "the direction of the effect survived at stricter and looser thresholds, though with much wider uncertainty at the strictest cutoff (OR = 9.33, 95% CI 1.14–76.09)."

---

### Study 5: Stimulating the balance organ changes how quickly you recognize your own face
**PMID:** 42276516 | **Verdict:** ⚠️ Minor issues

**Issue A. Scene-setting implies a subjective change that wasn't measured** — Severity: Minor

- **As written:** "unable to say why their own face suddenly feels no more special than a friend's"
- **Abstract says:** "under L-GVS RTs for self-faces no longer differ from those of familiar-other faces, effectively shifting the SA toward a more general familiarity advantage."
- **Problem:** The finding is a reaction-time equivalence in an explicit recognition task. No subjective or phenomenological report is described, so the "feels no more special" framing invents an experience the study didn't assess.
- **Suggested fix:** "unable to notice that their own face has stopped being the fastest one they recognize."

**Issue B. Study has no connection to the digest's stated focus** — Severity: Minor

- **As written:** "**Focus:** bipolar" (digest header) / "sinusoidal galvanic vestibular stimulation"
- **Abstract says:** "while receiving sinusoidal bipolar GVS or Sham stimulation."
- **Problem:** This paper appears to have entered a bipolar-focused screen via the electrode configuration term "bipolar GVS," not because it concerns bipolar disorder. Not a factual error in the write-up, but worth flagging so the section editor knows the entry is off-topic for the stated brief.
- **Suggested fix:** Retain only if the desk wants a standalone Mind item; otherwise drop from a bipolar-focused digest.

---

### Study 6: Two stages of treatment-resistant depression turn out to be two different conditions
**PMID:** 41904070 | **Verdict:** ⚠️ Minor issues

**Issue A. Headline overstates "two different conditions"** — Severity: Minor

- **As written:** "Two stages of treatment-resistant depression turn out to be two different conditions"
- **Abstract says:** "a simple two-stage TRD model differentiated a 'complex but responsive' subgroup (TRD1) from a more biologically refractory profile (TRD2)."
- **Problem:** The authors describe two clinical *profiles* within depression, distinguished by comorbidity burden and improvement trajectory. "Two different conditions" implies distinct nosological entities, which the data do not establish.
- **Suggested fix:** "Two stages of treatment-resistant depression look like two very different clinical profiles"

**Issue B. Prevalence figure doesn't match this cohort** — Severity: Minor

- **As written:** "'Treatment-resistant' is currently a single label attached to roughly a third of depressed patients"
- **Abstract says:** "TRD1 patients (24%)… TRD2 patients (29%)" — i.e. 53% of this inpatient cohort met one of the two TRD definitions.
- **Problem:** The "roughly a third" figure is a general literature estimate that sits awkwardly next to a study in which over half the sample was classified as treatment-resistant. Readers will assume the number comes from this paper.
- **Suggested fix:** "'Treatment-resistant' is currently a single label — one that covered more than half of this inpatient cohort (24% TRD1, 29% TRD2)."

*Note:* The digest's TRD definitions omit the "for ≥4 weeks" duration requirement in both tiers; not an error, but worth restoring if space allows.

---

### Study 7: Veterans with PTSD improve faster in borderline personality disorder therapy, not slower
**PMID:** 41084836 | **Verdict:** ✅ Accurate

No factual errors found. N (62), the probable/confirmed PTSD split (24 + 7 = 31), the VA setting, the null results for baseline severity and engagement, the steeper BPD symptom reductions, and the "clean diagnostic profiles (e.g. excluding bipolar disorder)" point all match the abstract. Framing is consistent, and the absence of a comparison arm is properly caveated.

---

### Study 8: Bipolar disorder and schizophrenia look identical in blood tests at the first psychotic episode
**PMID:** 42112712 | **Verdict:** ⚠️ Minor issues

**Issue A. Headline runs against the authors' own conclusion** — Severity: Minor

- **As written:** "Bipolar disorder and schizophrenia look identical in blood tests at the first psychotic episode"
- **Abstract says:** "No significant differences in blood cell counts or inflammatory markers were found between bipolar disorder and schizophrenia spectrum groups… Condition-specific findings, like decreased RBCs in bipolar disorder and eosinophils in schizophrenia, suggest unique early haematological profiles."
- **Problem:** The direct between-group comparison was null — so the headline is defensible — but the authors emphasize condition-specific profiles versus controls and conclude the opposite of "identical." The body text handles this fairly; the headline does not, and an editor should know the paper's own spin points the other way.
- **Suggested fix:** "Bipolar disorder and schizophrenia can't be told apart on routine blood tests at the first psychotic episode"

---

### Study 9: Shame about a bipolar diagnosis damages daily functioning through a specific route
**PMID:** 42113129 | **Verdict:** ⚠️ Minor issues

**Issue A. Self-esteem and social support were tested on a different relationship** — Severity: Moderate

- **As written:** "not through coping style, insight, self-esteem or social support, none of which mediated anything" / "self-esteem, social support and coping strategies all failed to buffer the effect of internalized stigma on functioning"
- **Abstract says:** "Stigma coping strategies and cognitive insight did not significantly mediate this relationship. Cognitive insight, self-esteem, or perceived social support did not exhibit a significant effect on the relationship between internalized stigma and coping strategies."
- **Problem:** Only coping strategies and cognitive insight were reported as non-mediators of the stigma→functioning path. Self-esteem and perceived social support were reported as having no effect on the stigma→*coping* relationship — a different model. The digest merges the two, and the pitch hook ("what *didn't* matter") depends on that merge.
- **Suggested fix:** "Mediation analysis showed the link between internalized stigma and poorer functioning ran specifically through perceived devaluation and discrimination — not through coping style or cognitive insight. Self-esteem, cognitive insight and social support were separately tested and did not shape the stigma–coping relationship either." Rework the pitch hook accordingly.

**Issue B. Causal headline for cross-sectional mediation** — Severity: Minor

- **As written:** "Shame about a bipolar diagnosis damages daily functioning through a specific route"
- **Abstract says:** "A cross-sectional study was conducted… Internalized stigma experienced by individuals with bipolar disorder negatively impacts functioning through a heightened perception of discrimination and devaluation."
- **Problem:** "Damages" asserts causation from cross-sectional mediation, contradicting the digest's own caveat that "mediation here is statistical, not causal." (The authors use similar language, but that doesn't license it in a headline.) Separately, "shame" is a loose gloss on internalized stigma, whose most elevated domains here were alienation and social withdrawal.
- **Suggested fix:** "Internalized stigma tracks poorer functioning in bipolar disorder — via one specific route"

---

### Study 10: Loading the dose of a long-acting antipsychotic upfront shortens hospital stays for women
**PMID:** 41924987 | **Verdict:** ⚠️ Minor issues

**Issue A. Causal headline for a retrospective, non-randomized cohort** — Severity: Moderate

- **As written:** "Loading the dose of a long-acting antipsychotic upfront shortens hospital stays for women"
- **Abstract says:** "This retrospective cohort study included 87 female inpatients… Aripiprazole monohydrate LAI initiation with the TIS regimen was associated with shorter hospitalization and more favorable rehospitalization outcomes."
- **Problem:** "Shortens" states cause. The authors say "was associated with," and the digest's own caveats note that clinicians chose the regimen, so allocation was likely confounded. The headline contradicts the caveat.
- **Suggested fix:** "A two-injection start for a long-acting antipsychotic is linked to shorter hospital stays in women"

**Issue B. Outcome variable renamed** — Severity: Minor

- **As written:** "and took longer to relapse when they did"
- **Abstract says:** "time to rehospitalization was longer (P = 0.027)."
- **Problem:** The measured outcome is time to rehospitalization, not relapse. Relapse without readmission would not be captured, so the substitution broadens the claim.
- **Suggested fix:** "and took longer to be readmitted when they were"

---

### Study 11: Memory circuits go wrong in different ways in schizophrenia and bipolar disorder
**PMID:** 42679550 | **Verdict:** ✅ Accurate

No factual errors found. The six long-axis seeds, the two contexts, the shared right mid-hippocampal hypoconnectivity, the schizophrenia-specific right posterior–inferior temporal gyrus hyperconnectivity, and the context-dependent right anterior pattern all match the abstract. The caveat that sample sizes are not reported in the abstract is appropriately honest, and the "participants almost certainly medicated" line is correctly presented as an assumption rather than a finding.

---

## Issue Summary

| Study # | Headline | Verdict | Notes |
|---------|----------|---------|-------|
| 1 | Genes for addiction… explain why bipolar disorder and substance problems travel together | ⚠️ Minor issues | Two moderate framing overreaches: "undercuts the illness-drives-drinking story" and "reverses the arrow"; also overstates absence of use–bipolar genetic link |
| 2 | Serotonin abnormality blamed on BPD turns out to belong to depression | ⚠️ Minor issues | NS fit 7 rests on n=21 post-hoc subgroup (suggest 6); prescribing claim unverifiable |
| 3 | More data beats smarter algorithms when predicting bipolar disorder in children | ⚠️ Minor issues | "Direct evidence" vs authors' "may suggest"; pitch's neural-net-vs-questionnaire comparison not reported; generalization failure was one-directional |
| 4 | Most people with bipolar depression would not qualify for the trials… | ⚠️ Minor issues | Named comorbidities unverifiable; sensitivity analysis less robust than "held" implies |
| 5 | Stimulating the balance organ changes how quickly you recognize your own face | ⚠️ Minor issues | Pitch implies unmeasured subjective change; study is off-topic for a bipolar-focused digest (matched on "bipolar GVS") |
| 6 | Two stages of treatment-resistant depression turn out to be two different conditions | ⚠️ Minor issues | "Two different conditions" overstates two profiles; "roughly a third" conflicts with 53% in this cohort |
| 7 | Veterans with PTSD improve faster in BPD therapy, not slower | ✅ Accurate | Cleared |
| 8 | Bipolar disorder and schizophrenia look identical in blood tests… | ⚠️ Minor issues | Null between-group result is real, but headline contradicts authors' "unique early haematological profiles" conclusion |
| 9 | Shame about a bipolar diagnosis damages daily functioning through a specific route | ⚠️ Minor issues | Self-esteem/social support were tested on the stigma–coping path, not stigma–functioning; causal headline |
| 10 | Loading the dose of a long-acting antipsychotic upfront shortens hospital stays for women | ⚠️ Minor issues | Causal headline for retrospective non-randomized cohort; "relapse" should be "rehospitalization" |
| 11 | Memory circuits go wrong in different ways in schizophrenia and bipolar disorder | ✅ Accurate | Cleared |

**Total issues:** 19 (13 Minor, 6 Moderate, 0 Major)
**Entries requiring revision:** 9
**Entries cleared:** 2