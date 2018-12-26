from db.init_db import init_db
from scrap.download import store_everything
from transformation.format_raw import format_raw_records

# store_everything()


init_db()
format_raw_records()
