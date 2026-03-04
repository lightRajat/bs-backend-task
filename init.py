from app.models import Base, Contact
from app.utils import log
import csv
from datetime import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

def create_db(db_path: str = "data.db") -> None:
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    log("Database created successfully.")

def load_sample_data(sample_data_path: str = "sample-data.csv", db_path: str = "data.db") -> None:
    engine = create_engine(f"sqlite:///{db_path}")
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
    if os.path.exists("data.db"):
        option = input("Database already exists. Do you want to reset? (y/n): ")
        if option.lower() == "y":
            os.remove("data.db")
        else:
            os._exit(0)

    create_db()
    load_sample_data()
