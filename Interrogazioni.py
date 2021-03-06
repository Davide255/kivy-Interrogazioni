import random
from datetime import date
from Widgets.calendar_widget import calendar_data as cal_data

#### DATI DI ESEMPIO ####

names_and_pref = {
    'Davide':[date(2022, 2, 12), date(2022, 2, 17)], 
    'Filippo':[date(2022, 2, 13), date(2022, 2, 19)],
    'Gino':[date(2022, 2, 12), date(2022, 2, 17)], 
    'Paolo':[date(2022, 2, 13), date(2022, 2, 19)],
    'Giovanni':[date(2022, 2, 12), date(2022, 2, 17)], 
    'Pietro':[date(2022, 2, 13), date(2022, 2, 19)],
    'Alessandra':[date(2022, 2, 12), date(2022, 2, 17)], 
    'Chiara':[date(2022, 2, 13), date(2022, 2, 19)]
    }

days_num = {date(2022, 2, 12):2, date(2022, 2, 17):1, date(2022, 2, 13):1, date(2022, 2, 19):2, date(2022, 2, 1):1, date(2022, 2, 2):1}

#########################

days = tuple(days_num.keys())

class Student: # verrà usata per riorganizzare i dati
    def __init__(self, name: str, preferences: list, priority: int = 0):
        self.name = name # nome del volontario
        self.pref = preferences # giorni preferiti
        self.prio = priority # priorità, ovvero distanza dalla preferenza
        self.day = None # giorno in cui è posizionato; se None lo studente non è posizionato in alcun giorno
    
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

    def __repr__(self) -> str:
        return '<Student {}>'.format(self.name)

    def __next__(self):
        self.ind =+ 1
        if self.ind == len(self.pref):
            raise StopIteration()
        else:
            return self.pref[self.ind]

class Property(object):

    def __init__(self, fget, fset):
        self.fget = fget
        self.fset = fset

    def __get__(self, instance, cls):
        return self.fget(instance)
    
    def __set__(self, instance, value):
        return self.fset(instance,value)

class Interr(object):

    vols = dict()

    def __init__(self) -> None:
        for i in names_and_pref:
            exec('if not hasattr(Interr, \'%s\'):\n\tself.%s = Student(i, names_and_pref[i])\n\tInterr.vols[i] = self.%s\nelse:\n\tself.%s_2 = Student(i, names_and_pref[i])\n\tInterr.vols[i] = self.%s_2'.replace('%s', i))

        self.calend = self.calendar()
        self.pref_calendar = self.calend.alloc_volunteers(self.vols)

    class calendar():
        
        def __init__(self):
            months = cal_data.get_month_names()
            if months[0] == '':
                months.pop(0)
            self.month_names = months
            self.days_abrs = cal_data.get_days_abbrs()

            # Today date
            self.active_date = cal_data.today_date_list()
            
            # Quarter where current month in the self.quarter[1]
            self.get_quarter()

        def get_quarter(self):
            """ Get calendar and months/years nums for quarter """

            current_month = self.active_date[1]
            current_year = self.active_date[2]

            self.quarter_nums = cal_data.calc_quarter(
                current_year,
                current_month,
            )

            self.quarter = cal_data.get_quarter(
                current_year,
                current_month,
            )

        def next_month(self):
            self.active_date = [self.active_date[0], self.quarter_nums[2][1],
                                self.quarter_nums[2][0]]
            self.get_quarter()

        def _data_repr(self):
            self.dates = list()
            i = int()
            for m in self.quarter:
                month = self.quarter_nums[i][1]
                for s in m:
                    for d in s:
                        if d[2]:
                            self.dates.append(date(self.quarter_nums[0][0], month, d[0]))
                i += 1

            return self.dates
        
        def __data_alloc__(self, data: date, student: Student, tips=None):
            if not hasattr(self, 'pref_calendar'):
                self.pref_calendar = dict()
            else:
                if not self.pref_calendar.get(data):
                    self.pref_calendar[data] = [student]
                else:
                    self.pref_calendar[data].append(student)
        
        def alloc_volunteers(self, _list):
            for i in names_and_pref:
                for p in names_and_pref[i]:
                    self.__data_alloc__(p, _list[i])
            return self.pref_calendar

        datas = Property(_data_repr, lambda *args: None)

    def create_sheet(self):
        #self.test() 
        if hasattr(self, '__cache__'):
            return self.__cache__
        program = dict()
        _students = self.pref_calendar.copy() # get a mutable sequence of the preferences
        
        for day in self.pref_calendar: # iter single days in preferences dict keys; 
                                       # dict format = { date(**kwargs) : list( Student(**kwargs) ) }
            if len(_students[day]) > days_num[day]: # if there are too many students for a single day:
                
                program[day] = list() # initiallize the day's space to tell python that value will 
                                      # be a list() object

                for c in range(int(days_num[day])): #  itering for a specific number of times
                    r = random.randint(0, len(_students)-c)
                    try:
                        _s = _students[day].pop(r)
                    except IndexError:
                        _s = _students[day].pop(r-1)
                    while True:
                        if not _s.day:
                            program[day].append(_s) # random choose the student that will 
                                                    # pass on required day
                            _s.day = day
                            break
                        else:
                            r = random.randint(0, len(_students)-c)
                            _s = _students[day].pop(r)

            else: # if students are equal or less for the day those will be satisfied 
                program[day] = _students[day]

            _students.pop(day, 0)
        
        _missing = list()

        for i in self.vols: # get missing students
            if not self.vols[i].day:
                _missing.append(self.vols[i])

        if len(_missing): # if there are missing

            _free = list() # free days struct = [ [date(**kwargs), int(free_places)] ]

            for d in days_num: # get free days
                try:
                    if len(program[d]) < days_num[d]:
                        _free.append([d, days_num[d] - len(program[d])])
                    else:
                        pass
                except KeyError:
                    _free.append([d, days_num[d]])

            if len(_free) == 1 and len(_missing) == _free[0][1]: # if there is only one day free and day[free_places] students
                program[_free[0][0]] = _missing                  # put all those students in this day

            else: # else randomically extract the students in the day

                for _s in _missing:
                    try:
                        day = random.choice(_free)
                    except IndexError:
                        print('<==== WARNING: There aren\'t enought days for missing students: (missing: {}, free days: {}) ====>'.format(_missing, _free))
                        return dict()
                    try:
                        program[day[0]].append(_s)
                    except KeyError:
                        program[day[0]] = [_s]
                    if day[1] == 1:
                        _free.remove(day)
                    else:
                        _free[_free.index(day)][1] -= 1

        self.__cache__ = program
        return program

    program = Property(create_sheet, lambda *args: None) # handle to create_sheet function

    class Decrepited:

        a,b,c,d,e,f,g,h,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = "abcdefghjklmnopqrstuvwxyz" # nomi dei volontari
        vol_priority = {0:[a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z]} # priorità dei volontari

        ok = False
        days_num = {date(2021, 12, 30):3, date(2021, 12, 31):3, date(2022, 1, 1):2, date(2022, 1, 2):3, date(2022, 1, 3):2,
                    date(2022, 1, 4):3, date(2022, 1, 5):3, date(2022, 1, 6):3, date(2022, 1, 7):3} # interrogati per giorno
        days_vol = {date(2021, 12, 30):[h, j, k, l, m, n, o, p, q, r], date(2021, 12, 31):[s], date(2022, 1, 1):[a, b, c],
                    date(2022, 1, 2):[d], date(2022, 1, 3):[e, f, g], date(2022, 1, 4):[t, u],
                    date(2022, 1, 5):[], date(2022, 1, 6):[v, w], date(2022, 1, 7):[x, y, z]} # preferenze dei volontari
        
        days = tuple(days_num.keys())  

        def create_sheet_old_algorithm(self):
            self.test()
            while self.ok == False:
                for day in self.days_vol:
                    day_n = self.days_num[day]
                    priority = 0
                    while len(self.days_vol[day]) > day_n:
                        minor_priority = []
                        for i in self.days_vol[day]:
                            if i in self.vol_priority[priority]:
                                minor_priority.append(i)
                        if len(minor_priority) != 0:
                            rem = minor_priority.pop(minor_priority.index(random.choice(minor_priority)))
                            self.days_vol[day].remove(rem)
                            self.vol_priority[priority].remove(rem)
                            try:
                                self.vol_priority[priority+1].append(rem)
                            except KeyError:
                                self.vol_priority[priority+1] = []
                                self.vol_priority[priority+1].append(rem)
                            try: # prova a spostare un interrogato a caso al giorno successivo
                                self.days_vol[self.days[self.days.index(day)+1]].append(rem)
                            except IndexError: # sposta l'interrogato al giorno precedente
                                self.days_vol[self.days[self.days.index(day)-1]].append(rem)
                        else:
                            priority += 1
                self._check()
            print(self.days_vol)
            print(self.vol_priority)

        def test(self):
            """checks if there are enaugh days for the volunteers"""
            n = 0
            m = 0
            for d in self.days_num:
                n += self.days_num[d]
            for e in self.days_vol:
                m += len(self.days_vol[e])
            if m > n:
                class TooManyVolunteers(BaseException):
                    pass
                raise TooManyVolunteers("Too many volunteers, check again")

        def _check(self):
            """checks if there are too many volunteers in a day"""
            self.ok = True
            for day in self.days_num:
                if len(self.days_vol[day]) > self.days_num[day]:
                    self.ok = False

if __name__ == '__main__':
    if input('which alghorithm would you use? (n new/ o old) default \'n\': ') == 'o':
        interr = Interr.Decrepited
        interr().create_sheet_old_algorithm()
    else:
        interr = Interr()
        print(interr.program)
