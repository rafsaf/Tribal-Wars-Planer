from plemiona_pliki.wioska import Wiele_wiosek, Wioska
from plemiona_pliki.zbiorka_grubych_csv_NEW import zbiorka_grubych_z_ankiety

def zbiorka_offow(wioski: str, text: str, jednostka:str, minimalny_off:int, text_ankieta, text_obrona):
    context = zbiorka_grubych_z_ankiety(text_ankieta, text_obrona)
    wioski2 = wioski.split()
    wioski_w_roznych_rejonach = Wiele_wiosek(wioski).lista_z_wioskami
    output_text = "Kordy;Gracz;Wojsko;Ilość grubych;"

    for i in wioski_w_roznych_rejonach:
        output_text += i.get_player(150) + ";"
    output_text += "\r;;;;"
    for i in wioski2:
        output_text += i + ";"

    for i in text.split("\r"):

        i = i.split(",")
        i[0]=i[0].strip("\n")
        wioska = Wioska(i[0])

        odl = [round(wioska.time_distance(k, jednostka, 150) / 3600, 1) for k in wioski_w_roznych_rejonach]
        try:
            ile_grubych = str(context[wioska.kordy])
        except KeyError:
            print(wioska.get_player(150))
            ile_grubych = str(0)
            pass

        if int(i[3])+int(i[5])*4+int(i[7])*5+int(i[8])*8 >= int(minimalny_off) or int(ile_grubych) > 0:
            output_text+="\r"+i[0]+ ";"+wioska.get_player(150)+";"+ str(int(i[3])+int(i[5])*4+int(i[7])*5+int(i[8])*8)+";"+ile_grubych+";"+";".join(map(str, odl))
    return output_text


