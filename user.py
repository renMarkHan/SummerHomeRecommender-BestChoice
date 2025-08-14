from database import get_connection, get_all_properties
from property import Property

class User:
    def __init__(self, user_id, name, group_size, preferred_env, budget_min, budget_max, travel_start_date=None, travel_end_date=None):
        self.user_id = user_id
        self.name = name
        self.group_size = group_size
        self.preferred_env = preferred_env
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.travel_start_date = travel_start_date
        self.travel_end_date = travel_end_date

    def __repr__(self):
        return f"<User {self.name}, Group size: {self.group_size}, Pref: {self.preferred_env}>"

    def can_afford(self, nightly_price):
        """Check if a price is within user's budget."""
        return self.budget_min <= nightly_price <= self.budget_max

    def match_properties(self):
        """Return a list of Property objects matching the user's budget and preferred environment."""
        all_props = get_all_properties()
    
        matched = [
            prop for prop in all_props
            if self.can_afford(prop.nightly_price) 
            and prop.matches_environment(self.preferred_env)
        ]
    
        return matched

# ==============================
# CRUD Operations for Users (CRUD refers to create, read, update and delete)
# ==============================

def create_user(name, group_size, preferred_env, budget_min, budget_max, travel_start_date=None, travel_end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, group_size, preferred_env, budget_min, budget_max, travel_start_date, travel_end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, group_size, preferred_env, budget_min, budget_max, travel_start_date, travel_end_date))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


