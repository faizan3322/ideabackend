from app import db
from app import Contact

# Fetch and print all contacts
contacts = Contact.query.all()
for contact in contacts:
    print(contact.name, contact.email, contact.message)

# Count total contacts
print("Total contacts:", Contact.query.count())

# Get a specific record
record = Contact.query.get(1)
if record:
    print(record.name, record.email, record.message)
else:
    print("Record not found")
