Use at least three evidence families before making a strong claim:
- market structure data: census, filings, association reports, public benchmarks
- behavior data: search trends, reviews, job posts, product usage proxies
- direct customer evidence: interviews, surveys, waitlists, prepayments, LOIs

See `evidence-grading.md` for the confidence ladder. If all evidence comes from one source type, the conclusion is still fragile.

### 4. Segment Before You Generalize

Do not treat "the market" as one blob. Split by:
- customer type
- company size
- geography
- urgency of problem
- willingness to pay
- existing alternatives

Many bad conclusions come from averaging together segments that behave very differently.

### 5. Map Competition Around Customer Choice, Not Only Brand Names

Competitor analysis includes:
- direct competitors
- indirect substitutes
- internal workarounds such as spreadsheets, agencies, or manual processes
- future entrants with clear adjacency

Use `competitor-analysis.md` to build a positioning map, review-mining matrix, and whitespace view. The real competitor is whatever the customer would choose instead of the proposed offer.

### 6. Favor Revealed Demand Over Stated Enthusiasm

Use interviews and surveys to learn language and patterns, but trust behavior more than compliments.

Strong signals:
- repeated painful workarounds
- urgent problem frequency
- customers introducing others with the same pain
- willingness to pay, pilot, pre-order, or switch

Weak signals:
- "great idea"
- generic survey positivity
- likes, followers, or broad curiosity with no concrete action

See `validation.md` for interview, survey, and pricing research structures.

### 7. Finish with a Decision-Ready Recommendation

Every deliverable should end with:

```text
RECOMMENDATION
- What the evidence supports
- What remains uncertain
- What should happen next
- What would change the recommendation
```

Good market research reduces uncertainty. Great market research makes the next move obvious.

## Common Traps

- **Top-down theater** -> Huge category numbers create false confidence and weak planning.
- **Competitor tunnel vision** -> Looking only at visible brands misses substitutes and status-quo behavior.
- **Segment blur** -> Mixing SMB, enterprise, prosumer, and consumer demand corrupts the conclusion.
- **Source recency failure** -> Old pricing pages and stale reports make current decisions look safer than they are.
- **Opinion inflation** -> Survey excitement without action gets mistaken for demand.
- **No confidence labeling** -> Strong and weak evidence get presented with the same weight.
- **Research with no recommendation** -> User gets a report but no practical decision path.

## Security & Privacy

This skill does NOT:
- make hidden outbound requests
- fabricate customer signals or fake interviews
- access private competitor systems
- create persistent memory or maintain a local workspace by default
- store secrets unless the user explicitly asks for that workflow

Live web research is appropriate only when the task requires current market data or the user asks for external evidence.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `pricing` - Convert validation findings into pricing strategy and willingness-to-pay decisions.
- `seo` - Translate validated demand into search-driven positioning and content opportunities.
- `business` - Connect market findings to strategic choices and operating tradeoffs.
- `compare` - Structure side-by-side option analysis when multiple markets or segments compete.
- `data-analysis` - Turn collected numbers into cleaner interpretation and supporting visuals.

## Feedback

- If useful: `clawhub star market-research`
- Stay updated: `clawhub sync`
