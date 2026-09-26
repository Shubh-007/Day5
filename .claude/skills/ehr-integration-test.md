# EHR Integration Test Skill
## Healthcare System Connectivity & Data Exchange Validation

**Trigger**: `/ehr-test` or `ehr integration test` in prompt  
**Type**: Integration testing agent  
**Use Case**: Validate integration with Epic, Cerner, Meditech, Athena  

---

## What This Skill Does

Tests EHR integrations for:
- **API Connectivity**: OAuth2 auth, endpoint availability, latency
- **Data Exchange**: FHIR/HL7 compliance, data accuracy, round-trip integrity
- **Performance**: Throughput, latency targets, error rates
- **Error Handling**: Graceful degradation, retry logic, fallbacks
- **Security**: TLS encryption, credential management, audit logging
- **Format Compliance**: Valid HL7/FHIR, proper code mappings

---

## How to Use

```
/ehr-test <ehr_system> [--endpoint <url>] [--test-data <file>] [--load-test]
```

**Examples**:
```
/ehr-test epic --endpoint https://epic.healthcare.com/fhir --load-test

/ehr-test cerner --test-data sample_patient.json

/ehr-test all --endpoint-config /path/to/ehr_endpoints.json
```

---

## EHR Systems Supported

- **Epic**: SMART-on-FHIR, HL7v2 ADT, proprietary APIs
- **Cerner**: FHIR R4, proprietary Millennium APIs
- **Meditech**: HL7v2, HIEOS, REST APIs
- **Athena**: REST API with custom extensions
- **Generic**: Any FHIR-compliant system

---

## Test Suites

1. **Connectivity Tests** (5 min)
   - Authentication flows
   - Endpoint availability
   - Certificate validation

2. **Data Exchange Tests** (15 min)
   - Patient record retrieval
   - Medication list accuracy
   - Lab results mapping
   - Note submission

3. **Performance Tests** (30 min)
   - Throughput (records/sec)
   - Latency (p50/p95/p99)
   - Error rates under load

4. **Security Tests** (10 min)
   - TLS validation
   - Credential handling
   - Audit logging

---

## Output

```
✅ Epic Integration Test Results
├─ Connectivity: ✅ PASS (auth OK, <500ms latency)
├─ Data Exchange: ✅ PASS (100 patients, accuracy 99.8%)
├─ Performance: ✅ PASS (500 rec/sec, p95 < 2s)
├─ Security: ✅ PASS (TLS 1.3, encryption OK)
└─ Recommendation: Ready for production

Summary:
- 4/4 test suites passed
- Ready for pilot deployment
- Monitor: Lat P95 (currently 1.8s, target <2s)
```

---

## Integration

Used by:
- **Commure**: Validate Epic/Cerner note submission
- **Elation**: Verify chart data retrieval
- **Banner, Carta, Qualified**: Data access validation
- **DevOps**: Pre-deployment verification
- **QA**: Weekly integration regression tests

---

## Configuration

```json
{
  "ehr-integration-test": {
    "ehr_systems": ["epic", "cerner"],
    "endpoints": {
      "epic": "https://epic.health.org/fhir",
      "cerner": "https://cerner.health.org/fhir"
    },
    "performance_targets": {
      "throughput_records_per_sec": 500,
      "latency_p95_seconds": 2,
      "error_rate_percent": 0.1
    },
    "load_test_enabled": true
  }
}
```

---

## Team Permissions

- **DevOps Engineer**: Full access
- **Integration Lead**: Full access
- **QA Engineer**: Can trigger tests
- **Developers**: Read results
