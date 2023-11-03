import numpy as np
from scipy.spatial.distance import cdist


class CDistBrute:
    def __init__(
        self,
        ally_villages: np.ndarray,
        enemy_villages: np.ndarray,
        min_radius: float,
        max_radius: float,
    ) -> None:
        self.all_ally = ally_villages
        self.all_enemy = enemy_villages
        self.min_radius = min_radius
        self.max_radius = max_radius

    def result(self, batch_size: int = 18) -> tuple[np.ndarray, np.ndarray]:
        """
        Brute force. This is detailed version of result method.

        Returns
        -------
        tuple of np.ndarray is returned:

        (below `x` is minimum of distances to every enemy village)

        `front_lst` : array with coords `x <= min_radius`

        `back_lst` : array with coords `min_radius < x < max_radius`

        NOTES
        -----
        For given in class init enemy villages `N` and ally villages `M`
        - Step 1: Iterate over the `M` in `i` batches `k` of size `batch_size` where `i` is ceil from `len(M)/batch_size`
        - Step 2: For every batch k1, k2 calculate matrix of sq euclidean distances k x N allies from enemies
        - Step 3: Append villages in to front, back list
        """
        triple_result = self.triple_result(batch_size)
        return triple_result[0], triple_result[1]

    def triple_result(
        self, batch_size: int = 18
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Brute force. This is detailed version of result method.

        Returns
        -------
        tuple of np.ndarray is returned:

        (below `x` is minimum of distances to every enemy village)

        `front_lst` : array with coords `x <= min_radius`

        `back_lst` : array with coords `min_radius < x < max_radius`

        `away_lst` : array with coords `min_radius >= max_radius`

        NOTES
        -----
        For given in class init enemy villages `N` and ally villages `M`
        - Step 1: Iterate over the `M` in `i` batches `k` of size `batch_size` where `i` is ceil from `len(M)/batch_size`
        - Step 2: For every batch k1, k2 calculate matrix of sq euclidean distances k x N allies from enemies
        - Step 3: Append villages in to front, back or away list
        """

        sq_min_radius: float = self.min_radius**2
        sq_max_radius: float = self.max_radius**2

        total_front: list[np.ndarray] = []
        total_back: list[np.ndarray] = []
        total_away: list[np.ndarray] = []

        for i in range(int(np.ceil(self.all_ally.size / batch_size))):
            batch_ally = self.all_ally[i * batch_size : (i + 1) * batch_size]
            C = (cdist(np.array(batch_ally), self.all_enemy, "sqeuclidean")).min(axis=1)
            for index, x in np.ndenumerate(C):
                if x <= sq_min_radius:
                    total_front.append(batch_ally[index])
                elif x < sq_max_radius:
                    total_back.append(batch_ally[index])
                else:
                    total_away.append(batch_ally[index])

            # below implementation is also possible, but... slower
            # mask_front = C <= sq_min_radius
            # mask_back = np.where((C > sq_min_radius) & (C < sq_max_radius), True, False)
            # mask_away = C >= sq_max_radius
            # for array in batch_ally[mask_front]:
            #     total_front.append(array)
            # for array in batch_ally[mask_back]:
            #     total_back.append(array)
            # for array in batch_ally[mask_away]:
            #     total_away.append(array)

        return (np.array(total_front), np.array(total_back), np.array(total_away))
