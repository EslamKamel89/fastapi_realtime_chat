# 🧠 WebSockets in Practice — FastAPI (Backend-First)

A backend-focused realtime messaging system built to understand **how distributed systems behave under pressure**.

This is not a feature demo.
It is an architectural exercise disguised as a chat app.

---

## 🚀 What This Project Demonstrates

This project intentionally explores:

- ✅ WebSocket lifecycle in FastAPI
- ✅ Async SQLAlchemy session ownership
- ✅ Multi-worker process isolation
- ✅ Redis Pub/Sub as coordination (not storage)
- ✅ Database as durable truth
- ✅ At-least-once delivery semantics
- ✅ Failure scenarios (worker restarts, duplicates, ordering)

It is built to surface the difference between:

- Persistence vs Delivery
- Memory vs Process
- Coordination vs Durability
- Transport vs Business Logic

---

## 🏗️ Core Architecture

**Database** → Durable truth
**Redis (Pub/Sub)** → Ephemeral coordination
**WebSockets** → Transport only
**FastAPI lifespan** → Infrastructure ownership

The system runs correctly with:

```

uvicorn core.main:app --workers 2

```

Without Redis, multi-worker broadcasting fails.
With Redis, workers coordinate properly.

That boundary is the entire point.

---

## 🧩 Structure

```

core/
main.py # App lifecycle
database.py # Async DB engine
redis.py # Redis infrastructure
redis_listeners.py # Background subscriber
ws_registery.py # WebSocket adapter

apps/
auth/ # User model
messages/ # Message model + repository

templates/
index.html # Minimal UI to stress backend

```

---

## 🧪 Run Locally

1. Install dependencies
2. Provide `.env`:

```

DATABASE_URL=sqlite+aiosqlite:///./app.db
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0

```

3. Start Redis
4. Run:

```

uvicorn core.main:app --workers 2

```

Open two browser windows and observe behavior.

---

## 🎯 Purpose

This repository was built to:

- Develop production-grade backend thinking
- Understand distributed system boundaries
- Prepare for backend interviews (EU market)

It focuses on reasoning, not UI polish.

---

## 🏁 Final Note

This is not a chat app.

It is a distributed systems lab wearing a chat UI.
