from datetime import datetime
import random

from typing import List, Tuple


class Student:
    def __init__(self, name: str, busy_days: List[datetime]):
        self.name = name
        self.busy_days = busy_days

    def __repr__(self) -> str:
        return self.name


class Day:
    def __init__(self, interrs: List[Student], num_interrs: int, date: datetime):
        self.interrs = interrs
        self.num = num_interrs
        self.date = date

    def __repr__(self) -> str:
        return "Day %s" % self.date


def checkdays(
    students: List[Student], days: List[Day]
) -> Tuple[List[Student], List[Day]]:
    """Checks lsit's validity"""

    unallocateds = []
    empty_days = []

    # this parameters should always be falses, otherways there is a bug or the parameters are wrong
    # TODO: panic in this cases
    # TODO: consider students missing in students list or misparsed days
    overallocateds = False
    too_much_per_day = False
    incompatibles_dates = False

    for s in students:
        allocated = 0  # number of days where the student is allocated

        for d in days:
            if s in d.interrs:
                allocated += 1

        if allocated == 0:
            unallocateds.append(s)
        elif allocated > 1:
            overallocateds = True

    for d in days:
        if len(d.interrs) > d.num:
            too_much_per_day = True
        elif len(d.interrs) < d.num:
            empty_days.append(d)

    total = 0
    for d in days:
        total += d.num

    if total != len(students):
        incompatibles_dates = True

    return (unallocateds, empty_days)


# TODO: check if it's possible to create an infinite loop
def remove_interrs(days: List[Day], day: Day):
    """Removes students who selected an under-selected day from other days"""

    if len(day.interrs) <= day.num:
        for i in day.interrs:
            for d in days:
                if day != d:
                    try:
                        d.interrs.remove(i)
                        remove_interrs(days, d)
                    except ValueError:
                        pass


def create_list(days: List[Day], students: List[Student], iteration: int) -> List[Day]:

    (unallocateds, empty_days) = checkdays(students, days)
    if len(unallocateds) != 0:
        print("ERROR: Missing students:", unallocateds)

    for day in days:
        remove_interrs(days, day)

    for day in days:
        while len(day.interrs) > day.num:
            day.interrs.remove(random.choice(day.interrs))
        remove_interrs(days, day)

    (unallocateds, empty_days) = checkdays(students, days)
    if len(unallocateds) != 0:
        non_preferred_days = []
        for day in empty_days:
            non_preferred_days.append(
                Day(
                    list(
                        filter(
                            lambda student: day.date not in student.busy_days,
                            unallocateds,
                        )
                    ),
                    day.num - len(day.interrs),
                    day.date,
                )
            )

        if iteration > 3:
            print("Something went wrong: too much iterations!")
            return
        for day in create_list(non_preferred_days, unallocateds, iteration + 1):
            for d in days:
                if d.date == day.date:
                    d.interrs.extend(day.interrs)

    return days

def best_list(dl1: List[Day], dl2: List[Day], sl: List[Student], dl: List[Day]):
    bad_allocated_1 = 0
    good_allocated_1 = 0
    bad_allocated_2 = 0
    good_allocated_2 = 0
    for d in dl1:
        for s in d.interrs:
            for i in dl:
                if i.date == d.date:
                    if s in i.interrs:
                        good_allocated_1 +=1
                        print("This works!")
            if d.date in s.busy_days:
                bad_allocated_1 += 1
                print("This works too!")
    for d in dl2:
        for s in d.interrs:
            for i in dl:
                if i.date == d.date:
                    if s in i.interrs:
                        good_allocated_2 +=1
                        print("This works!")
            if d.date in s.busy_days:
                bad_allocated_2 += 1
                print("This works too!")
    if bad_allocated_2 < bad_allocated_1:
        return dl2
    elif good_allocated_2 > bad_allocated_1:
        return dl2
    return dl1

# placeholder function
def run():
    marianna = Student("Marianna", [datetime(2023, 1, 30)])
    carlaf = Student("Carla Fraschini", [datetime(2023, 2, 6)])
    gabriele = Student("Gabriele", [])
    carola = Student("Carola", [])
    ludo = Student("Ludovico", [datetime(2023, 2, 6)])
    maia = Student("Maia", [])
    viola = Student("Viola", [datetime(2023, 1, 30)])
    virgi = Student("Viriginia", [datetime(2023, 1, 30)])
    ele = Student("Elena", [])
    manu = Student("Manuela", [])
    albi = Student("Alberto", [datetime(2023, 1, 30), datetime(2023, 2, 6)])
    chiara = Student("Chiara", [])
    arianna = Student("Arianna", [])
    davi = Student("Davide", [datetime(2023, 2, 6)])
    greg = Student("Gregorio", [])
    carlad = Student("Carla Dipietromaria", [datetime(2023, 2, 6)])
    matte = Student("Matteo", [datetime(2023, 1, 30)])
    anti = Student("David-Leonardo Antal", [2023, 2, 6])
    bea = Student("Beatrice", [datetime(2023, 2, 6)])
    jan = Student("Janelle", [datetime(2023, 2, 6)])
    leo = Student("Leonardo Ghiglia", [datetime(2023, 2, 6)])
    nasi = Student("Roberto", [datetime(2023, 2, 6)])
    gino = Student("Luca", [])
    fil = Student("Filippo", [])

    studentslist = [
        marianna,
        carlaf,
        gabriele,
        carola,
        ludo,
        maia,
        viola,
        virgi,
        ele,
        manu,
        albi,
        chiara,
        arianna,
        davi,
        greg,
        carlad,
        matte,
        anti,
        bea,
        jan,
        leo,
        nasi,
        gino,
        fil,
    ]

    dayslist = [
            Day([albi, ele], 2, datetime(2023, 1, 25)),
            Day(
                [arianna, manu, davi, bea, ele],
                4,
                datetime(2023, 1, 30),
            ),
            Day(
                [carlad, fil, maia, viola, ele, carlaf, carola, ludo, chiara, arianna, bea, jan],
                3,
                datetime(2023, 2, 1),
            ),
            Day([], 3, datetime(2023, 2, 6)),
            Day(
                [maia, viola, virgi, ele, davi, anti, jan, leo, gino],
                3,
                datetime(2023, 2, 8),
            ),
            Day(
                [virgi, albi, davi, greg, matte, anti, bea, leo, nasi],
                3,
                datetime(2023, 2, 13),
            ),
            Day(
                [marianna, gabriele, manu, albi, greg, carlad, matte, nasi],
                3,
                datetime(2023, 2, 20),
            ),
            Day([marianna, gabriele, manu], 3, datetime(2023, 2, 22)),
            Day(
                [carlad, fil, maia, viola, ele, carlaf, carola, ludo, chiara, arianna, bea, jan],
                3,
                datetime(2023, 2, 27),
            ),
        ]
    
    days = create_list(
        dayslist,
        studentslist,
        0,
    )

    for i in range(20):
        random.shuffle(dayslist)
        days = best_list(create_list(
            dayslist,
            studentslist,
            0,
        ), days, studentslist, dayslist)

    for day in days:
        print(day.date.day, day.interrs)

    (ua, ed) = checkdays(studentslist, days)
    print("Unallocated students:", ua, "\n" + "Non-filled days:", ed)


if __name__ == "__main__":
    run()
