# 8-13. User Profile

def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first.title()
    user_info['last_name'] = last.title()
    return user_info

# Build a profile about yourself
user_profile = build_profile(
    'kendall', 
    'hazzard',
    location='new jersey',
    hobby='football',
    goal='to become a forensic scientist'
)

print(user_profile)