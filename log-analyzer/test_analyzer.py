import pytest
from analyzer import parse_line

def test_valid_line():
    line = "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created"
    data, err = parse_line(line)
    assert err is None
    assert data['level'] == 'WARN'

def test_invalid_time():
    line = "not-a-timestamp | ERROR | orders-api | ORDER_REJECTED | timestamp is invalid"
    data, err = parse_line(line)
    assert err is not None
    assert "Неверный формат времени" in err

def test_invalid_level():
    line = "2026-09-02T08:12:00Z | NOTICE | gateway | HTTP_502 | unsupported level"
    data, err = parse_line(line)
    assert err is not None
    assert "Неверный уровень" in err

def test_empty_field():
    line = "2026-09-03T09:00:00Z | INFO | auth-api | | missing event code"
    data, err = parse_line(line)
    assert err is not None
    assert "Неверное количество полей" in err
