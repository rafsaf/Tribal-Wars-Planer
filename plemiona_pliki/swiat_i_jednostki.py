class Swiat():
    def __init__(self, number):
        self.number = number
        self.predkosc_swiata = None
        self.predkosc_jednostek = None
        self.predkosc()

    def predkosc(self):
        if self.number == 150:
            self.predkosc_swiata = 1.2
            self.predkosc_jednostek = 0.8
        else:
            raise ValueError("błędny świat")


class Jednostki():
    def __init__(self):
        self.slownik_jedn_predkosc = {"pikinier":18, "miecznik":22, "topornik":18,"łucznik":18,"zwiadowca":9,
                                      "lekki kawalerzysta":10, "łucznik na koniu":10, 'ciężki kawalerzysta':11,
                                      "taran":30, "szlachcic":35, "katapulta":30}

    def predkosc_pik(self):
        return 18
    def predkosc_miecz(self):
        return 22
    def predkosc_zwiad(self):
        return 9
    def predkosc_ck(self):
        return 11
    def predkosc_lk(self):
        return 10
    def predkosc_taran(self):
        return 30
    def predkosc_szlachcic(self):
        return 35
    def predkosc_rycerz(self):
        return 10
