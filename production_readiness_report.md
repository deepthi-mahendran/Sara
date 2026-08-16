# Sara — Production Readiness Analysis

A comprehensive audit of every layer of the project, identifying **blockers**, **high-priority issues**, and **improvements** needed before this can safely handle real users and real money.

---

## 🔴 P0 — Critical Blockers (Must Fix Before Production)

### 1. In-Memory Auth State Will Not Survive Restarts or Scale

| File | Lines | Issue |
|------|-------|-------|
| [`auth.py`](file:///c:/Users/LENOVO/Downloads/Portfolio%20pieces/Sara/backend/app/api/auth.py#L29-L30) | 29-30 | `failed_login_attempts = OrderedDict()` — stored in process memory |
| [`auth.py`](file:///c:/Users/LENOVO/Downloads/Portfolio%20pieces/Sara/backend/app/api/auth.py#L45) | 45 | `active_refresh_jtis: dict[str, str] = {}` — refresh token JTI store is in-memory |
| [`telemetry.py`](file:///c:/Users/LENOVO/Downloads/Portfolio%20pieces/Sara/backend/app/api/telemetry.py#L12) | 12 | `rum_telemetry_store = []` — telemetry buffer in process memory |
| [`websocket_cart.py`](file:///c:/Users/LENOVO/Downloads/Portfolio%20pieces/Sara/backend/app/api/websocket_cart.py#L59) | 59 | `manager = ConnectionManager()` — WebSocket state in-memory |

**Impact**: 
- Server restart = all refresh tokens invalidated, all login attempt counts reset, all WebSocket sessions dropped, all telemetry lost.
- Multi-worker deployment (Gunicorn with multiple workers, Kubernetes pods) = each worker has its own `active_refresh_jtis`, so a refresh token created by worker A fails validation on worker B.
- Brute-force protection is trivially bypassed by restarting the server.

**Fix**: Move to Redis for session state (refresh JTIs, login attempts, rate limiting). Store telemetry in PostgreSQL or a time-series DB.

---

### 2. Receipt Verification is a Brute-Force Timing Oracle

```python
# receipts.py:47-63
@router.get("/verify-receipt/{signature}")
def verify_digital_receipt(signature: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).order_by(models.Order.id.desc()).limit(200).all()
    for order in orders:
        expected = generate_receipt_signature(order)
        if hmac.compare_digest(expected, signature):
            return { ... order details including email, name, amount ... }
    return {"valid": False}
```

**Issues**:
- **No authentication required** — anyone can call this endpoint
- **Iterates over 200 orders** per request — O(n) scan that leaks timing information
- **Exposes PII** (customer name, email, order amount) to unauthenticated callers
- **No rate limiting** on `verify-receipt` (only `get_digital_receipt` has it)

---

### 3. WebSocket Cart Has No Authentication

```python
# websocket_cart.py:62-65
@router.websocket("/ws/cart/{session_id}")
async def shared_cart_websocket(websocket: WebSocket, session_id: str):
    user_id = websocket.query_params.get("user_id", "anon_" + session_id[:4])
    user_name = websocket.query_params.get("user_name", "Shopper " + user_id[-3:])
```

**Issues**:
- Anyone can connect to any `session_id` and inject cart modifications
- User identity comes from **unauthenticated query params** — trivially spoofable
- No JWT validation on WebSocket connection
- A malicious user can join any shared cart and add/remove items

---

### 4. Hardcoded Fallback Secret Key in Receipts

```python
# receipts.py:12
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_secret_key_for_dev")
```

**Issue**: If `SECRET_KEY` env var is unset, receipts are signed with a publicly-known key. The main `auth.py` correctly crashes on missing `SECRET_KEY`, but `receipts.py` silently degrades.

---

### 5. `.env` File Committed to Git

```
# .env (658 bytes) is in the repo root AND backend/.env
SECRET_KEY=change-me-in-production-use-secrets-token-hex
POSTGRES_PASSWORD=sara
```

**Issue**: Even though it's a placeholder value, the `.env` file is tracked in git. The `.gitignore` lists `.env` but the file was committed before `.gitignore` was added.

**Fix**: `git rm --cached .env backend/.env` and ensure they never re-enter.

---

### 6. No HTTPS Enforcement in Docker Stack

```nginx
# nginx.conf:1-2
server {
    listen 80;
```

The Nginx container only listens on HTTP port 80. There is no TLS termination, no HTTPS redirect, and no SSL certificate configuration. The backend sets `Strict-Transport-Security` headers but the actual transport is unencrypted.

---

## 🟠 P1 — High Priority (Should Fix Before Launch)

### 7. Float Type for Financial Amounts

```python
# models.py:34, 91, 130
price = Column(Float)
total_amount = Column(Float, nullable=False)
price = Column(Float, nullable=False)
```

**Issue**: IEEE 754 floats cause rounding errors with money. `0.1 + 0.2 ≠ 0.3`. Over thousands of transactions, amounts will drift.

**Fix**: Use `Numeric(precision=10, scale=2)` / `DECIMAL` for all monetary columns.

---

### 8. No Payment Gateway Integration

The checkout flow creates orders and deducts inventory but **never charges the customer**. There is no Stripe, Razorpay, or any payment processing. Orders are marked `CONFIRMED` without payment verification.

**Impact**: Real money cannot flow through this system.

---

### 9. Coupon System is Hardcoded

```python
# orders.py:244
COUPONS = {"SARA20": 20, "WELCOME10": 10}
```

**Issues**:
- Coupons are static Python constants, not database-backed
- No usage limits, no per-user limits, no expiry dates
- Coupon name `SARA20` is from the pre-rebrand era
- No coupon creation/management API
- Discount is applied on subtotal but validated only on the backend — a mismatch could confuse users

---

### 10. No Database Connection Pooling Configuration

```python
# database.py:25-27
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
```

**Issue**: No `pool_size`, `max_overflow`, `pool_timeout`, or `pool_recycle` configured. Under load, the default pool (5 connections) will exhaust quickly, causing 500 errors.

---

### 11. No Input Sanitization on HTML-Rendered Fields

Order fields like `full_name`, `address`, `city` are stored raw and returned in API responses. If any downstream consumer renders these in HTML without escaping, it's an XSS vector.

---

### 12. Inventory Reservation Has No Cleanup Scheduler

```python
# inventory_lock.py:91-103 — POST /release-expired
def release_expired_reservations(db: Session = Depends(get_db)):
```

Expired inventory holds are only cleaned up when:
1. Another reservation is made for the same product (line 32-36)
2. Someone manually calls `POST /release-expired`

There is **no background scheduler** (cron, Celery beat, or APScheduler) to periodically sweep expired holds. Stale holds will silently reduce available stock.

---

### 13. Admin API Has No Admin Users

The admin endpoints correctly check `user.role == "ADMIN"`, but:
- There is no user management API to promote users to admin
- There is no seed script to create an initial admin user
- There is no admin UI frontend
- The only way to create an admin is to manually update the database

---

### 14. Email Delivery is Non-Functional by Default

```python
# auth.py:50
SMTP_HOST = os.environ.get("SMTP_HOST", "")
```

SMTP is unconfigured by default. The forgot-password flow falls back to **returning the reset token directly in the API response** — acceptable for development but a critical security issue in production (tokens in HTTP responses, browser history, server logs).

---

### 15. No Logging Infrastructure

- Backend uses `logging.getLogger(__name__)` but has no configured log handler, formatter, or log level
- No structured logging (JSON format for log aggregation)
- No request ID tracking for correlating logs across a request lifecycle
- No error tracking service integration (Sentry, etc.)
- Frontend `console.log`/`console.error` with no remote error reporting

---

## 🟡 P2 — Important Improvements

### 16. Frontend-Backend Integration is Incomplete

The frontend `app.js` (91 KB) contains **hardcoded product data** — products are defined as JavaScript arrays, not fetched from the `/api/products` endpoint. The backend has a full product API but the frontend doesn't consume it.

Similarly:
- Cart operations are client-side only (localStorage) — not synced with backend
- User authentication UI exists but may not fully integrate with JWT cookie flow
- Order tracking page exists but mock data may be used instead of real API calls

---

### 17. ~458 KB of Redundant CSS

| File | Size | Issue |
|------|------|-------|
| `style.css` | 124 KB | Main stylesheet |
| `global.css` | 108 KB | Heavily overlaps with `style.css` |
| `style.min.css` | 113 KB | Pre-minified copy (Vite handles this) — unreferenced |
| `bundle.css` | 113 KB | Another bundled copy — unreferenced |

Both `style.css` and `global.css` are loaded on every page, creating massive rule duplication.

---

### 18. 53 Dead JavaScript Files (~195 KB)

As identified in the previous analysis — 53 JS files in `frontend/js/` are never imported or referenced by any HTML page. They inflate the repo and confuse the project structure.

---

### 19. No Automated Testing for Backend

- **117 unit tests** exist for the frontend (Vitest), which is good
- **Zero tests** for the backend Python API (the `tests/api.test.js` is a JS file, not Python)
- No pytest test suite for auth, orders, inventory, pricing, etc.
- The `requirements.txt` includes `pytest` and `httpx` but no test files exist

---

### 20. No Database Seeding

There is no script to populate the products table with initial data. The frontend shows products from hardcoded JS arrays, but the backend API would return an empty list on a fresh database.

---

### 21. No CI/CD Pipeline

- No GitHub Actions, GitLab CI, or any CI configuration
- No automated linting, testing, or deployment on push
- No build verification before merge

---

### 22. Docker Compose Uses Default Credentials

```yaml
# docker-compose.yml:5-7
POSTGRES_USER: ${POSTGRES_USER:-sara}
POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-sara}
POSTGRES_DB: ${POSTGRES_DB:-sara_db}
```

Default password is `sara` — discoverable from the public repo.

---

### 23. No Database Backup Strategy

No backup script, no pg_dump cron, no WAL archiving, no point-in-time recovery configuration.

---

### 24. No API Versioning

All endpoints are at `/api/*` with no version prefix. Breaking changes will affect all consumers simultaneously.

---

### 25. WebAuthn/Passkey Implementation is Incomplete

```python
# auth.py:539
public_key_dump = raw_response.get("attestationObject") or cred_id
```

The WebAuthn registration:
- Does **not** verify the attestation object cryptographically
- Does **not** validate the challenge (the challenge from `register-options` is not stored server-side for verification)
- Stores raw `attestationObject` as a string, not parsed
- Login verify does not check signatures — it only verifies the credential ID exists

This is a **mock WebAuthn implementation** that accepts any credential without cryptographic verification.

---

### 26. No Rate Limiting on Several Sensitive Endpoints

| Endpoint | Has Rate Limit? |
|----------|----------------|
| `POST /register` | ✅ 5/min |
| `POST /login` | ✅ 5/min |
| `POST /forgot-password` | ✅ 5/min |
| `POST /reset-password` | ✅ 5/min |
| `GET /verify-receipt/{sig}` | ❌ No |
| `POST /release-expired` | ❌ No |
| `GET /api/products/*` | ❌ No |
| `GET /api/orders/*` | ❌ No |
| `POST /api/telemetry/rum` | ❌ No |
| `WebSocket /ws/cart/*` | ❌ No |

---

### 27. No CORS Restriction on Telemetry Endpoint

`POST /api/telemetry/rum` accepts arbitrary payloads with no authentication. An attacker could flood it with junk data, consuming the 1000-entry in-memory buffer and polluting metrics.

---

### 28. Service Worker Caching Strategy Needs Review

The `service-worker.js` (5 KB) caches pages for offline use, but:
- Cache invalidation strategy is unclear
- May serve stale product pages with outdated prices/stock
- No cache versioning visible

---

## 📋 Missing Features for Production E-Commerce

| Feature | Status | Priority |
|---------|--------|----------|
| Payment Gateway (Stripe/Razorpay) | ❌ Missing | P0 |
| Email Notifications (order confirmation, shipping) | ❌ SMTP unconfigured | P1 |
| Admin Dashboard UI | ❌ Missing (API exists, no frontend) | P1 |
| Product Image Upload/Management | ❌ Images are static files | P1 |
| Inventory Management UI | ❌ Missing | P1 |
| Order Fulfillment Workflow | ⚠️ Partial (status transitions exist, no shipping integration) | P1 |
| Customer Reviews & Ratings (backend) | ❌ Missing (frontend has `reviews.js` but no API) | P2 |
| Returns & Refunds Processing | ⚠️ Partial (return deadline computed but no refund flow) | P2 |
| Tax Calculation (region-specific) | ⚠️ Hardcoded 18% GST | P2 |
| Shipping Provider Integration | ❌ Hardcoded flat rate | P2 |
| Product Variants (size/color per SKU) | ❌ Missing | P2 |
| Analytics Dashboard | ⚠️ Partial (admin API exists, no UI) | P2 |
| SEO (sitemap.xml, robots.txt, SSR) | ⚠️ Partial (meta tags exist, no sitemap) | P2 |
| GDPR Compliance (data export/deletion) | ❌ Missing | P2 |
| Accessibility Audit (WCAG 2.1 AA) | ⚠️ A11y utilities exist, not verified | P2 |

---

## 📊 Summary by Priority

| Priority | Count | Effort Estimate |
|----------|-------|-----------------|
| 🔴 **P0 — Blockers** | 6 issues | ~2-3 weeks |
| 🟠 **P1 — High Priority** | 9 issues | ~3-4 weeks |
| 🟡 **P2 — Improvements** | 13 issues | ~4-6 weeks |
| **Total** | **28 issues** | **~9-13 weeks** |

> [!CAUTION]
> The project has a solid foundation — good database schema design, proper BOLA authorization checks, idempotent order creation, row-level inventory locking, and refresh token rotation. However, the **in-memory auth state** (P0 #1) and **lack of payment processing** (P1 #8) are fundamental blockers that must be resolved before handling any real traffic or money.
