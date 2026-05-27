from db import get_db

conn = get_db()

cards = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM cards").fetchall()}

conn.execute("DELETE FROM benefits")

benefits = [
    # Chase Freedom Flex
    (cards["Chase Freedom Flex"], "Cell Phone Protection", "Up to $800/claim, $1000/yr max, $50 deductible - pay monthly phone bill with this card"),

    # Wells Fargo Active Cash
    (cards["Wells Fargo Active Cash"], "Cell Phone Protection", "Up to $600/claim, $25 deductible - pay monthly phone bill with this card"),

    # Chase Sapphire Preferred
    (cards["Chase Sapphire Preferred"], "DoorDash DashPass Membership", "Complimentary DashPass - $0 delivery fees, reduced service fees - through 12/31/2027"),
    (cards["Chase Sapphire Preferred"], "10% Anniversary Points Bonus", "10% bonus on all points earned in prior card year - auto-applied"),

    # Chase United Quest
    (cards["Chase United Quest"], "25% Back on United Inflight Purchases", "25% statement credit on inflight WiFi, food, drinks"),
    (cards["Chase United Quest"], "2 Free Checked Bags", "For you + companion on same reservation"),
    (cards["Chase United Quest"], "10% Off United Award Flights", "10% fewer miles needed for award flights"),
    (cards["Chase United Quest"], "10,000-Mile Award Discount", "On anniversary + after $20k calendar year spend"),
]

for card_id, title, description in benefits:
    conn.execute(
        "INSERT INTO benefits (card_id, title, description) VALUES (?, ?, ?)",
        (card_id, title, description)
    )

conn.commit()
conn.close()
print(f"Seeded {len(benefits)} card benefits.")
