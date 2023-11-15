def main():
    import os

    username = os.environ.get("username")
    password = os.environ.get("password")
    country = os.environ.get("country")
    site = os.environ.get("site")
    print("site: ", site, "country: ", country, "user:", username, "pwd:", password)