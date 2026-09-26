# Graph Report - Day4  (2026-09-19)

## Corpus Check
- Corpus is ~2,957 words - fits in a single context window. You may not need a graph.

## Summary
- 23 nodes · 23 edges · 5 communities (3 shown, 2 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.92)
- Token cost: 57,600 input · 0 output

## Community Hubs (Navigation)
- Fund Data Pipeline
- Live Fund Data Flow
- SIP Calculation Core
- MCP Server Config

## God Nodes (most connected - your core abstractions)
1. `fund-data-fetcher Agent` - 6 edges
2. `fetchMarketData()` - 4 edges
3. `displayFunds()` - 4 edges
4. `selectFund()` - 3 edges
5. `calculateSIP()` - 3 edges
6. `fetch` - 2 edges
7. `fund-data.json Output Schema` - 2 edges
8. `SIP Calculator Enhanced Page (with Live Fund Data)` - 2 edges
9. `calculateSIP()` - 2 edges
10. `formatNumber()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `SIP Calculator Page (Basic, with Pie Chart)` --semantically_similar_to--> `SIP Calculator Enhanced Page (with Live Fund Data)`  [INFERRED] [semantically similar]
  sip-calculator.html → sip-calculator-enhanced.html
- `calculateSIP()` --semantically_similar_to--> `calculateSIP()`  [INFERRED] [semantically similar]
  sip-calculator-enhanced.html → sip-calculator.html
- `formatNumber()` --semantically_similar_to--> `formatNumber()`  [INFERRED] [semantically similar]
  sip-calculator-enhanced.html → sip-calculator.html
- `fund-data-fetcher Agent` --references--> `SIP Calculator Enhanced Page (with Live Fund Data)`  [EXTRACTED]
  .claude/agents/fund-data-fetcher.md → sip-calculator-enhanced.html
- `fetchMarketData()` --references--> `fund-data-fetcher Agent`  [EXTRACTED]
  sip-calculator-enhanced.html → .claude/agents/fund-data-fetcher.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Duplicated Core SIP Calculation Logic Across Both Pages** — sip_calculator_enhanced_calculatesip, sip_calculator_enhanced_formatnumber, sip_calculator_enhanced_resetform, sip_calculator_calculatesip, sip_calculator_formatnumber, sip_calculator_resetform [INFERRED 0.85]
- **Live Fund Data Browsing Flow in Enhanced Calculator** — sip_calculator_enhanced_fetchmarketdata, sip_calculator_enhanced_displayfunds, sip_calculator_enhanced_filterfunds, sip_calculator_enhanced_selectfund, sip_calculator_enhanced_usefundreturns, sip_calculator_enhanced_fmtpct [EXTRACTED 1.00]
- **End-to-End Pipeline: Fetch Live NAV Data to SIP Return Input** — claude_agents_fund_data_fetcher_agent, claude_agents_fund_data_fetcher_fund_data_json, sip_calculator_enhanced_fetchmarketdata, sip_calculator_enhanced_usefundreturns, sip_calculator_enhanced_calculatesip [INFERRED 0.85]

## Communities (5 total, 2 thin omitted)

### Community 0 - "Fund Data Pipeline"
Cohesion: 0.29
Nodes (7): fund-data-fetcher Agent, CAGR Return Calculation, fund-data.json Output Schema, mfapi.in Public API, Target Funds List (5 Indian Large-/Flexi-Cap Schemes), SIP Calculator Enhanced Page (with Live Fund Data), SIP Calculator Page (Basic, with Pie Chart)

### Community 1 - "Live Fund Data Flow"
Cohesion: 0.47
Nodes (5): displayFunds(), fetchMarketData(), filterFunds(), fmtPct(), selectFund()

### Community 2 - "SIP Calculation Core"
Cohesion: 0.50
Nodes (4): calculateSIP(), calculateSIP(), formatNumber(), formatNumber()

## Knowledge Gaps
- **4 isolated node(s):** `/home/labuser/venv/bin/mcp-server-fetch`, `mfapi.in Public API`, `Target Funds List (5 Indian Large-/Flexi-Cap Schemes)`, `SIP Calculator Page (Basic, with Pie Chart)`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 10 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `fund-data-fetcher Agent` connect `Fund Data Pipeline` to `Live Fund Data Flow`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Why does `fetchMarketData()` connect `Live Fund Data Flow` to `Fund Data Pipeline`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **What connects `/home/labuser/venv/bin/mcp-server-fetch`, `mfapi.in Public API`, `Target Funds List (5 Indian Large-/Flexi-Cap Schemes)` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._