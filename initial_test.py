import json

from json_output_inspector import repair_json

myjson = """Sure, here is the JSON you requested:
{
    "name": "John
    age: 30
    "city": "New York",
    "state": "NY",
    "zip": 10001,
    "is_active": true
    "is_admin": false,
    roles: [
        "admin",
        "user"
    ],
    "address": {
        "street": "123 Main St",
        "unit": 1
    
}"""

output = repair_json(myjson, "llama3.2", "http://host.docker.internal:11434/v1")

try:
    step1 = json.loads(output)
    print(json.dumps(step1, indent=4))
except:
    print("FAILED")
    print(output)
