class User:
    def __init__(self, id: int, email: str, password_hash: str, is_active: bool = True ):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active

    def change_password(self, new_hash: str):
        if new_hash == self.password_hash:
            raise ValueError("New password can't be the same as old one")
        elif new_hash is None:
            raise ValueError("New password can't be empty")
        self.password_hash = new_hash
        
    def deactivate(self):
        if self.is_active is False:
            raise ValueError("User is already deactivated")
        self.is_active = False

    def activate(self):
        if self.is_active is True:
            raise ValueError("User is already activated")
        self.is_active = True