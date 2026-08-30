from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

app = FastAPI(title="PR-Pilot Target App")

# ✅ PATCH P1 (SEC-01): Secret resolved from environment at call time — no plain-text credentials in source.
# ✅ PATCH P2 (SEC-02 / SEC-03): Reusable auth dependency injected into all protected routes.
_bearer_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme)):
    api_key = os.environ.get("INTERNAL_SYSTEM_API_KEY")
    if not api_key or credentials.credentials != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid or missing token")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/user-data")
def get_user_data(auth: None = Depends(verify_token)):
    """Returns sensitive user metrics — protected by bearer token auth."""
    return {"user": "admin", "metrics": "highly_confidential_financials"}

# ✅ PATCH P3 (SEC-04): Bare pass replaced with structured HTTPException (Manifest §2).
@app.get("/api/v1/compute")
def compute_metrics(factor: int = 0, auth: None = Depends(verify_token)):
    try:
        result = 100 / factor
        return {"calculated_factor": result}
    except ZeroDivisionError:
        raise HTTPException(status_code=500, detail="Computation error: factor must be a non-zero integer")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal computation error: {exc}")
