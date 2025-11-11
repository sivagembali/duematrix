from models import db, Cycle
from datetime import date
from app import create_app


def seed_cycles():
    # Create tables if they don't exist
    db.create_all()

    existing = Cycle.query.all()
    if existing:
        print(f"{len(existing)} cycles already exist. Skipping seeding.")
        return

    cycles = [
        Cycle(cycle_name='Q1-2025', start_date=date(2025, 1, 1), end_date=date(2025, 3, 31), status='active'),
        Cycle(cycle_name='Q2-2025', start_date=date(2025, 4, 1), end_date=date(2025, 6, 30), status='upcoming'),
        Cycle(cycle_name='Q3-2025', start_date=date(2025, 7, 1), end_date=date(2025, 9, 30), status='upcoming'),
    ]

    for c in cycles:
        db.session.add(c)

    db.session.commit()
    print(f"Inserted {len(cycles)} cycles.")


if __name__ == '__main__':
    # Ensure we run inside Flask application context so SQLAlchemy has access to app config
    app = create_app()
    with app.app_context():
        seed_cycles()
