# Shortlink: DevOps/SRE Checklist

A URL shortener built and operated end to end on AWS.

**Rule:** one phase at a time. Every phase ends with something working, a short note in my own words, and a log entry.

## The App

- `POST /shorten` → create a short code for a long URL
- `GET /:code` → redirect + count the click
- `GET /stats/:code` → click count
- `GET /health` → health check

**Stack:** Python FastAPI or Node Express, plus Postgres

---

## Before Starting (AWS Safety)

- [ ] AWS account created
- [ ] MFA enabled on root user, root not used for daily work
- [ ] IAM/Identity Center user created for daily work
- [ ] Billing budget alert set (e.g. $5/month)
- [ ] Empty GitHub repo `shortlink` created

## Habits (Every Phase)

- [ ] Log entry in `docs/log.md` (what I did, what broke, how I fixed it, what I learned)
- [ ] Phase note in my own words (`docs/phase-N-name.md`)
- [ ] Broke something on purpose and fixed it
- [ ] Explained the phase back (to Claude or to a friend)
- [ ] Re-read notes after one week and ran a command from memory

---

# BUILD

## Phase 1: Git Workflow

**Purpose:** nothing reaches `master` without review; every change is traceable.

- [x] `git init`, first commit, push to GitHub
- [x] Add `.gitignore` and README
- [x] Protect `master` (require pull request)
- [x] Complete one full branch → PR → merge cycle

**Learn:** branches, PRs, commit messages, branch protection
**Done when:** `master` is protected and one PR is merged.

## Phase 2: The App (API + Database)

**Purpose:** a real service to operate.

- [ ] `POST /shorten` stores code + long URL in Postgres
- [ ] `GET /:code` redirects and increments clicks
- [ ] `GET /stats/:code` returns the count
- [ ] `GET /health`
- [ ] Config via environment variables (no secrets in code)
- [ ] Runs locally end to end

**Learn:** REST APIs, SQL basics, DB connections, health endpoints
**Done when:** I can shorten a URL and be redirected, locally.

## Phase 3: Containers (Docker + Compose)

**Purpose:** runs identically on my laptop and on the server.

- [ ] Dockerfile for the API
- [ ] docker-compose with API + Postgres + reverse proxy
- [ ] Postgres data in a volume (survives restart)
- [ ] Secrets/config via env file (not committed)

**Learn:** images vs containers, layers, volumes, networking, env vars
**Done when:** `docker compose up` starts the whole app from scratch.

## Phase 4: CI (GitHub Actions)

**Purpose:** broken changes can't be merged.

- [ ] Tests for `/shorten`, redirect, `/stats`
- [ ] Workflow runs lint + tests + Docker build on every PR
- [ ] Branch protection requires the checks to pass
- [ ] Dependency caching

**Learn:** pipeline YAML, automated testing, status checks
**Done when:** a PR with a failing test is blocked.

---

# SHIP

## Phase 5: AWS Server (EC2), Hardened

**Purpose:** a real machine on the internet that is safe to expose.

- [ ] Launch EC2 (small instance) with an IAM role attached
- [ ] Security Group: allow only 22 (my IP only), 80, 443
- [ ] SSH keys only; non-root user; (optional) SSM Session Manager
- [ ] Install Docker
- [ ] Read auth logs and spot bot login attempts
- [ ] Run the compose stack by hand on the server

**Learn:** Linux users/permissions/logs, security groups, IAM roles, SSH
**Done when:** the app responds from the server's public IP.

## Phase 6: CD (Auto-Deploy)

**Purpose:** merge to `main` = deployed, no manual steps.

- [ ] ECR repository created
- [ ] GitHub Actions authenticates to AWS with OIDC (no stored access keys)
- [ ] On merge: build image → push to ECR → server pulls and restarts
- [ ] Deployment tagged by git commit SHA
- [ ] Practiced a rollback to the previous version

**Learn:** registries, CI secrets/OIDC, deploy over SSH/SSM, rollback
**Done when:** a merged PR changes the live app automatically.

## Phase 7: Domain, DNS, HTTPS

**Purpose:** friendly name and encrypted traffic.

- [ ] Domain bought
- [ ] Route 53 hosted zone + A record to the server
- [ ] HTTPS via Caddy (automatic certificates)
- [ ] HTTP redirects to HTTPS

**Learn:** DNS records/TTL, reverse proxy, TLS certificates
**Done when:** `https://my-domain/abc123` redirects with a valid padlock.

## Phase 8: Infrastructure as Code (Terraform)

**Purpose:** rebuild everything from code.

- [ ] Terraform state in S3 (with locking)
- [ ] EC2, security group, IAM, ECR, Route 53 record defined in code
- [ ] Changes go through PRs (`terraform plan` visible)
- [ ] `terraform destroy` then `terraform apply` rebuilds everything

**Learn:** declarative infra, state, plan vs apply, modules
**Done when:** I can recreate the whole environment with one command.

---

# RUN

## Phase 9: Monitoring and Alerting

**Purpose:** know it's broken before users tell me.

- [ ] API exposes metrics (requests, errors, redirect latency)
- [ ] Prometheus scrapes them; Grafana dashboard built
- [ ] CloudWatch logs/metrics for the instance
- [ ] External uptime check
- [ ] Alerts (down, high error rate) to Discord/email
- [ ] Triggered an alert on purpose and received it

**Learn:** metrics vs logs vs alerts, golden signals, PromQL, alert hygiene
**Done when:** stopping the API sends me an alert within minutes.

## Phase 10: SRE Practice

**Purpose:** measurable reliability and learning from failure.

- [ ] SLI/SLO written (e.g. 99.9% of redirects succeed in under 100 ms)
- [ ] Load test with k6; found the breaking point
- [ ] Failure experiments (stop DB, fill disk, kill container) and observed alerts
- [ ] Automated Postgres backups to S3
- [ ] Restored from a backup successfully
- [ ] Runbook written (`docs/runbook.md`)
- [ ] Postmortem written (`docs/postmortem-001.md`)

**Learn:** SLOs/error budgets, load testing, backup/restore, incident writing
**Done when:** I have an SLO, a tested restore, a runbook and a postmortem.

---

# Stretch Goals (After the 10 Phases)

- [ ] Move Postgres to RDS and compare with the container
- [ ] Put an ALB + ACM certificate in front, compare with Caddy
- [ ] Add rate limiting and abuse protection
- [ ] Add a second environment (staging) via Terraform

## Cost Rules

- Keep the billing alert on.
- ALB, NAT gateway and RDS cost money while running: destroy them when not in use.
- Run `terraform destroy` at the end of long breaks.

---

## Progress

| Phase | Started | Finished | Notes |
|---|---|---|---|
| 1 Git workflow | | | |
| 2 App | | | |
| 3 Containers | | | |
| 4 CI | | | |
| 5 AWS server | | | |
| 6 CD | | | |
| 7 Domain/HTTPS | | | |
| 8 Terraform | | | |
| 9 Monitoring | | | |
| 10 SRE practice | | | |
