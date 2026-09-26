# Banner Health AI Clinical Assistant - Detailed System Architecture

## Low-Level Design Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHYSICIAN TIER (User Interface)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Physician Portal (Web/Mobile)  │  Real-time Notifications  │  Analytics    │
│         [React/Vue]             │      [WebSocket]          │  [Grafana]    │
└──────────────────┬──────────────────────────────┬──────────────────┬────────┘
                   │                              │                  │
┌──────────────────▼──────────────────────────────▼──────────────────▼────────┐
│                    API Gateway & Load Balancer (NGINX/HAProxy)              │
│  Rate Limiting │ Auth (OAuth2/SAML) │ Request Routing │ SSL/TLS            │
│  Token Bucket  │ JWT Validation     │ Sticky Sessions │ Compression        │
└──────────────────┬───────────────────────────────────────────────────────────┘
                   │
      ┌────────────┼────────────┬──────────────┬──────────────┐
      │            │            │              │              │
┌─────▼──────┐ ┌──▼─────────┐ ┌──▼──────────┐ ┌──▼──────────┐ ┌──▼────────┐
│ Physician  │ │    AI      │ │Documentation│ │   Quality  │ │  Audit &  │
│ Interface  │ │ Processing │ │  Generator  │ │ Assurance  │ │  Logging  │
│ Service    │ │ Engine     │ │ Service     │ │ Engine     │ │ Service   │
│            │ │            │ │             │ │            │ │           │
│ REST API   │ │LLM Orch    │ │Template Eng │ │ Validators │ │Event Log  │
│ WebSocket  │ │Prompt Mgmt │ │Format Conv  │ │ Compliance │ │Trail Mgmt │
│ Dashboard  │ │Context Mgmt│ │Validation   │ │ Checker    │ │Anomaly    │
└─────┬──────┘ └──┬────────┘ └──┬──────────┘ └──┬────────┘ └────┬──────┘
      │           │             │              │               │
      └───────────┼─────────────┼──────────────┼───────────────┘
                  │             │              │
        ┌─────────▼─────────────▼──────────────▼────────────┐
        │                                                   │
    ┌───▼──────────────┐              ┌─────────────────┐  │
    │ EHR Integration  │              │ Data Ingestion  │  │
    │ Layer            │              │ Pipeline        │  │
    │                  │              │                 │  │
    │ EHR Connectors   │              │ Validators      │  │
    │ (Epic, Cerner)   │              │ Normalizers     │  │
    │ Connection Pool  │              │ De-identifier   │  │
    │ Auth Manager     │              │ Queue Manager   │  │
    └───┬──────────────┘              └────────┬────────┘  │
        │                                      │            │
        └──────────────┬───────────────────────┘            │
                       │                                    │
        ┌──────────────▼──────────────────────────────────┐ │
        │     System Integration & Resilience Layer       │ │
        │                                                 │ │
        │ Service Registry (Consul)                       │ │
        │ Circuit Breaker (Hystrix pattern)               │ │
        │ Configuration Manager (Spring Cloud Config)     │ │
        │ Health Check Orchestration                      │ │
        │ Graceful Degradation & Feature Flags            │ │
        └──────────────┬──────────────────────────────────┘ │
                       │                                    │
        ┌──────────────▼──────────────────────────────────┐ │
        │        Data Storage & Management Layer          │ │
        │                                                 │ │
        │ ┌─────────────────────────────────────────┐    │ │
        │ │ PostgreSQL (Primary + Read Replicas)    │    │ │
        │ │ - Patient Records (Encrypted PII)       │    │ │
        │ │ - Encounters                            │    │ │
        │ │ - Generated Documentation               │    │ │
        │ │ - Immutable Audit Trail                 │    │ │
        │ │ - Quality Scores                        │    │ │
        │ └─────────────────────────────────────────┘    │ │
        │                                                 │ │
        │ ┌─────────────────────────────────────────┐    │ │
        │ │ Redis Cluster (Caching + Session)       │    │ │
        │ │ - Patient Demographics Cache            │    │ │
        │ │ - Physician Sessions                    │    │ │
        │ │ - Template Cache                        │    │ │
        │ │ - Dead Letter Queue Fallback            │    │ │
        │ └─────────────────────────────────────────┘    │ │
        │                                                 │ │
        │ ┌─────────────────────────────────────────┐    │ │
        │ │ Encryption Service (AES-256)            │    │ │
        │ │ - Field-level encryption                │    │ │
        │ │ - Key Management (AWS KMS)              │    │ │
        │ │ - Key Rotation (Annual)                 │    │ │
        │ └─────────────────────────────────────────┘    │ │
        │                                                 │ │
        │ ┌─────────────────────────────────────────┐    │ │
        │ │ Access Control Service (RBAC/ABAC)      │    │ │
        │ │ - Row-level security                    │    │ │
        │ │ - Attribute-based access                │    │ │
        │ └─────────────────────────────────────────┘    │ │
        └──────────────┬──────────────────────────────────┘ │
                       │                                    │
└───────────────────────┼────────────────────────────────────┘
                        │
        ┌───────────────▼───────────────┐
        │                               │
        │  Multi-Region Deployment       │
        │                               │
        │ ┌──────────────┐              │
        │ │ Region 1     │              │
        │ │ (Primary)    │              │
        │ │ K8s Cluster  │─┐            │
        │ │ PostgreSQL   │ │            │
        │ └──────────────┘ │            │
        │ ┌──────────────┐ │ Real-time  │
        │ │ Region 2     │ │ Replication│
        │ │ (Passive)    │─┤ & Failover │
        │ │ K8s Cluster  │ │            │
        │ │ PostgreSQL   │ │            │
        │ └──────────────┘ │            │
        │ ┌──────────────┐ │            │
        │ │ Region 3     │─┘            │
        │ │ (Disaster)   │              │
        │ │ K8s Cluster  │              │
        │ │ PostgreSQL   │              │
        │ └──────────────┘              │
        └───────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │  Monitoring & Logging │
        │                       │
        │ ┌──────────────────┐  │
        │ │ ELK Stack        │  │
        │ │ (Logs)           │  │
        │ │ Retention: 90d   │  │
        │ │ (Hot/Cold)       │  │
        │ └──────────────────┘  │
        │ ┌──────────────────┐  │
        │ │ Prometheus       │  │
        │ │ (Metrics)        │  │
        │ │ 15s intervals    │  │
        │ └──────────────────┘  │
        │ ┌──────────────────┐  │
        │ │ Jaeger           │  │
        │ │ (Distributed     │  │
        │ │  Tracing)        │  │
        │ │ 30d retention    │  │
        │ └──────────────────┘  │
        │ ┌──────────────────┐  │
        │ │ Grafana/Alerts   │  │
        │ │ Dashboards &     │  │
        │ │ Notifications    │  │
        │ └──────────────────┘  │
        └───────────────────────┘

Key Data Flows:
1. Clinical Data: EHR → Integration Layer → Ingestion Pipeline → Storage
2. Documentation: Context → AI Engine → Generator → QA Engine → Physician Interface
3. Audit Trail: All services → Audit & Logging → Immutable Storage
4. Monitoring: All services → Prometheus → Grafana/Alerts
5. Multi-region: Streaming replication across PostgreSQL replicas
```

## Service Communication Patterns

### Service Mesh & Discovery
- **Service Registry**: Consul for service discovery
- **Load Balancing**: Client-side load balancing with Ribbon
- **Circuit Breaker**: Hystrix pattern for fault tolerance
- **Timeout Management**: 30s default (configurable per operation)
- **Rate Limiting**: Token bucket algorithm (100 req/min per user, 10k req/sec global)

### Communication Protocols
- **Synchronous**: gRPC for internal service-to-service (low latency)
- **Asynchronous**: RabbitMQ for event streaming (data ingestion, audit events)
- **Real-time**: WebSocket for physician interface (status updates, notifications)
- **Batch**: Kafka for analytics and reporting data streams

## Data Flow Patterns

### Clinical Documentation Flow
1. **Ingestion**: EHR system → REST API → Message Queue
2. **Validation**: Data Ingestion Pipeline validates completeness
3. **Processing**: AI Engine generates documentation
4. **Quality Check**: QA Engine validates accuracy and compliance
5. **Delivery**: Physician Interface presents for review
6. **Audit**: All events logged to immutable audit trail

### Error & Recovery Patterns
- **Circuit Breaker**: Open on 5 consecutive failures, half-open after 30s
- **Retry Logic**: Exponential backoff (1s, 2s, 4s, 8s, 16s)
- **Fallback**: Template-based generation if AI unavailable
- **Dead Letter Queue**: Failed messages retained for manual review
- **Health Checks**: 30s probes with 3-failure threshold for auto-restart

## Database Architecture

### Partitioning Strategy
- **Encounters**: Daily range partitioning by admission_date (hot: last 90 days, cold: archive)
- **Generated Docs**: Daily partitioning by created_at (optimize for recent queries)
- **Audit Events**: Daily partitioning by timestamp (immutable, 7-year retention)
- **AI Events**: Daily partitioning by created_at (cost tracking and trending)

### Replication & Failover
- **PostgreSQL Streaming Replication**: 3+ read replicas across availability zones
- **Failover**: Automatic with pg_basebackup (new standby promotion in <5 min)
- **RPO**: 1 minute (continuous WAL streaming)
- **RTO**: 5 minutes (automatic client reconnection)

### Query Optimization
- **Indexes**: Composite indexes on foreign keys and filter columns
- **Materialized Views**: Pre-aggregated metrics for dashboards (hourly refresh)
- **Query Timeout**: 60s default (shorter per operation type)
- **Connection Pooling**: HikariCP (min: 10, max: 100 per service instance)

## Technology Stack

### Compute
- **Container Runtime**: Docker
- **Orchestration**: Kubernetes 1.28+ (managed: AWS EKS, GCP GKE)
- **Service Mesh**: Istio for traffic management and security
- **Auto-scaling**: HPA based on CPU/memory, custom metrics (AI queue depth)

### Data Storage
- **Primary Database**: PostgreSQL 15+
- **Cache Layer**: Redis 7+ (cluster mode for HA)
- **Document Store**: S3/GCS for historical archives
- **Message Queue**: RabbitMQ 3.12+ (cluster mode)

### Observability
- **Logs**: ELK Stack (Elasticsearch 8+, Logstash, Kibana)
- **Metrics**: Prometheus 2.40+, Grafana 9+
- **Tracing**: Jaeger 1.40+ (production deployment)
- **Alerting**: AlertManager, PagerDuty

### AI/ML
- **LLM Provider**: Claude (Anthropic) primary, fallback to alternative
- **Prompt Management**: Custom framework with versioning
- **Model Selection**: Heuristic-based by doc type and complexity
- **Cost Tracking**: Custom billing aggregator

### Security
- **API Gateway**: Kong or AWS API Gateway
- **Authentication**: OAuth2/SAML (enterprise SSO)
- **Encryption**: TLS 1.3 for transit, AES-256 for at-rest
- **Key Management**: AWS KMS or HashiCorp Vault

## Scaling Patterns

### Horizontal Scaling
- **Stateless Services**: AI Processing, Documentation Generator (scale to 100+ pods)
- **Load Balancing**: Nginx/HAProxy with health checks
- **Session Affinity**: Physician WebSocket connections (sticky sessions)

### Vertical Scaling
- **Database**: Increase read replica count, implement connection pooling
- **Cache**: Add Redis nodes to cluster (automatic rebalancing)
- **Message Queue**: Increase RabbitMQ cluster size

### Caching Strategy
- **L1 Cache**: In-memory caching within service (thread-safe, 1-hour TTL)
- **L2 Cache**: Redis distributed cache (80% target hit rate)
- **Cache Invalidation**: Event-based pub/sub on data updates
- **Cache Warming**: Pre-load templates, physician profiles on startup

## Disaster Recovery

### RTO/RPO Targets
- **RTO**: 5 minutes (automatic failover)
- **RPO**: 1 minute (continuous streaming replication)
- **Testing**: Monthly non-disruptive failover drills
- **Runbooks**: Documented recovery procedures for each failure mode

### Backup Strategy
- **Daily Incremental**: Nightly backup of changes only
- **Weekly Full**: Complete database snapshot
- **Geo-redundancy**: Backups stored in geographically distinct regions
- **Retention**: 90 days hot (recovery possible in <1 hour), 7 years cold (compliance)

### Chaos Engineering
- **Frequency**: Weekly in staging, monthly validation
- **Scenarios**: Service kill, network delays, packet loss, CPU throttling
- **Measurement**: RTO, data consistency, recovery success
- **Continuous Improvement**: Runbook updates after each test
