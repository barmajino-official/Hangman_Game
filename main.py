from src.library.ClassMain import DataHandler
from tabulate import tabulate

filename = "src/data/data.json"
data_handler = DataHandler(filename)


def diplayTable(data):
    headers = ['Name', 'Hint', "Level"]

    rows = [[d['name'], d['hint'], d['level']] for d in data]

    print(tabulate(rows, headers=headers, tablefmt='grid'))


def SelectToRun(items):
    print("* Select :")
    for item in items:
        print(f"{items.index(item)} - {item['Title']}")
    index = int(input(" Select : \t"))
    if items[index]["arg"]:
        items[index]["def"](**items[index]["arg"])
    else:
        items[index]["def"]()


def SelectLevel():
    try:
        levels = data_handler.get_all_levels()
        print(f"Select one of this levels :")
        for level in levels:
            print(f"{levels.index(level)} - {level}")
        return levels[int(input(f" Select :\t"))]
    except ValueError as GetLevelsErr:
        print(GetLevelsErr)
    # handle the error here


def SelectRecord(level):
    try:
        recordes = data_handler.get_all_records(level)

        print(f"Select one of this records :")
        for recorde in recordes:
            print(f"{recorde['index']} - {recorde['name']}")
        return recordes[int(input(f" Select :\t"))]
    except ValueError as GetAllRecordsErr:
        print(GetAllRecordsErr)
        # handle the error here


def create():
    try:
        levels = data_handler.get_all_levels()
        SelectedLevel = SelectLevel()
        Name = input("Enter the name :\t")
        Hint = input("Enter the hint :\t")
        try:
            data_handler.add_record(SelectedLevel, Name, Hint)
        except ValueError as AddRecordErr:
            print(AddRecordErr)
    # handle the error here

    except ValueError as GetLevelsErr:
        print(GetLevelsErr)
    # handle the error here


def edit():
    SelectedLevel = SelectLevel()
    SelecterRecord = SelectRecord(SelectedLevel)
    try:
        Name = input("Enter the name :\t")
        Hint = input("Enter the hint :\t")
        data_handler.edit_record(
            SelectedLevel, SelecterRecord['index'], name=Name, hint=Hint)
    except ValueError as EditRecordErr:
        print(EditRecordErr)
        # handle the error here


def move():
    try:
        SelectedFrom = SelectLevel()
        SelecterRecord = SelectRecord(SelectedFrom)
        SelectedTo = SelectLevel()

        data_handler.move_record(
            SelecterRecord['index'], SelectedFrom, SelectedTo)
    except ValueError as MoveRecordErr:
        print(MoveRecordErr)
        # handle the error here


def delete():
    try:
        SelectedFrom = SelectLevel()
        SelecterRecord = SelectRecord(SelectedFrom)
        data_handler.delete_record(SelectedFrom, SelecterRecord['index'])

    except ValueError as DeleteRecordErr:
        print(DeleteRecordErr)
        # handle the error here


def editcenter():
    SelectToRun([{"Title": "Edit Record", "def": edit, "arg": None},
                {"Title": "Move Record", "def": move, "arg": None},
                {"Title": "Delete Record", "def": delete, "arg": None}])


def displayLevels():
    try:
        levels = data_handler.get_all_levels()
        print(levels)
    except ValueError as GetAllLevelsErr:
        print(GetAllLevelsErr)
        # handle the error here


def displayAllRecords():
    try:
        records = data_handler.get_all_records()
        diplayTable(records)
    except ValueError as GetAllRecordsErr:
        print(GetAllRecordsErr)
        # handle the error here


def display():
    SelectToRun([{"Title": "Display Levels", "def": displayLevels, "arg": None},
                {"Title": "Display Records", "def": displayAllRecords, "arg": None}])


def search():
    try:

        matches = data_handler.search_records(
            input("* Enter Search KEYWORD :\t"))
        print(matches)
    except ValueError as SearchRecordsErr:
        print(SearchRecordsErr)
        # handle the error here


def Play():
    score: int = 0
    harts: str = "❤️ "
    hartsLength: int = 5
    tempList = []
    level: str = SelectLevel()
    exit: str = False
    while (exit != True):
        Answare: str = ""
        try:
            record = data_handler.get_random_record(level)
            if (len(tempList) < record['levelLanght'] and exit != True):

                while (record['name'] in tempList):
                    record = data_handler.get_random_record(level)
                tempList.append(record['name'])
                while (Answare != record['name']):
                    print(f"Ges What is this {record['maskname']}")
                    print(f"hint : {record['hint']} | {harts*hartsLength}")
                    Answare = input("*Enter your Answare :\t")
                    if (Answare != record['name']):
                        hartsLength -= 1
                        if (hartsLength <= 0):
                            exit = True
                            break
                score += 1
            else:
                exit = True

        except ValueError as GetRandomRecordErr:
            print(GetRandomRecordErr)
    print(f"Score : {score}")

    # handle the error here


if __name__ == "__main__":
    while True:
        SelectToRun([{"Title": "Play", "def": Play, "arg": None},
                     {"Title": "Edit", "def": editcenter, "arg": None},
                     {"Title": "Create", "def": create, "arg": None},
                     {"Title": "Display", "def": display, "arg": None},
                     {"Title": "Search", "def": search, "arg": None},
                     {"Title": "Exit", "def": exit, "arg": None}])
