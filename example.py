from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

toy = scanner.find_toy()
print(toy)
with SpheroEduAPI(toy) as api:
    api.spin(360, 10)