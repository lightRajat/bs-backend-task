from app.models import Base, Contact
from app.utils import log
import csv
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session
import sys
load_dotenv()

def create_db(engine) -> None:
    Base.metadata.create_all(engine)
    log("Database created successfully.")

def load_sample_data(engine, sample_data_path: str = "sample-data.csv") -> None:
    session = Session(engine)

    with open(sample_data_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contact = Contact(
                phoneNumber=row["phoneNumber"] if row["phoneNumber"] else None,
                email=row["email"] if row["email"] else None,
                linkedId=int(row["linkedId"]) if row["linkedId"] else None,
                linkPrecedence=row["linkPrecedence"],
                createdAt=datetime.fromisoformat(row["createdAt"]),
                updatedAt=datetime.fromisoformat(row["updatedAt"]),
                deletedAt=None if not row["deletedAt"] else datetime.fromisoformat(row["deletedAt"])
            )
            session.add(contact)

    session.commit()
    session.close()
    log("Sample data loaded successfully.")

if __name__ == "__main__":
    engine = create_engine(os.getenv("DATABASE_URL"))

    if inspect(engine).has_table("Contact", schema="public"):
        if len(sys.argv) > 1 and sys.argv[1] == "--reset":
            with engine.connect() as conn:
                conn.execute(text('TRUNCATE TABLE "Contact" RESTART IDENTITY CASCADE'))
                conn.commit()
        else:
            os._exit(0)

    create_db(engine)
    load_sample_data(engine)
