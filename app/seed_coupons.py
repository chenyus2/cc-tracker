from db import get_db

conn = get_db()

cards = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM cards").fetchall()}

conn.execute("DELETE FROM coupons")

def monthly_credits(card_id, title, merchant, value, notes):
    """Generate 12 monthly coupon entries for 2026."""
    months = [
        ("2026-01-01", "2026-01-31"),
        ("2026-02-01", "2026-02-28"),
        ("2026-03-01", "2026-03-31"),
        ("2026-04-01", "2026-04-30"),
        ("2026-05-01", "2026-05-31"),
        ("2026-06-01", "2026-06-30"),
        ("2026-07-01", "2026-07-31"),
        ("2026-08-01", "2026-08-31"),
        ("2026-09-01", "2026-09-30"),
        ("2026-10-01", "2026-10-31"),
        ("2026-11-01", "2026-11-30"),
        ("2026-12-01", "2026-12-31"),
    ]
    entries = []
    for start, end in months:
        entries.append((card_id, title, merchant, "dollar", value, None, start, end, notes))
    return entries


coupons = []

# ============================================================
# AMEX GOLD ($325/yr) - Total credits: $424/yr
# ============================================================

# $10/mo Uber Cash ($120/yr + $5 bonus in Dec = $125/yr)
for start, end in [
    ("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28"),
    ("2026-03-01", "2026-03-31"), ("2026-04-01", "2026-04-30"),
    ("2026-05-01", "2026-05-31"), ("2026-06-01", "2026-06-30"),
    ("2026-07-01", "2026-07-31"), ("2026-08-01", "2026-08-31"),
    ("2026-09-01", "2026-09-30"), ("2026-10-01", "2026-10-31"),
    ("2026-11-01", "2026-11-30"),
]:
    coupons.append((cards["Amex Gold"], "Uber Cash Credit", "Uber / Uber Eats", "dollar", 10, None, start, end, "Monthly - auto-added to Uber account"))
coupons.append((cards["Amex Gold"], "Uber Cash Credit", "Uber / Uber Eats", "dollar", 15, None, "2026-12-01", "2026-12-31", "Monthly - $15 in December ($5 bonus)"))

# $10/mo Dining Credit ($120/yr)
coupons += monthly_credits(cards["Amex Gold"], "Dining Credit",
    "Grubhub, Seamless, Cheesecake Factory, Goldbelly, Wine.com, Five Guys, Milk Bar",
    10, "Monthly - enrollment required")

# $7/mo Dunkin Credit ($84/yr)
coupons += monthly_credits(cards["Amex Gold"], "Dunkin Credit", "Dunkin", 7, "Monthly - enrollment required")

# $50 semi-annual Resy Global Dining Access ($100/yr)
coupons.append((cards["Amex Gold"], "Resy Dining Credit (H1)", "Resy Global Dining Access restaurants", "dollar", 50, None, "2026-01-01", "2026-06-30", "Semi-annual - pay at Resy-partnered restaurants"))
coupons.append((cards["Amex Gold"], "Resy Dining Credit (H2)", "Resy Global Dining Access restaurants", "dollar", 50, None, "2026-07-01", "2026-12-31", "Semi-annual - pay at Resy-partnered restaurants"))

# ============================================================
# AMEX BLUE CASH PREFERRED ($95/yr) - Total credits: $120/yr
# ============================================================

# $10/mo Disney Streaming Credit ($120/yr)
coupons += monthly_credits(cards["Amex Blue Cash Preferred"], "Disney Bundle Credit",
    "Disney+, Hulu, ESPN+ (disneyplus.com, hulu.com, plus.espn.com)",
    10, "Monthly - including bundle subscriptions")

# ============================================================
# CHASE SAPPHIRE PREFERRED ($95/yr) - Total credits: $290/yr value
# ============================================================

# $50/yr hotel credit (Chase Travel)
coupons.append((cards["Chase Sapphire Preferred"], "Annual Hotel Credit", "Chase Travel Portal", "dollar", 50, None, "2026-01-01", "2026-12-31", "Annual - hotel bookings via Chase Travel"))

# $10/mo DoorDash credit ($120/yr) - through 12/31/2027
coupons += monthly_credits(cards["Chase Sapphire Preferred"], "DoorDash Monthly Credit",
    "DoorDash (groceries, retail, restaurants)",
    10, "Monthly promo - through 12/31/2027")

# DashPass membership (value $120/yr) - complimentary through 12/31/2027
coupons.append((cards["Chase Sapphire Preferred"], "DoorDash DashPass Membership", "DoorDash", "dollar", 0, None, "2026-01-01", "2026-12-31", "Complimentary DashPass - $0 delivery fees, reduced service fees - through 12/31/2027"))

# 5x on Lyft (through 9/30/2027)
coupons.append((cards["Chase Sapphire Preferred"], "5x Points on Lyft", "Lyft", "dollar", 0, None, "2026-01-01", "2026-12-31", "5x UR points on Lyft rides - through 9/30/2027"))

# 10% anniversary points bonus
coupons.append((cards["Chase Sapphire Preferred"], "10% Anniversary Points Bonus", "Chase", "dollar", 0, None, "2026-10-01", "2026-10-31", "10% bonus on all points earned in prior card year - auto-applied"))

# $100 Global Entry / TSA PreCheck (every 4 years)
coupons.append((cards["Chase Sapphire Preferred"], "Global Entry / TSA PreCheck Credit", "Global Entry or TSA PreCheck", "dollar", 100, None, "2026-01-01", "2026-12-31", "Once every 4 years - statement credit on application fee"))

# ============================================================
# CHASE UNITED QUEST ($250/yr) - Total credits: $660+/yr value
# ============================================================

# $200/yr United TravelBank Cash (annual, on anniversary)
coupons.append((cards["Chase United Quest"], "United TravelBank Cash", "United Airlines", "dollar", 200, None, "2026-01-01", "2026-12-31", "Annual on account anniversary - $200 deposited to TravelBank"))

# $100/yr rideshare credit ($8/mo Jan-Nov + $12 Dec)
for start, end in [
    ("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28"),
    ("2026-03-01", "2026-03-31"), ("2026-04-01", "2026-04-30"),
    ("2026-05-01", "2026-05-31"), ("2026-06-01", "2026-06-30"),
    ("2026-07-01", "2026-07-31"), ("2026-08-01", "2026-08-31"),
    ("2026-09-01", "2026-09-30"), ("2026-10-01", "2026-10-31"),
    ("2026-11-01", "2026-11-30"),
]:
    coupons.append((cards["Chase United Quest"], "Rideshare Credit", "Lyft, Uber, rideshare", "dollar", 8, None, start, end, "Monthly $8 - yearly opt-in required"))
coupons.append((cards["Chase United Quest"], "Rideshare Credit", "Lyft, Uber, rideshare", "dollar", 12, None, "2026-12-01", "2026-12-31", "Monthly $12 in December - yearly opt-in required"))

# $180/yr Instacart credit ($10 + $5 = $15/mo) - through 12/31/2027
coupons += monthly_credits(cards["Chase United Quest"], "Instacart Credit",
    "Instacart", 15, "Monthly ($10 + $5 credits) - through 12/31/2027")

# $150/yr Renowned Hotels credit (annual, on anniversary)
coupons.append((cards["Chase United Quest"], "Renowned Hotels Credit", "Chase Renowned Hotels & Resorts", "dollar", 150, None, "2026-01-01", "2026-12-31", "Annual - up to $150 back on hotel accommodations via Chase Renowned Hotels"))

# $150/yr JSX credit (annual)
coupons.append((cards["Chase United Quest"], "JSX Flight Credit", "JSX", "dollar", 150, None, "2026-01-01", "2026-12-31", "Annual - up to $150 back on JSX flights booked directly"))

# $80/yr Avis/Budget credit ($40 x 2 rentals)
coupons.append((cards["Chase United Quest"], "Avis/Budget Car Rental Credit", "Avis or Budget (via cars.united.com)", "dollar", 80, None, "2026-01-01", "2026-12-31", "Annual - $40 TravelBank cash per rental, up to 2 rentals via cars.united.com"))

# 25% back on United inflight purchases
coupons.append((cards["Chase United Quest"], "United Inflight 25% Back", "United Airlines (inflight WiFi, food, drinks)", "percent", 25, None, "2026-01-01", "2026-12-31", "Ongoing - 25% statement credit on inflight purchases"))

# 2 free checked bags
coupons.append((cards["Chase United Quest"], "2 Free Checked Bags", "United Airlines", "dollar", 0, None, "2026-01-01", "2026-12-31", "Ongoing - 2 free checked bags for you + companion on same reservation"))

# 10% off UA award flights
coupons.append((cards["Chase United Quest"], "10% Off United Award Flights", "United Airlines (MileagePlus redemptions)", "percent", 10, None, "2026-01-01", "2026-12-31", "Ongoing - 10% fewer miles needed for award flights"))

# 10,000-mile award discount (on anniversary + after $20k spend/yr)
coupons.append((cards["Chase United Quest"], "10,000-Mile Award Discount", "United Airlines", "dollar", 0, None, "2026-01-01", "2026-12-31", "Annual on anniversary + after $20k calendar year spend"))

# $100 Global Entry / TSA PreCheck
coupons.append((cards["Chase United Quest"], "Global Entry / TSA PreCheck Credit", "Global Entry or TSA PreCheck", "dollar", 100, None, "2026-01-01", "2026-12-31", "Once every 4 years"))

# ============================================================
# CITI STRATA PREMIER ($95/yr)
# ============================================================

# $100/yr hotel savings ($100 off $500+ stay)
coupons.append((cards["Citi Strata Premier"], "Annual Hotel Savings", "thankyou.com / Citi Travel", "dollar", 100, 500, "2026-01-01", "2026-12-31", "Annual - $100 off a single hotel stay of $500+ via thankyou.com"))

# $100 Global Entry / TSA PreCheck / Nexus (every 5 years)
coupons.append((cards["Citi Strata Premier"], "Global Entry / TSA PreCheck Credit", "Global Entry, TSA PreCheck, or Nexus", "dollar", 100, None, "2026-01-01", "2026-12-31", "Once every 5 years"))

# ============================================================
# CHASE FREEDOM FLEX ($0/yr)
# ============================================================

# Cell phone protection
coupons.append((cards["Chase Freedom Flex"], "Cell Phone Protection", "Cell phone bill paid with card", "dollar", 800, None, "2026-01-01", "2026-12-31", "Up to $800/claim, $1000/yr max, $50 deductible - pay monthly phone bill with this card"))

# ============================================================
# WELLS FARGO ACTIVE CASH ($0/yr)
# ============================================================

# Cell phone protection
coupons.append((cards["Wells Fargo Active Cash"], "Cell Phone Protection", "Cell phone bill paid with card", "dollar", 600, None, "2026-01-01", "2026-12-31", "Up to $600/claim, $25 deductible - pay monthly phone bill with this card"))

# ============================================================
# Cards with NO recurring credits/perks:
# - Amex Blue Cash Everyday ($0/yr) - just cashback rates
# - Apple Card ($0/yr) - just cashback rates
# - BofA Customized Cash Rewards ($0/yr) - just cashback rates
# - BofA Platinum Plus ($0/yr) - no rewards at all
# - Citi AAdvantage MileUp ($0/yr) - just miles earning
# - Discover it Cash Back ($0/yr) - just rotating categories
# - Robinhood Gold Card ($0/yr) - just 3% cashback
# - US Bank Platinum ($0/yr) - no rewards at all
# ============================================================


for card_id, title, merchant, dtype, value, min_spend, start, end, notes in coupons:
    conn.execute(
        "INSERT INTO coupons (card_id, title, merchant, discount_type, discount_value, min_spend, start_date, end_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (card_id, title, merchant, dtype, value, min_spend, start, end, notes)
    )

conn.commit()
conn.close()
print(f"Seeded {len(coupons)} credits/perks for 2026.")
