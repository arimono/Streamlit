import time
from models import selectAll

refresh_interval = 5
# Main loop
while True:
    # Fetch data from your DB
    data, column_names = selectAll("sensor")
    print(len(data))
    print("refreshed")
    time.sleep(refresh_interval)
    
