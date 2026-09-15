def pull_user_data(sp):
    user_data = sp.current_user()
    user_name = user_data["display_name"]
    try:
        user_pfp = user_data["images"][0]["url"]
    except:
        user_pfp = None
    return user_name, user_pfp