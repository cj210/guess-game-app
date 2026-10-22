import pytest
from guess_number.core import validate_guess, guess_compare

class TestValidateGuess:
    
    @pytest.mark.parametrize("inp, exp", [("Ding", 0), ("234", 0), ("0", 0), ("1", 1), ("100", 100), ("-1", 0) ])
    def test_validate_guess_method(self, inp, exp):
        
        assert validate_guess(inp) == exp

class TestGuessCompare:
    
    @pytest.mark.parametrize("inp, exp", [((20,30), "Too Low"), ((50,30), "Too High"), ((55, 55), "You got it")])
    def test_validate_guess_compare_method(self, inp, exp):
        
        assert guess_compare(*inp) == exp

        
        

    