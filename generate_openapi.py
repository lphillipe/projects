import json
from car_api.app import app

schema = app.openapi()

with open("openapi.json", "w") as f:
    json.dump(schema, f, indent=2)

print("openapi.json gerado com sucesso!")