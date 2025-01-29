from fastapi.security import HTTPBearer

security_scheme = HTTPBearer(bearerFormat="JWT")
