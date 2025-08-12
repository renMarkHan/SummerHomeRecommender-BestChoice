from database import create_tables
from user import User, create_user
from property import Property, create_property

def seed_users():
    """
    Seed the database with sample users using the User class.
    """
    # Create sample User objects
    users = [
        User(None, "Alice", 4, "mountain", 100, 200, "2025-08-01", "2025-08-07"),
        User(None, "Bob", 2, "beach", 80, 150, None, None),
        User(None, "Charlie", 5, "city", 120, 250, "2025-09-10", "2025-09-20")
    ]

    # Insert each user into the database using the create_user function
    for u in users:
        create_user(
            u.name,
            u.group_size,
            u.preferred_env,
            u.budget_min,
            u.budget_max,
            u.travel_start_date,
            u.travel_end_date
        )

def seed_properties():
    """
    Seed the database with sample properties using the Property class.
    """
    # Create sample Property objects
    properties = [
        Property(None, "Aspen", "cabin", 180, "WiFi,Hot Tub", "mountain,remote"),
        Property(None, "Miami", "condo", 140, "WiFi,Pool", "beach,nightlife"),
        Property(None, "Toronto", "house", 200, "Pet Friendly,WiFi", "city,family-friendly")
    ]

    # Insert each property into the database using the create_property function
    for p in properties:
        create_property(
            p.location,
            p.type,
            p.nightly_price,
            p.features,
            p.tags
        )

if __name__ == "__main__":
    """
    Create tables and seed the database with test data.
    """
    create_tables()
    seed_users()
    seed_properties()
    print("Database seeded with test data ✅")
