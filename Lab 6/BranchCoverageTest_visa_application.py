"""Branch coverage tests for visa_application.py.

Goal: make every decision (if / elif / else) evaluate both True and False,
and check the boundary values on each comparison.
Run with:
    coverage run --branch -m pytest BranchCoverageTest_visa_application.py
    coverage report -m
"""
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ======================= visa_fee =======================

# --- input validation: True and False sides ---

def test_unknown_visa_type_raises():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 1, "normal", "B")


def test_negative_entries_raises():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_zero_entries_is_valid():
    # entries == 0 is the boundary of `entries < 0` (False side)
    assert visa_fee("tourist", 0, "normal", "B") == 0


# --- nationality bonus: `group == "A" and visa_type != "student"` ---

def test_group_a_non_student_gets_bonus_entry():
    # tourist 1 + bonus 1 = 2 included -> 2 entries are free
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_group_a_student_gets_no_bonus():
    # student 2 included, no bonus -> 4 entries = 2 extra at 40
    assert visa_fee("student", 4, "normal", "A") == 80


def test_group_b_gets_no_bonus():
    # tourist 1 included -> 2 entries = 1 extra at 40
    assert visa_fee("tourist", 2, "normal", "B") == 40


# --- `extra <= 0` ---

def test_exactly_included_entries_free():
    # business includes 3; extra == 0 is the boundary
    assert visa_fee("business", 3, "express", "B") == 0


def test_one_extra_entry_charged():
    # extra == 1 just past the boundary, express rate
    assert visa_fee("business", 4, "express", "B") == 100


# --- speed and bulk surcharge: all four combinations ---

def test_normal_speed_small_order():
    # extra 3, no bulk -> 3 * 40
    assert visa_fee("tourist", 4, "normal", "B") == 120


def test_express_small_order():
    # extra 3, no bulk -> 3 * 100
    assert visa_fee("tourist", 4, "express", "B") == 300


def test_normal_speed_bulk_order():
    # extra 6 (>5) -> rate 40 + 20 = 60, no express add-on
    assert visa_fee("tourist", 7, "normal", "B") == 6 * 60


def test_express_bulk_order():
    # extra 6 (>5) -> rate 100 + 20 + 10 = 130
    assert visa_fee("tourist", 7, "express", "B") == 6 * 130


def test_extra_exactly_five_no_surcharge():
    # extra == 5 is the boundary of `extra > 5` (False side)
    assert visa_fee("tourist", 6, "normal", "B") == 5 * 40


def test_unrecognised_speed_uses_normal_rate():
    # anything other than "express" falls into the else branch
    assert visa_fee("tourist", 2, "standard", "B") == 40


# ======================= documents_complete =======================

def test_renewal_with_form():
    assert documents_complete(1, 0, True) is True


def test_renewal_without_form():
    assert documents_complete(0, 5, True) is False


def test_new_application_too_few_photos():
    assert documents_complete(3, 1, False) is False


def test_new_application_complete():
    # photos == 2 and forms == 3 are both boundaries
    assert documents_complete(3, 2, False) is True


def test_new_application_too_few_forms():
    assert documents_complete(2, 2, False) is False


# ======================= application_status =======================
# cutoff: express 10 / normal 30, plus 15 in peak season.
# open if days >= cutoff, closing if days >= cutoff - 15, else closed.

@pytest.mark.parametrize(
    "days_left, is_express, is_peak, expected",
    [
        # normal, off-peak (cutoff 30)
        (30, False, False, "open"),
        (29, False, False, "closing"),
        (15, False, False, "closing"),
        (14, False, False, "closed"),
        # express, off-peak (cutoff 10)
        (10, True, False, "open"),
        (9, True, False, "closing"),
        (-5, True, False, "closing"),
        (-6, True, False, "closed"),
        # normal, peak (cutoff 45)
        (45, False, True, "open"),
        (30, False, True, "closing"),
        (29, False, True, "closed"),
        # express, peak (cutoff 25)
        (25, True, True, "open"),
        (10, True, True, "closing"),
        (9, True, True, "closed"),
    ],
)
def test_application_status(days_left, is_express, is_peak, expected):
    assert application_status(days_left, is_express, is_peak) == expected
