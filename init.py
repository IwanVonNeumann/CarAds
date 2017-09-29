from db.init_db import init_db
from transformation.format_raw import format_raw_records

# sections = get_sections_list()

# for section in sections:
#     store_section(section, "pages/sections")

# store_ads(r"pages\ads")


init_db()
format_raw_records()
