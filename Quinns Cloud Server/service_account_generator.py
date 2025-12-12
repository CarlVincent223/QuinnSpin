import json
import base64

with open("quinns-laundry-house-5d121-cad4a86b8589.json", 'r') as file:
    ServAccKey_data = json.load(file)

json_string = json.dumps(ServAccKey_data)
json_bytes = json_string.encode('utf-8')
base64_bytes = base64.b64encode(json_bytes)
base64_string = base64_bytes.decode('utf-8')
print(base64_string)