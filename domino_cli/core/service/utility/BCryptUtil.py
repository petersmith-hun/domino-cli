import bcrypt

PASSWORD_ENCODING = "utf8"


def encrypt(raw_value: str) -> str:
    """
    Utility function to encrypt arbitrary values using BCrypt.

    :param raw_value: input string to be encrypted
    :return: BCrypt-encrypted value as string
    """
    encrypted_password_as_byte_array: bytes = bcrypt.hashpw(raw_value.encode(PASSWORD_ENCODING), bcrypt.gensalt())

    return encrypted_password_as_byte_array.decode(PASSWORD_ENCODING)
