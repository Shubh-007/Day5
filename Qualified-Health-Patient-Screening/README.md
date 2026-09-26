# Qualified Health - Patient Screening Platform

**Use Case**: Identifying Patients for Life-Saving Treatments  
**Status**: GO with phased execution  
**Generated**: 2026-09-26  
**Workflow Tokens**: 80,614 (reused orchestration script, -90% vs Banner Health)

## 📋 Documentation

- **[plan.md](./plan.md)** - Main planning document with HLD, LLD, implementation, risks, success criteria
- **[architecture/](./architecture/)** - System architecture details
- **[implementation/](./implementation/)** - Development roadmap and phases
- **[monitoring/](./monitoring/)** - Observability strategy

## 🎯 Quick Facts

| Aspect | Detail |
|--------|--------|
| **Health Systems** | 2-5 initial → 50+ long-term |
| **Patient Populations** | 10-50M total across systems |
| **Timeline** | 21+ weeks (v0→v1→v2) |
| **Team** | 15-20 FTE → 50-60 FTE |
| **Budget** | $3-5M/year (infrastructure + personnel) |
| **API SLA** | 99.5% uptime, <200ms p95 latency |

## 🚀 Phase Gates

- **v0→v1**: 90%+ rule accuracy, <10% data reconciliation errors, HIPAA audit pass
- **v1→v2**: 99.5% uptime, multi-EHR integration, <200ms API latency

## ⚠️ Critical Success Factors

1. Clinical advisory board (3-5 experts) by month 1
2. Data quality monitoring from week 3
3. Single health system v0 validation by month 3
4. FDA engagement by month 12
5. Explicit phase gates before scaling

## 🔗 Related Projects

- **Banner Health** - `/home/labuser/Day5/Banner-Health-Clinical-Assistant/` (physician documentation)
- **Qualified Health** - `/home/labuser/Day5/Qualified-Health-Patient-Screening/` (patient screening)

**Both use same plan orchestration workflow for consistency.**
