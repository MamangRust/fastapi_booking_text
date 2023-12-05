class TextUsersRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    # Create a user entry and append it to the file
    def create_user(self, user_info):
        with open(self.file_path, "a") as file:
            file.write(user_info + "\n")

    # Read all user entries from the file
    def read_all_users(self):
        with open(self.file_path, "r") as file:
            return file.readlines()

    def find_by_email(self, email):
        users = self.read_all_users()
        for user_info in users:
            user_info_data = user_info.strip().split(", ")
            user_email = user_info_data[1].split(": ")[1]
            if user_email == email:
                user = {}
                for info in user_info_data:
                    key, value = info.split(": ")
                    user[key.strip()] = value.strip()

                return user  # Return the user entry if found
        return None  # Return None if user entry is not found

    # Create a user entry with detailed information
    def create_user_with_details(self, name, email, password):
        user_info = f"Name: {name}, Email: {email}, Password: {password}"
        self.create_user(user_info)

    # Update an existing user entry with detailed information
    def update_user_with_details(self, user_id, name=None, email=None, password=None):
        users = self.read_all_users()
        if 0 <= user_id < len(users):
            user_info = users[user_id].strip().split(", ")
            updated_info = {
                "Name": name if name else user_info[0].split(": ")[1],
                "Email": email if email else user_info[1].split(": ")[1],
                "Password": password if password else user_info[2].split(": ")[1],
            }

            # Construct updated user information
            updated_user_info = f"Name: {updated_info['Name']}, Email: {updated_info['Email']}, Password: {updated_info['Password']}\n"

            # Update the user entry in the file
            users[user_id] = updated_user_info
            with open(self.file_path, "w") as file:
                file.writelines(users)
        else:
            print("User ID out of range.")

    # Delete a user entry based on the provided user_id
    def delete_user(self, user_id):
        users = self.read_all_users()
        if 0 <= user_id < len(users):
            del users[user_id]
            with open(self.file_path, "w") as file:
                file.writelines(users)
        else:
            print("User ID out of range.")
