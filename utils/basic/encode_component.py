# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from urllib.parse import quote


def encode_component(string_to_encode: str) -> str:
    # https://stackoverflow.com/questions/946170/equivalent-javascript-functions-for-pythons-urllib-parse-quote-and-urllib-par
    return quote(string_to_encode, safe="()*!'")
