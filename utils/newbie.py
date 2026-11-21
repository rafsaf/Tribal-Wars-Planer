# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from datetime import UTC, datetime, timedelta


def newbie_since(ratio_days: int) -> datetime:
    """Players created after this moment are still protected by the world ratio."""
    return datetime.now(UTC) - timedelta(days=ratio_days)


def is_newbie_blocked(
    ratio: int,
    since: datetime,
    target_player: str,
    target_points: int,
    target_created_at: datetime,
    attacker_points: int,
    attacker_created_at: datetime,
) -> bool:
    """World newbie protection: the smaller player, if young, blocks attacks over ratio:1."""
    if ratio <= 0 or target_player == "":
        return False
    if attacker_points > target_points:
        return target_created_at > since and attacker_points > ratio * target_points
    return attacker_created_at > since and target_points > ratio * attacker_points
