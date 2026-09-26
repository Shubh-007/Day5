---
type: community
members: 6
---

# Live Fund Data Flow

**Members:** 6 nodes

## Members
- [[displayFunds()]] - code - sip-calculator-enhanced.html
- [[fetchMarketData()]] - code - sip-calculator-enhanced.html
- [[filterFunds()]] - code - sip-calculator-enhanced.html
- [[fmtPct()]] - code - sip-calculator-enhanced.html
- [[selectFund()]] - code - sip-calculator-enhanced.html
- [[useFundReturns()]] - code - sip-calculator-enhanced.html

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Live_Fund_Data_Flow
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Fund Data Pipeline]]

## Top bridge nodes
- [[fetchMarketData()]] - degree 4, connects to 1 community