import pytest

from app.services.policies.dwfq import suggest_next


def test_empty_queue_returns_none():
    assert suggest_next([]) is None


def test_single_normal_customer_is_selected():
    customer = {"id": "normal", "vulnerability_score": 0.0, "wait_minutes": 10.0}
    assert suggest_next([customer]) is customer


def test_single_group_selects_highest_effective_priority():
    lower = {"id": "lower", "vulnerability_score": 0.8, "wait_minutes": 0.0}
    higher = {"id": "higher", "vulnerability_score": 1.2, "wait_minutes": 0.0}
    assert suggest_next([lower, higher]) is higher


def test_normal_priority_selection_when_fairness_ratio_is_within_limit():
    vulnerable = {"id": "vulnerable", "vulnerability_score": 0.6, "wait_minutes": 0.0}
    normal = {"id": "normal", "vulnerability_score": 0.0, "wait_minutes": 5.0}
    assert suggest_next([normal, vulnerable]) is vulnerable


def test_fairness_override_selects_longer_waiting_group():
    normal = {"id": "normal-long-wait", "vulnerability_score": 0.0, "wait_minutes": 40.0}
    vulnerable = {"id": "vulnerable-short-wait", "vulnerability_score": 1.0, "wait_minutes": 1.0}

    # Without the override, the vulnerable customer has higher individual priority:
    # 1.02 versus 0.80. Group average wait ratio is 40:1, above the default 1.5.
    assert suggest_next([normal, vulnerable]) is normal


def test_ratio_equal_to_limit_does_not_trigger_override():
    normal = {"id": "normal", "vulnerability_score": 0.0, "wait_minutes": 3.0}
    vulnerable = {"id": "vulnerable", "vulnerability_score": 1.0, "wait_minutes": 2.0}

    # The ratio is exactly 1.5; the implementation triggers only when it is greater.
    assert suggest_next([normal, vulnerable]) is vulnerable


def test_score_at_vulnerability_threshold_is_vulnerable():
    at_threshold = {"id": "threshold", "vulnerability_score": 0.5, "wait_minutes": 0.0}
    normal_longer_wait = {"id": "normal", "vulnerability_score": 0.0, "wait_minutes": 1.0}

    # With equal average waits, the fairness override is not triggered; the score
    # at the threshold gives this customer the higher effective priority.
    assert suggest_next([normal_longer_wait, at_threshold]) is at_threshold
