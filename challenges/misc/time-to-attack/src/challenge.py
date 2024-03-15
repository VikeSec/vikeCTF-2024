from time import sleep

FLAG = r"vikeCTF{T1MIN6_A77@CK5_4R3_FUN}"
PASSWORD = "dxse465r78"


def check_password(password: str, user_input: str) -> bool:
    index = 0

    while index < min(len(password), len(user_input)):
        if password[index] != user_input[index]:
            return False
        else:
            index += 1
            sleep(0.5)

    return len(password) == len(user_input)


if __name__ == "__main__":
    user_input = input("Welcome! Enter password to login: ")
    if check_password(PASSWORD, user_input):
        print("Login succesful: " + FLAG)
    else:
        print("Login failed")
