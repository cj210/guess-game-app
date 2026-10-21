from random import randint


def generate_secret() -> int:
    return randint(1,100)

def validate_guess(n: str) -> int:
    if n.isnumeric():
        if int(n) > 0 and int(n) < 101:
            return int(n)
    print("Not a valid number")
    return 0

def guess_compare(guess: int, secret: int) -> str:
    if guess > secret:
        return "Too High"
    if guess < secret:
        return "Too Low"
    return "You got it"

def runner(secret: int) -> bool:
    # print(f"secret: {secret}")
    guess: int  = 0
    while not guess:
        user_input: str = input("Enter number between 1 and 100: ")
        guess: int = validate_guess(user_input)
    message: str = guess_compare(guess, secret)
    print(message)
    return message == "You got it"
    
def user_continue() -> bool:
    continue_option: str = input("Do you wish to play again? y/n: ")
    if continue_option.lower() in ('y', 'yes'):
        return True
    return False
    


