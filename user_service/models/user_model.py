class User:
    users = []
    id_counter = 1

    @classmethod
    def get_all_users(cls):
        return cls.users

    @classmethod
    def create_user(cls, username, email):
        user = {
            "id": cls.id_counter,
            "username": username,
            "email": email
        }
        cls.users.append(user)
        cls.id_counter += 1
        return user
