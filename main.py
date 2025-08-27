from database import create_tables
from user import create_user, User
import database


def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("🏝 Vacation Rentals CLI Menu 🏝")
    print("="*50)
    print("1. Create User Profile")
    print("2. Edit Profile")
    print("3. View Properties")
    print("4. Get Recommendations")
    print("5. Exit")
    print("="*50)


def create_user_menu():
    """Handle user creation menu."""
    print("\n📝 Creating New User Profile")
    print("-" * 30)
    
    name = input("Enter your name: ")
    group_size = int(input("Enter your group size: "))
    preferred_env = input("Preferred environment (mountain/lake/beach/city): ")
    budget_min = float(input("Minimum budget per night: "))
    budget_max = float(input("Maximum budget per night: "))
    travel_start_date = input("Travel start date (YYYY-MM-DD, optional): ") or None
    travel_end_date = input("Travel end date (YYYY-MM-DD, optional): ") or None

    # Store user in DB
    user_id = create_user(name, group_size, preferred_env, budget_min, budget_max, travel_start_date, travel_end_date)
    print(f"✅ User profile created with ID: {user_id}")
    
    return user_id


def edit_profile_menu():
    """Handle profile editing menu."""
    print("\n✏️ Edit User Profile")
    print("-" * 30)
    
    # First, we need to find the user to edit
    # For simplicity, we'll ask for user ID
    # In a real app, you might want to search by name or email
    try:
        user_id = int(input("Enter your user ID: "))
        
        # Get current user data
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            print("❌ User not found!")
            return
        
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
        
        print(f"Current profile: {current_user}")
        print("\nEnter new values (press Enter to keep current value):")
        
        new_name = input(f"Name [{current_user.name}]: ") or current_user.name
        new_group_size = input(f"Group size [{current_user.group_size}]: ") or current_user.group_size
        new_preferred_env = input(f"Preferred environment [{current_user.preferred_env}]: ") or current_user.preferred_env
        new_budget_min = input(f"Minimum budget [{current_user.budget_min}]: ") or current_user.budget_min
        new_budget_max = input(f"Maximum budget [{current_user.budget_max}]: ") or current_user.budget_max
        new_travel_start = input(f"Travel start date [{current_user.travel_start_date}]: ") or current_user.travel_start_date
        new_travel_end = input(f"Travel end date [{current_user.travel_end_date}]: ") or current_user.travel_end_date
        
        # Update user in database
        cursor.execute('''
            UPDATE users 
            SET name=?, group_size=?, preferred_env=?, budget_min=?, budget_max=?, travel_start_date=?, travel_end_date=?
            WHERE user_id=?
        ''', (new_name, int(new_group_size), new_preferred_env, float(new_budget_min), 
              float(new_budget_max), new_travel_start, new_travel_end, user_id))
        
        conn.commit()
        conn.close()
        
        print("✅ Profile updated successfully!")
        
    except ValueError:
        print("❌ Invalid user ID!")
    except Exception as e:
        print(f"❌ Error updating profile: {e}")


def view_properties_menu():
    """Handle viewing properties menu."""
    print("\n🏠 Available Properties")
    print("-" * 30)
    
    try:
        all_properties = database.get_all_properties()
        
        if not all_properties:
            print("❌ No properties found in the database.")
            return
        
        for i, prop in enumerate(all_properties, 1):
            print(f"{i}. {prop}")
            if hasattr(prop, 'features') and prop.features:
                print(f"   Features: {', '.join(prop.features)}")
            if hasattr(prop, 'tags') and prop.tags:
                print(f"   Tags: {', '.join(prop.tags)}")
            print()
            
    except Exception as e:
        print(f"❌ Error loading properties: {e}")


def get_recommendations_menu():
    """Handle getting recommendations menu."""
    print("\n🎯 Get Personalized Recommendations")
    print("-" * 40)
    
    try:
        user_id = int(input("Enter your user ID: "))
        
        # Get user data
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            print("❌ User not found!")
            return
        
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
        
        print(f"Finding recommendations for: {current_user.name}")
        print(f"Preferences: {current_user.preferred_env} environment, Budget: ${current_user.budget_min}-${current_user.budget_max}/night")
        
        # Get matches
        matches = current_user.match_properties()
        
        if matches:
            print(f"\n🎯 We found {len(matches)} matching properties for you:")
            print("-" * 50)
            for i, prop in enumerate(matches, 1):
                print(f"{i}. {prop}")
                if hasattr(prop, 'features') and prop.features:
                    print(f"   Features: {', '.join(prop.features)}")
                if hasattr(prop, 'tags') and prop.tags:
                    print(f"   Tags: {', '.join(prop.tags)}")
                print()
        else:
            print("\n❌ No matching properties found for your preferences.")
            print("Try adjusting your budget or preferred environment.")
            
    except ValueError:
        print("❌ Invalid user ID!")
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")


def main():
    """Main application loop."""
    print("🏝 Welcome to Vacation Rentals CLI 🏝")
    create_tables()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                create_user_menu()
            elif choice == "2":
                edit_profile_menu()
            elif choice == "3":
                view_properties_menu()
            elif choice == "4":
                get_recommendations_menu()
            elif choice == "5":
                print("\n👋 Thank you for using Vacation Rentals CLI! Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
