import os
import json
import random
from typing import List, Dict, Union, Tuple


class DataHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"easy": [], "medium": [], "hard": []}
            self.save_data()

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f)

    def add_record(self, level: str, name: str, hint: str):
        if level not in self.data:
            raise ValueError(f"Invalid level: {level}")

        self.data[level].append(f"{name}:{hint}")
        self.save_data()

    def delete_record(self, level: str, index: int):
        if level not in self.data:
            raise ValueError(f"Invalid level: {level}")

        if index < 0 or index >= len(self.data[level]):
            raise ValueError("Invalid index")

        del self.data[level][index]
        self.save_data()

    def edit_record(self, level: str, index: int, name: str = None, hint: str = None):
        if level not in self.data:
            raise ValueError(f"Invalid level: {level}")

        if index < 0 or index >= len(self.data[level]):
            raise ValueError("Invalid index")

        record = self.data[level][index].split(":")
        if name is not None:
            record[0] = name
        if hint is not None:
            record[1] = hint

        self.data[level][index] = ":".join(record)
        self.save_data()

    def search_records(self, keyword: str) -> List[Tuple[str, str, str]]:
        matches = []
        for level in self.data:
            for record in self.data[level]:
                if keyword in record:
                    matches.append(
                        (record.split(":")[0], record.split(":")[1], level))

        if not matches:
            raise ValueError(f"No matches found for keyword: {keyword}")

        return matches

    def get_random_record(self, level: str) -> Dict[str, Union[str, int]]:
        if level not in self.data:
            raise ValueError(f"Invalid level: {level}")

        if not self.data[level]:
            raise ValueError(f"No records in level: {level}")

        record = random.choice(self.data[level]).split(":")
        random_index = random.randint(0, len(record[0]) - 1)
        masked_name = ""
        for index_, letter in enumerate(record[0]):
            if index_ == random_index:
                masked_name += letter
            else:
                masked_name += "-"

        return {"name": record[0], "maskname": masked_name, "hint": record[1], "levelLanght": len(self.data[level])}

    def get_all_records(self, level: str = "All") -> List[Dict[str, Union[str, int]]]:
        if (level != "All"):
            if level not in self.data:
                raise ValueError(f"Invalid level: {level}")

            if len(self.data[level]) <= 0:
                raise ValueError(f"level: {level} is empty")

        records = []
        if (level == "All"):
            for level in self.get_all_levels():
                for index, record in enumerate(self.data[level]):
                    name, hint = record.split(":")
                    records.append(
                        {"name": name, "hint": hint, "index": index, "level": level})

        else:
            for index, record in enumerate(self.data[level]):
                name, hint = record.split(":")
                records.append(
                    {"name": name, "hint": hint, "index": index, "level": level})
        return records

    def get_all_levels(self) -> List[str]:
        return list(self.data.keys())

    def move_record(self, recordIndex, from_level, to_level):
        if from_level == to_level:
            raise ValueError("Cannot move record to the same level")
        if from_level not in self.data or not self.data[from_level]:
            raise ValueError(f"No records found in level {from_level}")
        if to_level not in self.data:
            raise ValueError(f"Invalid destination level: {to_level}")
        record = self.data[from_level][recordIndex]
        self.data[from_level].pop(int(recordIndex))
        self.data[to_level].append(record)
        self.save_data()

    # rest of the code
