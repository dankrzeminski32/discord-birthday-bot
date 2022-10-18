from datetime import datetime
from pytz import timezone
import pytz    
# Current time in UTC
now_utc = datetime.now(timezone('America/Chicago'))

print(now_utc.day, now_utc.month)