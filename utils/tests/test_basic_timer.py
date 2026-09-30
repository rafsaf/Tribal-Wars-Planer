# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from utils.basic import timing


def test_timing(capsys):
    @timing
    def test_func():
        pass

    test_func()
