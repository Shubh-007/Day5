# 📊 K6 Load Testing Guide - Elation Health RAG Integration

**Purpose**: Validate that RAG endpoints meet performance targets under realistic clinical load  
**Test File**: `load-tests/k6-load-test.js`  
**Version**: 1.0

---

## Quick Start

### Run K6 Load Test

```bash
cd /home/labuser/Day5/Elation-Health-Chart-Review

# Basic run
k6 run load-tests/k6-load-test.js

# Run with CSV export and summary
k6 run load-tests/k6-load-test.js \
  --out csv=results.csv \
  --summary-export=summary.json

# Run with verbose output
k6 run load-tests/k6-load-test.js -v
```

### View Results

```bash
# CSV results
cat results.csv | head -20

# Summary JSON
cat summary.json | jq '.metrics'
```

---

## Test Configuration

### Load Profile

```
Duration: ~4 minutes total
├── Ramp-up (30s)    → 0 to 10 users
├── Steady (60s)     → 10 to 50 users
├── Spike (30s)      → 50 to 100 users (peak clinic load)
├── Sustained (60s)  → back to 50 users
└── Ramp-down (30s)  → 50 to 0 users
```

**Rationale**: Simulates typical clinic morning:
- Early morning (light load)
- Mid-morning peak (50 users)
- Spike (busy period with 100 concurrent reviews)
- Sustained high load
- Wind-down

### Performance Thresholds

| Metric | Target | Threshold |
|--------|--------|-----------|
| Dashboard API | <2s | p95 < 2000ms |
| RAG Endpoints | <100ms | p95 < 500ms |
| All APIs | Overall | p99 < 1000ms |
| Error Rate | <1% | rate < 0.1 |

---

## Test Scenarios

### 1. Dashboard Load Test

```javascript
testDashboardLoad()
├── Endpoint: GET /api/dashboard
├── Purpose: Load all patient summaries
├── Expected: <2s response time
└── Metric: dashboard_latency
```

**What it tests**:
- Backend can serve multiple patient summaries
- Includes RAG data (when available)
- Handles spike in dashboard refreshes

---

### 2. Clinical Context Retrieval

```javascript
testClinicalContext()
├── Endpoint: GET /api/tools/clinical-context/{mrn}
├── Params: ?include=problems,medications,alerts
├── Purpose: RAG retrieves rich patient context
├── Expected: <100ms response time
└── Metric: tool_latency (clinical_context)
```

**What it tests**:
- RAG engine can fetch patient data quickly
- Parameters are processed correctly
- Data structure is consistent

---

### 3. Condition Profile Lookup

```javascript
testConditionProfile()
├── Endpoint: GET /api/tools/condition-profile/{icd10}
├── Conditions tested: I10, E11.9, E78.5, I50.9, F41.1
├── Purpose: Retrieve clinical guidelines for condition
├── Expected: <50ms response time
└── Metric: tool_latency (condition_profile)
```

**What it tests**:
- RAG knowledge base retrieval is fast
- Condition codes are recognized
- Guidelines are properly formatted

---

### 4. Drug Interaction Check

```javascript
testDrugInteractions()
├── Endpoint: POST /api/tools/drug-interactions
├── Payload: {"medications": ["Lisinopril", "Metformin"]}
├── Purpose: Check for drug-drug interactions
├── Expected: <50ms response time
└── Metric: tool_latency (drug_interactions)
```

**What it tests**:
- Interaction checking is fast
- Can handle multiple drug combinations
- Safety data is accurate

**Drug combinations tested**:
- Lisinopril + Metformin (no interaction)
- Atorvastatin + Sertraline (no interaction)
- Metoprolol + Aspirin (check)
- 3-drug combination (Lisinopril + Atorvastatin + Metformin)

---

### 5. RAG Retrieval Test

```javascript
testRagRetrieval()
├── Endpoint: GET /api/tools/retrieve/context
├── Params: ?query=diabetes%20management&context_type=guideline
├── Purpose: Retrieve guidelines via RAG semantic search
├── Expected: <100ms response time
└── Metric: rag_latency
```

**What it tests**:
- RAG semantic retrieval works under load
- Query parameters are handled correctly
- Relevance ranking functions properly

**Queries tested**:
- "diabetes management"
- "hypertension treatment"
- "heart failure"

---

### 6. Safety Alerts Test

```javascript
testSafetyAlerts()
├── Endpoint: GET /api/tools/safety-alerts/{mrn}
├── Params: ?severity=all
├── Purpose: Fetch critical safety alerts for patient
├── Expected: <50ms response time
└── Metric: tool_latency (safety_alerts)
```

**What it tests**:
- Alert system performs under load
- Critical alerts are prioritized
- Patient MRN validation works

---

### 7. Lab Trend Analysis

```javascript
testLabTrends()
├── Endpoint: GET /api/tools/lab-trends/{mrn}/{test_code}
├── Tests: A1c, glucose, creatinine
├── Purpose: Retrieve lab value history & trends
├── Expected: <100ms response time
└── Metric: tool_latency (lab_trends)
```

**What it tests**:
- Lab data retrieval is efficient
- Trend analysis completes quickly
- Multiple test codes are supported

---

### 8. Search Records Test

```javascript
testSearchRecords()
├── Endpoint: GET /api/tools/search-records
├── Params: ?query=A1c&limit=10
├── Purpose: Full-text search patient records
├── Expected: <200ms response time
└── Metric: tool_latency (search_records)
```

**What it tests**:
- Search indexing is fast
- Query parsing works correctly
- Result limiting works

---

## Custom Metrics

### Key Metrics Collected

```javascript
Latency Metrics:
├── api_latency          → All API calls
├── dashboard_latency    → Dashboard-specific
├── tool_latency         → RAG tools average
├── rag_latency          → RAG retrieval specific
└── tool_calls           → Count of tool invocations

Reliability:
├── errors               → Error rate
└── http_req_duration    → HTTP request duration
```

### Reading the Output

```
✓ is ok - passed
✗ is not ok - failed

Example output:
  data_received..................: 2.5 MB 623 kB/s
  data_sent.......................: 1.2 MB 300 kB/s
  http_req_duration...............: avg=85ms p(95)=142ms p(99)=289ms
  http_req_failed.................: 0.00%
```

---

## Expected Results

### Healthy Baseline

When RAG integration is working correctly, you should see:

```
┌─────────────────────────────┬──────┬──────┬────────┬────────┐
│ Metric                      │ Avg  │ Min  │ Max    │ Status │
├─────────────────────────────┼──────┼──────┼────────┼────────┤
│ Dashboard Load              │ 1.2s │ 800m │ 1.8s   │ ✅     │
│ Clinical Context            │ 45ms │ 20ms │ 95ms   │ ✅     │
│ Condition Profile           │ 30ms │ 10ms │ 60ms   │ ✅     │
│ Drug Interactions           │ 35ms │ 15ms │ 70ms   │ ✅     │
│ RAG Retrieval               │ 60ms │ 25ms │ 120ms  │ ✅     │
│ Safety Alerts               │ 40ms │ 15ms │ 80ms   │ ✅     │
│ Lab Trends                  │ 55ms │ 20ms │ 110ms  │ ✅     │
│ Search Records              │ 120ms│ 50ms │ 200ms  │ ✅     │
│ Error Rate                  │ 0.0% │ -    │ -      │ ✅     │
└─────────────────────────────┴──────┴──────┴────────┴────────┘
```

### Degraded Performance (Investigate)

If you see:
- Dashboard load > 3s → Backend bottleneck
- RAG queries > 200ms → Database or retrieval issue
- Error rate > 1% → Connection or validation issue

---

## Troubleshooting

### Issue: Connection Refused

```bash
Error: Request Failed
Error code 104
```

**Solution**: Ensure backend is running
```bash
python backend/app.py
# Should show: Uvicorn running on http://0.0.0.0:8000
```

### Issue: Slow Performance

```
p(95)=1500ms (exceeds 500ms threshold)
```

**Diagnosis**:
```bash
# Check backend logs
tail -f /tmp/elation-backend.log

# Monitor system resources
watch -n 1 'ps aux | grep python'

# Check database
# (if using database for RAG)
```

**Solutions**:
1. Add caching to RAG queries
2. Optimize database indexes
3. Increase server resources
4. Profile hot paths with py-spy

### Issue: High Error Rate

```
http_req_failed...................: 12.50%
```

**Diagnosis**:
```bash
# Check specific failures in CSV
grep 'fail' results.csv

# Check error types
cat results.csv | grep 'error' | sort | uniq -c
```

**Common Causes**:
- Patient MRN not found → Verify test data
- Query parameter validation → Check encoding
- Rate limiting → Reduce concurrent users

---

## Performance Optimization

### If Tests Fail

1. **Identify bottleneck**
   ```bash
   grep 'p(95)' summary.json
   ```

2. **Profile the code**
   ```bash
   # Backend profiling
   python -m py_spy record -o profile.svg python backend/app.py
   ```

3. **Common optimizations**
   - Add caching (Redis) for RAG queries
   - Batch queries where possible
   - Optimize database queries
   - Use async/await for I/O
   - Connection pooling

### Caching Strategy

```python
# Example: Cache condition profiles
from functools import lru_cache

@lru_cache(maxsize=100)
def get_condition_profile(icd10: str):
    return rag_engine.get_condition(icd10)
```

---

## Integration with CI/CD

### Run K6 in GitHub Actions

```yaml
- name: Run K6 Load Test
  run: |
    k6 run load-tests/k6-load-test.js \
      --out csv=results.csv \
      --summary-export=summary.json
    
    # Fail if thresholds exceeded
    k6 run load-tests/k6-load-test.js \
      --threshold='http_req_duration{type:dashboard}<2000' \
      --threshold='errors<0.1'
```

### Upload Results

```yaml
- name: Upload K6 Results
  uses: actions/upload-artifact@v2
  with:
    name: k6-results
    path: |
      results.csv
      summary.json
```

---

## Monitoring in Production

### Key Metrics to Track

1. **Response Time P95**
   - Target: <500ms for RAG endpoints
   - Alert if: >1000ms

2. **Error Rate**
   - Target: <0.1%
   - Alert if: >1%

3. **Throughput**
   - Target: 50+ concurrent users
   - Alert if: <20 users causes issues

4. **Resource Usage**
   - CPU: <70%
   - Memory: <80%
   - Disk: <85%

### Grafana Dashboard Query

```promql
# P95 latency for RAG endpoints
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{endpoint=~"/api/tools/.*"}[5m]))

# Error rate
rate(http_requests_failed_total[5m]) / rate(http_requests_total[5m])

# Throughput
rate(http_requests_total[5m])
```

---

## Test Report Template

When submitting K6 results:

```markdown
# K6 Load Test Results

**Date**: [DATE]
**Duration**: 4 minutes
**Peak Load**: 100 concurrent users

## Results Summary
- ✅ All endpoints < 500ms (RAG threshold)
- ✅ Error rate: 0.0%
- ✅ Dashboard load: avg 1.2s (target <2s)

## Performance Breakdown
[Table of results]

## Issues Found
[List any threshold breaches]

## Recommendations
[Optimization suggestions]
```

---

## References

- **K6 Documentation**: https://k6.io/docs
- **Performance Testing**: https://k6.io/blog/performance-testing-guide
- **Thresholds**: https://k6.io/docs/using-k6/thresholds
- **Custom Metrics**: https://k6.io/docs/using-k6/metrics

---

**Last Updated**: 2026-09-26  
**Status**: Ready for testing  
**Attribution**: Claude Haiku 4.5

