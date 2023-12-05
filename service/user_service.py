class UsersService:
    def __init__(self, repository):
        self.repository = repository

    def find_by_email(self, email):
        return self.repository.find_by_email(email)

    # Create a user with provided details (name, email, password)
    def create_user(self, name, email, password):
        return self.repository.create_user_with_details(name, email, password)

    # Retrieve all users from the repository
    def get_all_users(self):
        return self.repository.read_all_users()

    # Update a user's information based on provided details (name, email, password)
    def update_user(self, user_id, name=None, email=None, password=None):
        return self.repository.update_user_with_details(user_id, name, email, password)

    # Delete a user using their ID
    def delete_user(self, user_id):
        return self.repository.delete_user(user_id)
