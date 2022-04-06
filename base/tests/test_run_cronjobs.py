import os
from typing import Callable

import django.conf
from django.conf import LazySettings
from pytest import CaptureFixture, MonkeyPatch


def test_run_cronjobs(monkeypatch: MonkeyPatch, capsys: CaptureFixture):
    import time

    import schedule

    os.environ["DJANGO_SETTINGS_MODULE"] = "tribal_wars_planer.settings_cronjobs"

    def fake_time_sleep_pass(secs: float):
        pass

    def always_run_pending_jobs():
        return schedule.run_all()

    def run_threaded_not_threaded(job_func: Callable[[], None]):
        job_func()

    monkeypatch.setattr(time, "sleep", fake_time_sleep_pass)
    monkeypatch.setattr(django.conf, "settings", LazySettings())
    monkeypatch.setattr(schedule, "run_pending", always_run_pending_jobs)

    django.conf.settings.JOB_LIFETIME_MAX_SECS = -1

    from base import run_cronjobs

    monkeypatch.setattr(run_cronjobs, "run_threaded", run_threaded_not_threaded)

    run_cronjobs.main()

    out, err = capsys.readouterr()

    assert err == (
        "INFO Cronjobs starting\n"
        "INFO db_update\n"
        "INFO db_update\n"
        "INFO outdate_overviews_delete\n"
        "INFO outdate_outline_delete\n"
        "INFO Cronjobs restarting in 60s...\n"
    )
