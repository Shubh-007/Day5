---
type: community
members: 7
---

# Fund Data Pipeline

**Members:** 7 nodes

## Members
- [[CAGR Return Calculation]] - rationale - .claude/agents/fund-data-fetcher.md
- [[SIP Calculator Enhanced Page (with Live Fund Data)]] - code - sip-calculator-enhanced.html
- [[SIP Calculator Page (Basic, with Pie Chart)]] - code - sip-calculator.html
- [[Target Funds List (5 Indian Large-Flexi-Cap Schemes)]] - concept - .claude/agents/fund-data-fetcher.md
- [[fund-data-fetcher Agent]] - document - .claude/agents/fund-data-fetcher.md
- [[fund-data.json Output Schema]] - concept - .claude/agents/fund-data-fetcher.md
- [[mfapi.in Public API]] - concept - .claude/agents/fund-data-fetcher.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Fund_Data_Pipeline
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Live Fund Data Flow]]

## Top bridge nodes
- [[fund-data-fetcher Agent]] - degree 6, connects to 1 community
- [[fund-data.json Output Schema]] - degree 2, connects to 1 community