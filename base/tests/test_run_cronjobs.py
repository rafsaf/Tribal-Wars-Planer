# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from collections.abc import Callable

import django.conf
from django.conf import LazySettings
from django.core.management import call_command
from freezegun import freeze_time
from pytest import CaptureFixture, MonkeyPatch


@freeze_time("2022-05-10")
def test_run_cronjobs(monkeypatch: MonkeyPatch, capsys: CaptureFixture):
    import time

    import schedule

    def fake_time_sleep_pass(secs: float):
        pass

    def always_run_pending_jobs():
        return schedule.run_all()

    def run_threaded_not_threaded(job_func: Callable[[], None], **kwargs):
        job_func(**kwargs)

    monkeypatch.setattr(time, "sleep", fake_time_sleep_pass)
    monkeypatch.setattr(django.conf, "settings", LazySettings())
    monkeypatch.setattr(schedule, "run_pending", always_run_pending_jobs)

    django.conf.settings.JOB_LIFETIME_MAX_SECS = -1

    from base.management.commands import runcronjobs

    monkeypatch.setattr(runcronjobs, "run_threaded", run_threaded_not_threaded)

    call_command("runcronjobs")

    out, err = capsys.readouterr()
    assert out == (
        "starting task dbupdate\n"
        "success task dbupdate - processed in 0.0s\n"
        "starting task dbupdate\n"
        "success task dbupdate - processed in 0.0s\n"
        "starting task outdateoverviewsdelete\n"
        "success task outdateoverviewsdelete - processed in 0.0s\n"
        "starting task outdateoutlinedelete\n"
        "success task outdateoutlinedelete - processed in 0.0s\n"
        "starting task calculatepaymentfee\n"
        "success task calculatepaymentfee - processed in 0.0s\n"
        "starting task worldlastupdate\n"
        "success task worldlastupdate - processed in 0.0s\n"
    )
