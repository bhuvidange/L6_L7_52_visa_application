"""Line (code) coverage tests for visa_application.py.

Goal: execute every line of the module at least once.
Run with:
    coverage run -m pytest CodeCoverageTest_visa_application.py
    coverage report -m
"""
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------- visa_fee ----------

def test_within_included_entries():
    # tourist includes 1 entry, so 1 entry costs nothing
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_unknown_visa_type_raises():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 1, "normal", "B")


def test_negative_entries_raises():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_group_a_bonus_entry_normal_speed():
    # tourist 1 + group A bonus 1 = 2 included; 4 entries -> 2 extra at 40
    assert visa_fee("tourist", 4, "normal", "A") == 80


def test_express_with_bulk_surcharge():
    # business includes 3; 10 entries -> 7 extra (>5)
    # rate = 100 (express) + 20 (bulk) + 10 (express bulk) = 130
    assert visa_fee("business", 10, "express", "B") == 7 * 130


# ---------- documents_complete ----------

def test_documents_complete():
    assert documents_complete(3, 2, False) is True


def test_renewal_needs_one_form():
    assert documents_complete(1, 0, True) is True


def test_too_few_photos():
    assert documents_complete(3, 1, False) is False


# ---------- application_status ----------

def test_status_open_express_peak():
    # express cutoff 10 + peak 15 = 25; 30 days left -> open
    assert application_status(30, True, True) == "open"


def test_status_closing_normal():
    # normal cutoff 30; 20 days left is within 15 of cutoff -> closing
    assert application_status(20, False, False) == "closing"


def test_status_closed_normal():
    # normal cutoff 30; 5 days left is below 15 -> closed
    assert application_status(5, False, False) == "closed"
