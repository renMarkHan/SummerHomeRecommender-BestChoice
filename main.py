from database import create_tables
from user import create_user, User
import database


def main():
    print("🏝 Welcome to Vacation Rentals CLI 🏝")
    create_tables()

    # 1. Collect user info
    name = input("Enter your name: ")
    group_size = int(input("Enter your group size: "))
    preferred_env = input("Preferred environment (mountain/lake/beach/city): ")
    budget_min = float(input("Minimum budget per night: "))
    budget_max = float(input("Maximum budget per night: "))
    travel_start_date = input("Travel start date (YYYY-MM-DD, optional): ") or None
    travel_end_date = input("Travel end date (YYYY-MM-DD, optional): ") or None

    # 2. Store user in DB
    user_id = create_user(name, group_size, preferred_env, budget_min, budget_max, travel_start_date, travel_end_date)
    print(f"✅ User profile created with ID: {user_id}")

    # 3. Load user object from DB (to use match method)
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    current_user = User(
        user_id=row[0],
        name=row[1],
        group_size=row[2],
        preferred_env=row[3],
        budget_min=row[4],
        budget_max=row[5],
        travel_start_date=row[6],
        travel_end_date=row[7]
    )

    # 4. Match properties
    matches = current_user.match_properties()

    if matches:
        print("\n🎯 We found these matching properties for you:")
        for p in matches:
            print(p)
    else:
        print("\n❌ No matching properties found for your preferences.")


if __name__ == "__main__":
    main()
