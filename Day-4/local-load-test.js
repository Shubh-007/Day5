import http from 'k6/http';
import { check, sleep } from 'k6';

// Local target: the R&D Evidence Retrieval Agent web app already running
// on this box (see start.sh / DEPLOY.md). Override with -e BASE_URL=... to
// point elsewhere (falls back to a public placeholder if nothing is local).
const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';

export const options = {
  stages: [
    { duration: '20s', target: 10 }, // ramp up to 10 VUs
    { duration: '20s', target: 10 }, // hold at 10 VUs
    { duration: '20s', target: 0 },  // ramp down
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],   // error rate < 1%
    http_req_duration: ['p(95)<500'], // p95 latency < 500ms
  },
};

const REQUESTERS = ['dr.smith@hospital.local', 'dr.jones@hospital.local', 'dr.lee@hospital.local'];
const QUESTIONS = [
  'What is the evidence for beta-blocker use in heart failure reducing mortality?',
  'Is red wine consumption associated with reduced cardiovascular risk?',
];

export default function () {
  const statusRes = http.get(`${BASE_URL}/api/status`, { tags: { name: 'status' } });
  check(statusRes, {
    'status is 200': (r) => r.status === 200,
  });

  const requester = REQUESTERS[Math.floor(Math.random() * REQUESTERS.length)];
  const question = QUESTIONS[Math.floor(Math.random() * QUESTIONS.length)];

  const queryRes = http.post(
    `${BASE_URL}/api/query`,
    { research_question: question, requester_id: requester },
    { tags: { name: 'query' } }
  );
  check(queryRes, {
    'query is 200': (r) => r.status === 200,
    'query returned success': (r) => {
      try {
        return JSON.parse(r.body).success === true;
      } catch {
        return false;
      }
    },
  });

  sleep(1);
}
