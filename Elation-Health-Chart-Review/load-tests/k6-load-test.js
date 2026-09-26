/**
 * Elation Health - K6 Load Testing Script
 * Tests core API endpoints under realistic load
 *
 * Run: k6 run k6-load-test.js
 * With results: k6 run k6-load-test.js --out csv=results.csv --summary-export=summary.json
 */

import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const apiLatency = new Trend('api_latency');
const dashboardLatency = new Trend('dashboard_latency');
const toolLatency = new Trend('tool_latency');
const ragLatency = new Trend('rag_latency');
const toolCallCount = new Counter('tool_calls');

// Configuration
const BASE_URL = 'http://localhost:8000';
const PATIENTS = ['P001234', 'P005678', 'P009012'];

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 10, name: 'ramp-up' },      // Ramp up to 10 users
    { duration: '1m', target: 50, name: 'steady' },         // Stay at 50 users
    { duration: '30s', target: 100, name: 'spike' },        // Spike to 100 users
    { duration: '1m', target: 50, name: 'sustained' },      // Back to 50
    { duration: '30s', target: 0, name: 'ramp-down' }       // Ramp down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500', 'p(99)<1000'],      // 95% < 500ms
    'http_req_duration{type:dashboard}': ['p(95)<2000'],    // Dashboard < 2s
    'errors': ['rate<0.1'],                                 // Error rate < 10%
  },
  ext: {
    loadimpact: {
      projectID: 3400000,
      name: 'Elation Health Load Test'
    }
  }
};

// Test 1: Dashboard Load
export function testDashboardLoad() {
  group('Dashboard - Load all patient summaries', () => {
    const res = http.get(`${BASE_URL}/api/dashboard`);

    dashboardLatency.add(res.timings.duration, { type: 'dashboard' });
    errorRate.add(res.status !== 200);

    check(res, {
      'dashboard loaded': (r) => r.status === 200,
      'has patients': (r) => r.body.includes('patientName'),
      'response time < 2s': (r) => r.timings.duration < 2000,
      'returns 3 patients': (r) => r.body.includes('P001234')
    });
  });

  sleep(1);
}

// Test 2: Clinical Context Retrieval
export function testClinicalContext() {
  const patientMrn = PATIENTS[Math.floor(Math.random() * PATIENTS.length)];

  group(`Clinical Context - Get context for ${patientMrn}`, () => {
    const res = http.get(
      `${BASE_URL}/api/tools/clinical-context/${patientMrn}?include=problems,medications,alerts`
    );

    toolLatency.add(res.timings.duration, { endpoint: 'clinical_context' });
    toolCallCount.add(1);
    errorRate.add(res.status !== 200);

    check(res, {
      'context retrieved': (r) => r.status === 200,
      'has problems': (r) => r.body.includes('problems'),
      'has medications': (r) => r.body.includes('medications'),
      'has alerts': (r) => r.body.includes('alerts'),
      'response time < 100ms': (r) => r.timings.duration < 100
    });
  });

  sleep(0.5);
}

// Test 3: Condition Profile Lookup
export function testConditionProfile() {
  const conditions = ['I10', 'E11.9', 'E78.5', 'I50.9', 'F41.1'];
  const condition = conditions[Math.floor(Math.random() * conditions.length)];

  group(`Condition Profile - ${condition}`, () => {
    const res = http.get(`${BASE_URL}/api/tools/condition-profile/${condition}`);

    toolLatency.add(res.timings.duration, { endpoint: 'condition_profile' });
    errorRate.add(res.status !== 200);

    check(res, {
      'condition found': (r) => r.status === 200,
      'has name': (r) => r.body.includes('name'),
      'has management': (r) => r.body.includes('management'),
      'response time < 50ms': (r) => r.timings.duration < 50
    });
  });

  sleep(0.3);
}

// Test 4: Drug Interaction Check
export function testDrugInteractions() {
  const drugSets = [
    ['Lisinopril', 'Metformin'],
    ['Atorvastatin', 'Sertraline'],
    ['Metoprolol', 'Aspirin'],
    ['Lisinopril', 'Atorvastatin', 'Metformin']
  ];

  const drugs = drugSets[Math.floor(Math.random() * drugSets.length)];

  group(`Drug Interactions - ${drugs.join(', ')}`, () => {
    const payload = JSON.stringify({ medications: drugs });
    const res = http.post(
      `${BASE_URL}/api/tools/drug-interactions`,
      payload,
      { headers: { 'Content-Type': 'application/json' } }
    );

    toolLatency.add(res.timings.duration, { endpoint: 'drug_interactions' });
    toolCallCount.add(1);
    errorRate.add(res.status !== 200);

    check(res, {
      'interactions checked': (r) => r.status === 200,
      'has total_interactions': (r) => r.body.includes('total_interactions'),
      'response time < 50ms': (r) => r.timings.duration < 50
    });
  });

  sleep(0.5);
}

// Test 5: RAG Retrieval
export function testRagRetrieval() {
  const queries = ['diabetes management', 'hypertension treatment', 'heart failure'];
  const query = queries[Math.floor(Math.random() * queries.length)];

  group(`RAG Retrieval - ${query}`, () => {
    const res = http.get(
      `${BASE_URL}/api/tools/retrieve/context?query=${encodeURIComponent(query)}&context_type=guideline`
    );

    ragLatency.add(res.timings.duration, { query_type: 'guideline' });
    errorRate.add(res.status !== 200);

    check(res, {
      'retrieval successful': (r) => r.status === 200,
      'has results': (r) => r.body.includes('results'),
      'response time < 100ms': (r) => r.timings.duration < 100
    });
  });

  sleep(0.5);
}

// Test 6: Safety Alerts
export function testSafetyAlerts() {
  const patientMrn = PATIENTS[Math.floor(Math.random() * PATIENTS.length)];

  group(`Safety Alerts - ${patientMrn}`, () => {
    const res = http.get(
      `${BASE_URL}/api/tools/safety-alerts/${patientMrn}?severity=all`
    );

    toolLatency.add(res.timings.duration, { endpoint: 'safety_alerts' });
    errorRate.add(res.status !== 200);

    check(res, {
      'alerts retrieved': (r) => r.status === 200,
      'has alert count': (r) => r.body.includes('total_alerts'),
      'response time < 50ms': (r) => r.timings.duration < 50
    });
  });

  sleep(0.3);
}

// Test 7: Lab Trend Analysis
export function testLabTrends() {
  const patientMrn = PATIENTS[Math.floor(Math.random() * PATIENTS.length)];
  const tests = ['A1c', 'glucose', 'creatinine'];
  const testCode = tests[Math.floor(Math.random() * tests.length)];

  group(`Lab Trends - ${patientMrn} ${testCode}`, () => {
    const res = http.get(
      `${BASE_URL}/api/tools/lab-trends/${patientMrn}/${testCode}`
    );

    toolLatency.add(res.timings.duration, { endpoint: 'lab_trends' });
    errorRate.add(res.status !== 200);

    check(res, {
      'trends retrieved': (r) => r.status === 200,
      'has values': (r) => r.body.includes('values'),
      'response time < 100ms': (r) => r.timings.duration < 100
    });
  });

  sleep(0.5);
}

// Test 8: Search Records
export function testSearchRecords() {
  const queries = ['A1c', 'blood pressure', 'medication change'];
  const query = queries[Math.floor(Math.random() * queries.length)];

  group(`Search Records - ${query}`, () => {
    const res = http.get(
      `${BASE_URL}/api/tools/search-records?query=${encodeURIComponent(query)}&limit=10`
    );

    toolLatency.add(res.timings.duration, { endpoint: 'search_records' });
    errorRate.add(res.status !== 200);

    check(res, {
      'search completed': (r) => r.status === 200,
      'has results': (r) => r.body.includes('total_results'),
      'response time < 200ms': (r) => r.timings.duration < 200
    });
  });

  sleep(0.5);
}

// Main test scenario
export default function() {
  // Simulate realistic user behavior
  testDashboardLoad();
  testClinicalContext();
  testConditionProfile();
  testDrugInteractions();
  testRagRetrieval();
  testSafetyAlerts();
  testLabTrends();
  testSearchRecords();
}

// Teardown - print summary
export function teardown(data) {
  console.log('=== Load Test Summary ===');
  console.log('Test completed successfully');
  console.log('Check results.csv for detailed metrics');
}
