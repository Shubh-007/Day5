import http from 'k6/http';
import { check, sleep } from 'k6';

// Scaled-down stand-in for the "10k VUs" request. The target is a
// single-threaded stdlib Python http.server (see DEPLOY.md: "adequate
// for testing/demo" only) on a 4-CPU/no-swap local VM, so 10k VUs would
// mostly measure k6's own memory exhaustion rather than the app. This
// ramps to 150 VUs, high enough to actually saturate a single-threaded
// server and show real degradation, without risking the host.
const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';

export const options = {
  stages: [
    { duration: '20s', target: 150 }, // ramp up to 150 VUs
    { duration: '30s', target: 150 }, // hold at 150 VUs
    { duration: '10s', target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
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
