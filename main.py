from fastapi import FastAPI

app = FastAPI(title="Fastapi Realtime Chat 🗨️")


@app.get("/health")
async def health():
    return {"status": "ok"}
