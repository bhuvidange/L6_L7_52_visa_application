import math

from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee


# ---------- Step 3: "must not crash" fuzz tests (arbitrary text / None) ----------

@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    try:
        parse_application(s)
    except Exception as e:
        assert False, f"parse_application crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    try:
        processing_average(s)
    except Exception as e:
        assert False, f"processing_average crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r} for input {s!r}"


# ---------- Extra properties: structured inputs and result sanity ----------

@given(st.text() | st.none() | st.integers() | st.lists(st.integers()))
def test_all_functions_accept_any_type(x):
    for fn in (parse_application, processing_average, payable_fee):
        try:
            fn(x)
        except Exception as e:
            assert False, f"{fn.__name__} crashed with: {e!r} for input {x!r}"


@given(st.text(alphabet=st.characters(blacklist_characters=":"), max_size=20),
       st.integers(min_value=0, max_value=10**6))
def test_parse_application_valid_roundtrip(visa, n):
    result = parse_application(f"{visa}:{n}")
    if visa.strip():
        assert result == (visa.strip().title(), n)
    else:
        assert result is None


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_processing_average_within_bounds(days):
    avg = processing_average(",".join(map(str, days)))
    assert min(days) <= avg <= max(days)


@given(st.floats(min_value=0, max_value=1e9, allow_nan=False),
       st.floats(min_value=0, max_value=1e9, allow_nan=False))
def test_payable_fee_never_negative(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None
    assert math.isfinite(result) and result >= 0
