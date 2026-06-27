import pytest
from betting import get_situation
from deckclass import Players

hero = Players()
hero.type = "HERO"

villain = Players()
villain.type = "VILLAIN"

villain2 = Players()
villain2.type = "VILLAIN"

def test_get_situationRfi():
    num_raises= 0
    first_raiser = None
    current_player = None
    hero_was_last_raiser = False

    assert get_situation(0, None, None, False) == "rfi"

def test_get_situationFacingRfi():
    assert get_situation(1, None, None, True) == "facingRfi"
    assert get_situation(1, None, None, False) == "facingRfi"

def test_get_situationRfivs3bet():
    assert get_situation(2, hero, hero, True) ==  "rfi_vs_3bet"

def test_get_situation2():
    """
    This one test the villain face 3 bet after he raises
    """
    assert get_situation(2, villain, villain, False) == "rfi_vs_3bet"

def test_get_situation3():
    """
    This test for fallbacks
    """
    assert get_situation(2, None, hero, False) == "facingRfi"

def test_get_situation4():
    """
    This test is for fallback with villain and villain
    """
    assert get_situation(2, villain2, villain, False) == "facingRfi"