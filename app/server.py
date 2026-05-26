from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
from db import get_db, init_db

app = Flask(__name__)


def get_cards():
    conn = get_db()
    cards = [dict(r) for r in conn.execute("SELECT * FROM cards ORDER BY issuer, name").fetchall()]
    conn.close()
    return cards


def get_categories():
    conn = get_db()
    cats = [dict(r) for r in conn.execute("SELECT * FROM categories ORDER BY name").fetchall()]
    conn.close()
    return cats


@app.route("/")
def dashboard():
    cards = get_cards()
    categories = get_categories()
    conn = get_db()
    today = date.today().isoformat()

    best = []
    for cat in categories:
        rows = conn.execute("""
            SELECT r.*, c.name as card_name, c.issuer
            FROM rewards r
            JOIN cards c ON r.card_id = c.id
            WHERE r.category_id = ?
            AND (r.start_date IS NULL OR r.start_date <= ?)
            AND (r.end_date IS NULL OR r.end_date >= ?)
            ORDER BY r.reward_percent DESC
        """, (cat["id"], today, today)).fetchall()
        if rows:
            ranking = []
            for row in rows:
                ranking.append({
                    "card": row["card_name"],
                    "issuer": row["issuer"],
                    "percent": row["reward_percent"],
                    "type": row["reward_type"],
                    "notes": row["notes"],
                })
            best.append({
                "category": cat["name"],
                "category_id": cat["id"],
                "top": ranking[0],
                "ranking": ranking,
            })

    active_coupons = [dict(r) for r in conn.execute("""
        SELECT co.*, c.name as card_name
        FROM coupons co
        JOIN cards c ON co.card_id = c.id
        WHERE co.used = 0
        AND (co.end_date IS NULL OR co.end_date >= ?)
        ORDER BY co.end_date ASC
    """, (today,)).fetchall()]

    week_from_now = (date.today() + timedelta(days=7)).isoformat()
    expiring_soon = [c for c in active_coupons if c.get("end_date") and c["end_date"] <= week_from_now]

    total_annual_fees = sum(c.get("annual_fee") or 0 for c in cards)

    today_d = date.today()
    for card in cards:
        if card.get("open_date"):
            try:
                opened = datetime.strptime(card["open_date"], "%Y-%m-%d").date()
                delta = today_d - opened
                years = delta.days // 365
                months = (delta.days % 365) // 30
                card["age"] = f"{years}y {months}m"
            except ValueError:
                card["age"] = "-"
        else:
            card["age"] = "-"

    conn.close()
    return render_template("dashboard.html",
                           cards=cards,
                           categories=categories,
                           best=best,
                           active_coupons=active_coupons,
                           total_annual_fees=total_annual_fees)


@app.route("/cards")
def cards_page():
    cards = get_cards()
    conn = get_db()
    for card in cards:
        rewards = [dict(r) for r in conn.execute("""
            SELECT r.*, cat.name as category_name
            FROM rewards r
            JOIN categories cat ON r.category_id = cat.id
            WHERE r.card_id = ?
            ORDER BY r.reward_percent DESC
        """, (card["id"],)).fetchall()]
        card["rewards"] = rewards
    conn.close()
    categories = get_categories()
    return render_template("cards.html", cards=cards, categories=categories)


@app.route("/api/cards", methods=["POST"])
def add_card():
    data = request.form
    conn = get_db()
    conn.execute(
        "INSERT INTO cards (name, issuer, last_four, annual_fee, open_date, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (data["name"], data.get("issuer"), data.get("last_four"),
         float(data.get("annual_fee") or 0),
         data.get("open_date") or None, data.get("notes"))
    )
    conn.commit()
    conn.close()
    return redirect(url_for("cards_page"))


@app.route("/api/cards/<int:card_id>/update", methods=["POST"])
def update_card(card_id):
    data = request.form
    conn = get_db()
    conn.execute("""
        UPDATE cards SET name=?, issuer=?, last_four=?, annual_fee=?, open_date=?, notes=?
        WHERE id=?
    """, (data["name"], data.get("issuer"), data.get("last_four"),
          float(data.get("annual_fee") or 0),
          data.get("open_date") or None, data.get("notes"), card_id))
    conn.commit()
    conn.close()
    return redirect(url_for("cards_page"))


@app.route("/api/cards/<int:card_id>/delete", methods=["POST"])
def delete_card(card_id):
    conn = get_db()
    conn.execute("DELETE FROM rewards WHERE card_id = ?", (card_id,))
    conn.execute("DELETE FROM coupons WHERE card_id = ?", (card_id,))
    conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("cards_page"))


@app.route("/api/rewards", methods=["POST"])
def add_reward():
    data = request.form
    conn = get_db()
    conn.execute(
        "INSERT INTO rewards (card_id, category_id, reward_type, reward_percent, start_date, end_date, is_rotating, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (int(data["card_id"]), int(data["category_id"]), data.get("reward_type", "cashback"),
         float(data["reward_percent"]), data.get("start_date") or None,
         data.get("end_date") or None, 1 if data.get("is_rotating") else 0,
         data.get("notes"))
    )
    conn.commit()
    conn.close()
    return redirect(url_for("cards_page"))


@app.route("/api/rewards/<int:reward_id>/delete", methods=["POST"])
def delete_reward(reward_id):
    conn = get_db()
    conn.execute("DELETE FROM rewards WHERE id = ?", (reward_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("cards_page"))


@app.route("/api/categories", methods=["POST"])
def add_category():
    name = request.form.get("name", "").strip()
    if name:
        conn = get_db()
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
    return redirect(url_for("cards_page"))


@app.route("/coupons")
def coupons_page():
    cards = get_cards()
    conn = get_db()
    today = date.today().isoformat()
    show_hidden = request.args.get("show_hidden") == "1"

    hidden_filter = "" if show_hidden else "AND co.hidden = 0"

    # Current month boundaries
    today_d = date.today()
    month_start = today_d.replace(day=1).isoformat()
    if today_d.month == 12:
        next_month_start = today_d.replace(year=today_d.year + 1, month=1, day=1).isoformat()
    else:
        next_month_start = today_d.replace(month=today_d.month + 1, day=1).isoformat()
    month_end = (datetime.strptime(next_month_start, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

    # This month: end_date falls within current month OR end_date covers current month (semi-annual/annual that haven't been used yet)
    this_month = [dict(r) for r in conn.execute(f"""
        SELECT co.*, c.name as card_name
        FROM coupons co JOIN cards c ON co.card_id = c.id
        WHERE co.used = 0
        AND co.start_date <= ?
        AND co.end_date >= ?
        AND co.end_date <= ?
        {hidden_filter}
        ORDER BY co.end_date ASC
    """, (today, today, month_end)).fetchall()]

    # This period (semi-annual/annual that span beyond this month but are currently active)
    this_period = [dict(r) for r in conn.execute(f"""
        SELECT co.*, c.name as card_name
        FROM coupons co JOIN cards c ON co.card_id = c.id
        WHERE co.used = 0
        AND co.start_date <= ?
        AND co.end_date > ?
        AND co.end_date >= ?
        {hidden_filter}
        ORDER BY co.end_date ASC
    """, (today, month_end, today)).fetchall()]

    # Future months: starts after this month
    future = [dict(r) for r in conn.execute(f"""
        SELECT co.*, c.name as card_name
        FROM coupons co JOIN cards c ON co.card_id = c.id
        WHERE co.used = 0
        AND co.start_date >= ?
        {hidden_filter}
        ORDER BY co.start_date ASC, co.end_date ASC
    """, (next_month_start,)).fetchall()]

    active = this_month + this_period + future

    hidden_count = conn.execute("""
        SELECT COUNT(*) FROM coupons
        WHERE used = 0 AND hidden = 1 AND (end_date IS NULL OR end_date >= ?)
    """, (today,)).fetchone()[0]

    used = [dict(r) for r in conn.execute("""
        SELECT co.*, c.name as card_name
        FROM coupons co JOIN cards c ON co.card_id = c.id
        WHERE co.used = 1
        ORDER BY co.used_date DESC LIMIT 50
    """).fetchall()]

    expired = [dict(r) for r in conn.execute(f"""
        SELECT co.*, c.name as card_name
        FROM coupons co JOIN cards c ON co.card_id = c.id
        WHERE co.used = 0 AND co.end_date < ?
        {hidden_filter}
        ORDER BY co.end_date DESC LIMIT 50
    """, (today,)).fetchall()]

    conn.close()
    return render_template("coupons.html", cards=cards, active=active,
                           this_month=this_month, this_period=this_period, future=future,
                           used=used, expired=expired,
                           show_hidden=show_hidden, hidden_count=hidden_count)


@app.route("/api/coupons", methods=["POST"])
def add_coupon():
    data = request.form
    conn = get_db()
    conn.execute(
        "INSERT INTO coupons (card_id, title, merchant, discount_type, discount_value, min_spend, start_date, end_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (int(data["card_id"]), data["title"], data.get("merchant"),
         data.get("discount_type", "percent"),
         float(data["discount_value"]) if data.get("discount_value") else None,
         float(data["min_spend"]) if data.get("min_spend") else None,
         data.get("start_date") or None, data.get("end_date") or None,
         data.get("notes"))
    )
    conn.commit()
    conn.close()
    return redirect(url_for("coupons_page"))


@app.route("/api/coupons/<int:coupon_id>/use", methods=["POST"])
def use_coupon(coupon_id):
    conn = get_db()
    conn.execute("UPDATE coupons SET used = 1, used_date = ? WHERE id = ?",
                 (date.today().isoformat(), coupon_id))
    conn.commit()
    conn.close()
    return redirect(url_for("coupons_page"))


@app.route("/api/coupons/<int:coupon_id>/hide", methods=["POST"])
def hide_coupon(coupon_id):
    conn = get_db()
    conn.execute("UPDATE coupons SET hidden = 1 WHERE id = ?", (coupon_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("coupons_page"))


@app.route("/api/coupons/<int:coupon_id>/unhide", methods=["POST"])
def unhide_coupon(coupon_id):
    conn = get_db()
    conn.execute("UPDATE coupons SET hidden = 0 WHERE id = ?", (coupon_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("coupons_page", show_hidden="1"))


@app.route("/api/coupons/hide-by-title", methods=["POST"])
def hide_by_title():
    title = request.form.get("title")
    card_id = request.form.get("card_id", type=int)
    conn = get_db()
    if card_id:
        conn.execute("UPDATE coupons SET hidden = 1 WHERE title = ? AND card_id = ?", (title, card_id))
    else:
        conn.execute("UPDATE coupons SET hidden = 1 WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    return redirect(url_for("coupons_page"))


@app.route("/api/coupons/<int:coupon_id>/delete", methods=["POST"])
def delete_coupon(coupon_id):
    conn = get_db()
    conn.execute("DELETE FROM coupons WHERE id = ?", (coupon_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("coupons_page"))


def seed_if_empty():
    """Seed cards/rewards/coupons on first run if DB is empty."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
    conn.close()
    if count == 0:
        import subprocess
        import sys
        import os
        app_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run([sys.executable, os.path.join(app_dir, "seed_cards.py")], check=True)
        subprocess.run([sys.executable, os.path.join(app_dir, "seed_rewards.py")], check=True)
        subprocess.run([sys.executable, os.path.join(app_dir, "seed_coupons.py")], check=True)
        print("Database seeded.")


init_db()
seed_if_empty()

if __name__ == "__main__":
    app.run(debug=True, port=5556)
