from database import get_connection, get_all_properties_df
from property import Property
import numpy as np
import pandas as pd


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
        return self.budget_min <= nightly_price <= self.budget_max

    def match_properties(self, w_afford, w_pref_env):
        
        total = w_afford + w_pref_env
        if  total == 0 :
            w_afford = 1
            w_pref_env = 0
        else :
            w_afford = w_afford / total
            w_pref_env = w_pref_env/total
        
        print(w_afford)
        print(w_pref_env)
        print(self.preferred_env)
        

        all_props = get_all_properties_df()
        budget = (self.budget_max + self.budget_min) / 2  # Average budget
        prices = all_props["nightly_price"].to_numpy(dtype=float)
        afford = np.clip((budget - prices) / max(budget, 0.001), 0.0, 1.0)

        if self.preferred_env:
            env = np.array(
                [1.0 if self.preferred_env.lower() in [tag.lower() for tag in tags] else 0.0 for tags in all_props["tags"]],
                dtype=float
            )
        else:
            env = np.zeros(len(all_props), dtype=float)

        all_props["afford_score"] = afford
        all_props["env_score"] = env
        all_props["match_score"] = (
            w_afford * all_props["afford_score"] +
            w_pref_env * all_props["env_score"]
        )

        return all_props.sort_values("match_score", ascending=False)


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

# ==============================
# Useful function
# ==============================


def get_importance(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 10:
                return value / 10
            else:
                print("Please enter a number between 0 and 10.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
