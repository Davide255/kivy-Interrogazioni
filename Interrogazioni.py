import random

a,b,c,d,e,f,g,h,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = "abcdefghjklmnopqrstuvwxyz" # nomi dei volontari
days_num = {"12/30":3, "12/31":3, "1/1":2, "1/2":3, "1/3":2, "1/4":3, "1/5":3, "1/6":3, "1/7":3} # interrogati per giorno
days_vol = {"12/30":[h, j, k, l, m, n, o, p, q, r], "12/31":[s], "1/1":[a, b, c], "1/2":[d],
            "1/3":[e, f, g], "1/4":[t, u], "1/5":[], "1/6":[v, w], "1/7":[x, y, z]} # preferenze dei volontari
vol_priority = {0:[a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z]} # priorità dei volontari
ok = False
days = tuple(days_num.keys())

def main():
    global ok
    check()
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
        check()
    print(days_vol)
    print(vol_priority)

def test():
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

def check():
    """checks if there are too many volunteers in a day"""
    global days_vol, days_num, ok
    ok = True
    for day in days_num:
        if len(days_vol[day]) > days_num[day]:
            ok = False

test()
main()