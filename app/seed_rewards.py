from db import get_db

conn = get_db()

cards = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM cards").fetchall()}
cats = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM categories").fetchall()}

conn.execute("DELETE FROM rewards")

# Updated to current (2025) card terms
rewards = [
    # Amex Gold - $325/yr, 4x dining worldwide, 4x US groceries (up to $25k/yr), 3x flights booked directly, 1x other
    (cards["Amex Gold"], cats["Dining"], "points", 4, None),
    (cards["Amex Gold"], cats["Groceries"], "points", 4, "Up to $25k/yr"),
    (cards["Amex Gold"], cats["Travel"], "points", 3, "Flights booked directly with airline"),
    (cards["Amex Gold"], cats["Other"], "points", 1, None),

    # Amex Blue Cash Everyday - $0/yr, 3% groceries (up to $6k/yr), 3% gas, 3% online retail, 1% other
    (cards["Amex Blue Cash Everyday"], cats["Groceries"], "cashback", 3, "Up to $6k/yr then 1%"),
    (cards["Amex Blue Cash Everyday"], cats["Gas"], "cashback", 3, None),
    (cards["Amex Blue Cash Everyday"], cats["Online Shopping"], "cashback", 3, "Up to $6k/yr"),
    (cards["Amex Blue Cash Everyday"], cats["Other"], "cashback", 1, None),

    # Amex Blue Cash Preferred - $95/yr, 6% groceries (up to $6k/yr), 6% streaming, 3% transit, 3% gas, 1% other
    (cards["Amex Blue Cash Preferred"], cats["Groceries"], "cashback", 6, "Up to $6k/yr then 1%"),
    (cards["Amex Blue Cash Preferred"], cats["Streaming"], "cashback", 6, None),
    (cards["Amex Blue Cash Preferred"], cats["Transit"], "cashback", 3, "Including rideshare, parking, tolls"),
    (cards["Amex Blue Cash Preferred"], cats["Gas"], "cashback", 3, None),
    (cards["Amex Blue Cash Preferred"], cats["Other"], "cashback", 1, None),

    # Apple Card - $0/yr, 3% Apple/select merchants (Uber, Nike, Walgreens, etc.), 2% Apple Pay, 1% physical
    (cards["Apple Card"], cats["Online Shopping"], "cashback", 3, "Apple Store, Nike, Uber, T-Mobile, Walgreens, etc."),
    (cards["Apple Card"], cats["Transit"], "cashback", 3, "Uber, ride-share via Apple Pay"),
    (cards["Apple Card"], cats["Drug Stores"], "cashback", 3, "Walgreens only"),
    (cards["Apple Card"], cats["Wholesale Clubs"], "cashback", 2, "Via Apple Pay"),
    (cards["Apple Card"], cats["Other"], "cashback", 2, "Via Apple Pay; 1% with physical card"),

    # BofA Customized Cash Rewards - $0/yr, 3% choice category (currently Dining), 2% grocery/wholesale, 1% other ($2500/qtr combined cap on bonus categories)
    (cards["BofA Customized Cash Rewards"], cats["Dining"], "cashback", 3, "Choice category - $2500/qtr combined cap"),
    (cards["BofA Customized Cash Rewards"], cats["Groceries"], "cashback", 2, "$2500/qtr cap"),
    (cards["BofA Customized Cash Rewards"], cats["Wholesale Clubs"], "cashback", 2, "$2500/qtr cap"),
    (cards["BofA Customized Cash Rewards"], cats["Other"], "cashback", 1, None),

    # BofA Platinum Plus - $0/yr, no rewards (just 0% intro APR card)

    # Citi AAdvantage MileUp - $0/yr, 2x AA miles on American Airlines, 2x groceries, 1x other
    (cards["Citi AAdvantage MileUp"], cats["Travel"], "miles", 2, "American Airlines purchases only"),
    (cards["Citi AAdvantage MileUp"], cats["Groceries"], "miles", 2, None),
    (cards["Citi AAdvantage MileUp"], cats["Other"], "miles", 1, None),

    # Citi Strata Premier - $95/yr (renamed from Premier in 2024), 3x air/hotels/restaurants/supermarkets/gas/EV/streaming, 1x other
    (cards["Citi Strata Premier"], cats["Travel"], "points", 3, "Air travel & hotels"),
    (cards["Citi Strata Premier"], cats["Dining"], "points", 3, None),
    (cards["Citi Strata Premier"], cats["Groceries"], "points", 3, "Supermarkets"),
    (cards["Citi Strata Premier"], cats["Gas"], "points", 3, "Includes EV charging"),
    (cards["Citi Strata Premier"], cats["Streaming"], "points", 3, None),
    (cards["Citi Strata Premier"], cats["Other"], "points", 1, None),

    # Discover it Cash Back - $0/yr, 5% rotating quarterly categories (must activate), 1% other
    # Note: First year cashback match effectively doubles to 10%/2%
    (cards["Discover it Cash Back"], cats["Other"], "cashback", 1, "5% rotating quarterly - must activate each quarter"),

    # Chase United Quest - $250/yr, 3x United, 2x all other travel/dining/streaming, 1x other
    (cards["Chase United Quest"], cats["Travel"], "miles", 3, "United purchases; 2x other travel"),
    (cards["Chase United Quest"], cats["Dining"], "miles", 2, None),
    (cards["Chase United Quest"], cats["Streaming"], "miles", 2, "Select streaming services"),
    (cards["Chase United Quest"], cats["Other"], "miles", 1, None),

    # Chase Sapphire Preferred - $95/yr, 5x Chase Travel, 5x Lyft, 3x dining/streaming/online grocery, 2x other travel, 1x other
    (cards["Chase Sapphire Preferred"], cats["Travel"], "points", 5, "Chase Travel portal; 2x other travel bookings"),
    (cards["Chase Sapphire Preferred"], cats["Transit"], "points", 5, "Lyft only (through 9/30/2027); 2x Uber & other rideshare"),
    (cards["Chase Sapphire Preferred"], cats["Dining"], "points", 3, None),
    (cards["Chase Sapphire Preferred"], cats["Streaming"], "points", 3, "Select streaming"),
    (cards["Chase Sapphire Preferred"], cats["Groceries"], "points", 3, "Online grocery delivery only"),
    (cards["Chase Sapphire Preferred"], cats["Other"], "points", 1, None),

    # Chase Freedom Flex - $0/yr, 5% rotating quarterly (activate), 5% Chase Travel, 3% dining, 3% drugstores, 1% other
    (cards["Chase Freedom Flex"], cats["Dining"], "cashback", 3, None),
    (cards["Chase Freedom Flex"], cats["Drug Stores"], "cashback", 3, None),
    (cards["Chase Freedom Flex"], cats["Travel"], "cashback", 5, "Chase Travel portal only"),
    (cards["Chase Freedom Flex"], cats["Other"], "cashback", 1, "Plus 5% rotating quarterly - activate each quarter"),

    # Robinhood Gold Card - $0 card fee (requires Gold $5/mo or $50/yr), 3% on all purchases
    (cards["Robinhood Gold Card"], cats["Dining"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Groceries"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Gas"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Travel"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Online Shopping"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Streaming"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Transit"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Drug Stores"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Wholesale Clubs"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Utilities"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Home Improvement"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Entertainment"], "cashback", 3, None),
    (cards["Robinhood Gold Card"], cats["Other"], "cashback", 3, "Requires Robinhood Gold ($5/mo)"),

    # US Bank Platinum - $0/yr, no rewards (0% intro APR card)

    # Wells Fargo Active Cash - $0/yr, flat 2% cash back on all purchases
    (cards["Wells Fargo Active Cash"], cats["Dining"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Groceries"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Gas"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Travel"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Online Shopping"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Streaming"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Wholesale Clubs"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Utilities"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Home Improvement"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Entertainment"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Transit"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Drug Stores"], "cashback", 2, None),
    (cards["Wells Fargo Active Cash"], cats["Other"], "cashback", 2, None),
]

for card_id, cat_id, rtype, pct, notes in rewards:
    conn.execute(
        "INSERT INTO rewards (card_id, category_id, reward_type, reward_percent, notes) VALUES (?, ?, ?, ?, ?)",
        (card_id, cat_id, rtype, pct, notes)
    )

conn.commit()
conn.close()
print(f"Seeded {len(rewards)} reward rules (corrected to current terms).")
