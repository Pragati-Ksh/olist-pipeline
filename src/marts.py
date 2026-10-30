from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/olist.db")

with open("sql/marts.sql") as f:
    statements = [s.strip() for s in f.read().split(";") if s.strip()]

with engine.begin() as conn:
    for s in statements:
        conn.execute(text(s))

print("Created", len([s for s in statements if s.startswith("CREATE")]), "summary tables")