# Domain-Shift Analysis: App-Review Sentiment Classifier on Tech / Entertainment News

## Prediction distribution

| Label | Count |
|---|---|
| positive | 202 |
| neutral | 398 |
| negative | 433 |

## Confidence distribution

| Metric | Value |
|---|---|
| Mean predicted probability | 0.6159 |
| Median predicted probability | 0.5840 |
| Proportion with probability > 0.9 | 3.7% (~38 articles) |
| Proportion with probability < 0.6 | 53.6% (~554 articles) |

The model is only moderately confident on average, with a median below 0.6 — meaning more than half of all predictions fall in the low-confidence range. This is a strong signal of domain shift: on in-domain app reviews, confidence was concentrated in the 0.75–0.95 range. Here, over 53% of predictions fall below 0.6, reflecting genuine uncertainty when processing news prose that does not resemble consumer reviews.

## Five qualitative examples

### Example 1

- **Article ID:** NEWS_0035
- **Excerpt:** "Buy a $175,000 package to attend the Oscars and you might buy yourself trouble, lawyers for the Academy Awards warn..."
- **Predicted label:** negative — **0.905**
- **Interpretation:** Clearly wrong. This is a factual legal advisory piece with no sentiment — it warns consumers about ticket scams. The model latches onto words like "trouble" and "lawyers" and fires a high-confidence negative prediction. This exposes a systematic pattern: legal and warning language in news maps directly onto the complaint vocabulary of one-star app reviews, producing over-confident wrong predictions.

### Example 2

- **Article ID:** NEWS_0073
- **Excerpt:** "Impeached former Illinois Gov. Rod Blagojevich... was indicted Thursday on 16 felony counts by a federal grand jury..."
- **Predicted label:** negative — **0.917**
- **Interpretation:** Arguably correct, but for the wrong reasons. This is genuinely bad news, yet the model is confident because it pattern-matches on "arrested," "conspiracy," and "fraud" the same way it would respond to a one-star app review. The model has no understanding of political or legal context — it reads journalistic crime reporting as consumer complaint language.

### Example 3

- **Article ID:** NEWS_0004
- **Excerpt:** "Forbes' list of the world's wealthy has named Warren Buffett the richest person on the planet, surpassing his friend Bill Gates..."
- **Predicted label:** neutral — **0.398**
- **Interpretation:** Correct prediction, but extremely unconfident at 0.398 — barely above random. The article is a straightforward factual news item with no sentiment. This exposes the model's inability to recognize factual neutrality as a stable class: it hedges correctly but for the wrong reasons, pulled between positive signals (famous successful names) and neutral tone.

### Example 4

- **Article ID:** NEWS_0707
- **Excerpt:** "Vladimir Putin spent the Russian New Year boogying to the hits of ABBA after spending $30,000 to fly a tribute band to a lake town north of Moscow..."
- **Predicted label:** negative — **0.935**
- **Interpretation:** Clearly wrong. This is a lighthearted, humorous political news item. The model keys on "Vladimir Putin" and political context, associating them with negative sentiment. A confidence of 0.935 on a clearly neutral-to-positive article is a severe calibration failure — the model is maximally wrong and maximally confident simultaneously.

### Example 5

- **Article ID:** NEWS_0892
- **Excerpt:** "It's a high-tech, high-stakes game of cat-and-mouse... as the Iranian government seeks to shut down protesters using the Web..."
- **Predicted label:** negative — **0.958** (highest confidence in the entire corpus)
- **Interpretation:** Suspicious. A technical article about cyber-attacks on Iranian government websites achieves the highest confidence in the entire corpus. Words like "attack," "hacking," and "seeks" create a perfect storm of negative signals identical to a furious one-star app review. This is the most extreme example of domain-shift bias: security and political conflict language maps perfectly onto the negative class vocabulary the model learned from app complaints.

## Engineering judgment

I would not ship this model to production for tech and entertainment news sentiment classification. The core problem is not accuracy in isolation — the model produces plausible results on clearly negative stories such as crime and legal scandals — but miscalibrated confidence on out-of-domain content. With a median predicted probability of only 0.584 and over 53% of predictions falling below 0.6, the model is deeply uncertain on the majority of the corpus. In a production pipeline that uses predicted probability as a gating signal — for example, routing low-confidence predictions to human review — setting any meaningful threshold would flag more than half the corpus for manual inspection, making automation pointless. The 41.9% negative rate also signals systematic label pollution: any downstream system consuming these predictions would inherit a strong negativity bias unrelated to actual article sentiment, which in the news domain could distort editorial dashboards, topic monitoring, or brand-safety tools. Before deploying, I would fine-tune on a labeled sample of news articles, apply temperature scaling calibrated on a held-out news set, and set the human-review threshold conservatively at 0.85+ given how unreliable the mid-range confidence scores are in this domain.