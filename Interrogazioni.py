import random
from datetime import date

#### DATI DI ESEMPIO ####

names_and_pref = {'Davide':[date(2021, 12, 30)]}

a,b,c,d,e,f,g,h,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = "abcdefghjklmnopqrstuvwxyz" # nomi dei volontari
days_num = {date(2021, 12, 30):3, date(2021, 12, 31):3, date(2022, 1, 1):2, date(2022, 1, 2):3, date(2022, 1, 3):2,
            date(2022, 1, 4):3, date(2022, 1, 5):3, date(2022, 1, 6):3, date(2022, 1, 7):3} # interrogati per giorno
days_vol = {date(2021, 12, 30):[h, j, k, l, m, n, o, p, q, r], date(2021, 12, 31):[s], date(2022, 1, 1):[a, b, c],
            date(2022, 1, 2):[d], date(2022, 1, 3):[e, f, g], date(2022, 1, 4):[t, u],
            date(2022, 1, 5):[], date(2022, 1, 6):[v, w], date(2022, 1, 7):[x, y, z]} # preferenze dei volontari
vol_priority = {0:[a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z]} # priorità dei volontari

#########################

ok = False
days = tuple(days_num.keys())

class Vol(): # verrà usata per riorganizzare i dati
    def __init__(self, name: str, preferences: list, priority: int, available_days=None):
        self.name = name # nome del volontario
        self.pref = preferences # giorni preferiti
        self.prio = priority # priorità, ovvero distanza dalla preferenza
        self.days = available_days # giorni in cui può essere interrogato
        self.day = preferences[0] # giorno in cui è posizionato
    
    def sort_by_pref(self, ds, prfs): # ordina i giorni in cui può essere interrogato dal preferito al meno
        sorted_days = []
        i = 0
        while ds.len() > sorted_days.len():
            for d in ds:
                for p in prfs:
                    if abs((p-d).days) != i:
                        continue
                    else:
                        if not d in sorted_days: # controlla di non aver già inserito il giorno
                            sorted_days.append(d)
            i += 1
    
    def __iter__(self):
        self.ind = -1

    def __next__(self):
        self.ind =+ 1
        if self.ind == len(self.pref):
            raise StopIteration()
        else:
            return self.pref[self.ind]

class Interr:

    vols = list()

    def __init__(self) -> None:
        for i in names_and_pref:
            exec('if not hasattr(Interr, \'%s\'):\n\tself.%s = Vol(i, names_and_pref[i], 0)\n\tInterr.vols.append(self.%s)\nelse:\n\tself.%s_2 = Vol(i, names_and_pref[i], 0)\n\tInterr.vols.append(self.%s_2)'.replace('%s', i))

    def create_sheet(self):
        global ok
        self.check()
        while ok == False:
            for day in days_vol:
                day_n = days_num[day]
                priority = 0
                while len(days_vol[day]) > day_n:
                    minor_priority = []
                    for i in days_vol[day]:
                        if i in vol_priority[priority]:
                            minor_priority.append(i)
                    if len(minor_priority) != 0:
                        rem = minor_priority.pop(minor_priority.index(random.choice(minor_priority)))
                        days_vol[day].remove(rem)
                        vol_priority[priority].remove(rem)
                        try:
                            vol_priority[priority+1].append(rem)
                        except KeyError:
                            vol_priority[priority+1] = []
                            vol_priority[priority+1].append(rem)
                        try: # prova a spostare un interrogato a caso al giorno successivo
                            days_vol[days[days.index(day)+1]].append(rem)
                        except IndexError: # sposta l'interrogato al giorno precedente
                            days_vol[days[days.index(day)-1]].append(rem)
                    else:
                        priority += 1
            self.check()
        print(days_vol)
        print(vol_priority)

    def test(self):
        """checks if there are enaugh days for the volunteers"""
        n = 0
        m = 0
        for d in days_num:
            n += days_num[d]
        for e in days_vol:
            m += len(days_vol[e])
        if m > n:
            print("Too many volunteers")
            exit()

    def check(self):
        """checks if there are too many volunteers in a day"""
        global days_vol, days_num, ok
        ok = True
        for day in days_num:
            if len(days_vol[day]) > days_num[day]:
                ok = False

interr = Interr()
interr.test()
interr.create_sheet()
