from db import get_db, init_db

cards = [
    {"name": "Amex Gold", "issuer": "AMEX", "open_date": "2019-05-02", "annual_fee": 325},
    {"name": "Amex Blue Cash Everyday", "issuer": "AMEX", "open_date": "2022-11-05", "annual_fee": 0},
    {"name": "Amex Blue Cash Preferred", "issuer": "AMEX", "open_date": "2022-04-27", "annual_fee": 95},
    {"name": "Apple Card", "issuer": "APPLE", "open_date": "2019-08-12", "annual_fee": 0},
    {"name": "BofA Customized Cash Rewards", "issuer": "BANK OF AMERICA", "open_date": "2025-12-08", "annual_fee": 0},
    {"name": "BofA Platinum Plus", "issuer": "BANK OF AMERICA", "open_date": "2024-01-03", "annual_fee": 0},
    {"name": "Citi AAdvantage MileUp", "issuer": "CITI", "open_date": "2020-11-25", "annual_fee": 0},
    {"name": "Citi Strata Premier", "issuer": "CITI", "open_date": "2021-11-07", "annual_fee": 95},
    {"name": "Discover it Cash Back", "issuer": "DISCOVER", "open_date": "2019-01-14", "annual_fee": 0},
    {"name": "Chase United Quest", "issuer": "CHASE", "open_date": "2022-10-19", "annual_fee": 250},
    {"name": "Chase Sapphire Preferred", "issuer": "CHASE", "open_date": "2020-10-12", "annual_fee": 95},
    {"name": "Chase Freedom Flex", "issuer": "CHASE", "open_date": "2021-05-10", "annual_fee": 0},
    {"name": "Robinhood Gold Card", "issuer": "ROBINHOOD", "open_date": "2025-02-11", "annual_fee": 0},
    {"name": "US Bank Platinum", "issuer": "US BANK", "open_date": "2023-10-09", "annual_fee": 0},
    {"name": "Wells Fargo Active Cash", "issuer": "WELLS FARGO", "open_date": "2024-08-26", "annual_fee": 0},
]

if __name__ == "__main__":
    init_db()
    conn = get_db()
    conn.execute("DELETE FROM cards")
    conn.execute("DELETE FROM rewards")
    conn.execute("DELETE FROM coupons")
    for card in cards:
        conn.execute(
            "INSERT INTO cards (name, issuer, open_date, annual_fee) VALUES (?, ?, ?, ?)",
            (card["name"], card["issuer"], card["open_date"], card["annual_fee"])
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(cards)} cards.")
