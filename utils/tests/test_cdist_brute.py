from utils.basic.cdist_brute import CDistBrute


def test_cdist_brute(
    codspeed_benchmark,
) -> None:
    ally = []
    for i in range(1000):
        for j in range(20):
            ally.append((i, j))
    enemy = []
    for i in range(100):
        for j in range(6):
            enemy.append((i, j))

    @codspeed_benchmark
    def bench():
        CDistBrute(
            ally_villages=ally,
            enemy_villages=enemy,
            min_radius=1.0,
            max_radius=10.0,
        ).triple_result()
