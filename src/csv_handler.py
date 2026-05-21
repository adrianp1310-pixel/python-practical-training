import csv


def read_people(path):
    try:
        with open(path, 'r', encoding='utf-8', newline="") as f:
            reader = csv.DictReader(f)
            result = []
            for row in reader:
                row["age"] = int(row["age"])
                row["salary"] = int(row["salary"])
                result.append(row)
        return result
    except FileNotFoundError:
        return None


def filter_by_city(people, city):
    return [osoba for osoba in people if osoba["city"] == city]

def total_salary(people):
    return sum(p["salary"] for p in people)


def write_summary(path, people):
    try:
        summary = {}
        for p in people:
            city = p["city"]
            salary = int(p["salary"])
            if city not in summary:
                summary[city] = {"total_salary": salary, "count": 1}
            else:
                summary[city]["total_salary"] += salary
                summary[city]["count"] += 1
        with open(path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["city", "total_salary", "count"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for city, data in summary.items():
                row ={"city": city, "total_salary": data["total_salary"], "count": data["count"]}
                writer.writerow(row)
        return True
    except OSError:
        return False

