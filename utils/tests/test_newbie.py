from datetime import UTC, datetime, timedelta

from utils.newbie import is_newbie_blocked, newbie_since


def test_is_newbie_blocked() -> None:
    now = datetime.now(UTC)
    young, old = now - timedelta(days=10), now - timedelta(days=61)
    since = newbie_since(60)

    def blocked(target_pts, target_at, attacker_pts, attacker_at, ratio=20, player="p"):
        return is_newbie_blocked(
            ratio, since, player, target_pts, target_at, attacker_pts, attacker_at
        )

    # big attacker vs young small target
    assert blocked(5000, young, 200_000, old)
    assert not blocked(5000, young, 100_000, old)
    assert not blocked(5000, old, 200_000, old)
    # young small attacker vs big target
    assert blocked(200_000, old, 5000, young)
    assert not blocked(200_000, old, 5000, old)
    assert not blocked(100_000, old, 5000, young)
    # big young player does not make small old one protected
    assert not blocked(5000, old, 200_000, young)
    # disabled / barbarians
    assert not blocked(5000, young, 200_000, old, ratio=0)
    assert not blocked(0, young, 200_000, young, player="")
    # window edge
    assert not is_newbie_blocked(
        20, newbie_since(10), "p", 5000, now - timedelta(days=11), 200_000, old
    )
