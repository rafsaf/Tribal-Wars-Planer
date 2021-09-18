from utils.basic import timing


def test_timing(capsys):
    @timing
    def test_func():
        pass

    test_func()
    captured: str = capsys.readouterr().out
    assert "Func: test_func" in captured
    assert "Args:[()]" in captured
    assert "Kwargs:[{}]" in captured
    assert "Took:" in captured
    assert "Number of Queries: 0" in captured
    assert "Line by line time" in captured
