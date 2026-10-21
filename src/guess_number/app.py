from guess_number.core import generate_secret, validate_guess, guess_compare, runner, user_continue


def main() -> None:
    play_again: bool  = True
    while play_again:
        secret: int = generate_secret()
        for i in range(5,0,-1):
            won: bool = runner(secret)
            if won:
                break
            print(f"{i-1} attemps remaining" if i > 1 else f"Its {secret}. Game over!!")
                
        play_again = user_continue()

    
            
main()
            
