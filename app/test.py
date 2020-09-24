import json

with open("C:/Users/Jeevs/ccm-backend/app/geojson/uk.ac.cam.kings.geojson") as f:
    status = json.load(f)

print(status)