from api.main import app
from fastapi.routing import APIRoute

print(f"{'METHOD':<10} {'PATH':<40} {'NAME'}")
print("-" * 80)

for route in app.routes:
    if isinstance(route, APIRoute):
        methods = ", ".join(route.methods or [])
        print(f"{methods:<10} {route.path:<40} {route.name}")

print("updated")