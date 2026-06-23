# Module 7 Week A — Integration Task: Domain-Shift Analysis

Apply your fine-tuned classifier (from Lab 7A, hosted on Hugging Face Hub) to the tech / entertainment news corpus and analyze the domain-shift behavior.

Full instructions: see the **Integration Task 7A guide** linked in TalentLMS.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env       # then edit MODEL_HUB_ID
make smoke                 # CI substitute model on 5-row fixture
make apply                 # your real model on full 1,033-row tech-news corpus
```

## TODO for learner — fill these in before submitting

- **Hugging Face Hub model URL:** https://huggingface.co/MrMarwans/m7-app-review-sentiment
- **Reproducibility command:** `cp .env.example .env` (set MODEL_HUB_ID), then `make apply`.
- **What the model was trained on and why we're applying it here:**

The model was trained in Lab 7A on 7,472 consumer app reviews across 9 mobile applications, predicting three sentiment classes: `negative`, `neutral`, and `positive`. The training data consists of short, opinionated texts written by users rating apps — reviewers either praise an app enthusiastically or complain about bugs and poor experience, with a smaller neutral class for mixed feedback.

In this integration task, we apply the same model to 1,033 tech and entertainment news articles from CNN. News prose is fundamentally different: it is written by journalists, uses formal language, describes events without personal opinion, and regularly covers negative events such as crime, arrests, and lawsuits in a neutral, descriptive tone. The gap between consumer micro-opinions and professional news reporting is exactly the domain shift we analyze in `domain-shift-analysis.md` — the goal is to understand where the model generalizes and where it breaks.

## Submission

Open a PR from `integration-7a-domain-shift` into `main`. Paste the PR URL into TalentLMS → Module 7 → Integration Task 7A.

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.