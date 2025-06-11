import itertools

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

classes = [
    {
        "name": "UX|UI",
        "credits": 3,
        "schedules": [
            {"Tuesday": ["08:00-10:00"], "Monday": ["14:00-16:00"]},
            {"Monday": ["08:00-10:00"], "Tuesday": ["10:00-12:00"]},
        ]
    },
    {
        "name": "Business Architecture",
        "credits": 3,
        "schedules": [
            {"Saturday": ["07:00-10:00"]},
        ]
    },
    {
        "name": "IoT",
        "credits": 2,
        "schedules": [
            {"Monday": ["07:00-10:00"]},
            {"Monday": ["10:00-13:00"]},
            {"Thursday": ["07:00-10:00"]},
        ]
    },
    {
        "name": "AI",
        "credits": 3,
        "schedules": [
            {"Wednesday": ["08:00-11:00"]},
            {"Tuesday": ["13:00-16:00"]},
        ]
    },
    {
        "name": "Cyber Security",
        "credits": 3,
        "schedules": [
            {"Monday": ["10:00-13:00"]},
            {"Tuesday": ["09:00-12:00"]},
            {"Thursday": ["14:00-17:00"]},
        ]
    },
    {
        "name": "Project Admin",
        "credits": 2,
        "schedules": [
            {"Thursday": ["08:00-10:00"]},
            {"Thursday": ["10:00-12:00"]},
        ]
    },
    {
        "name": "Law",
        "credits": 2,
        "schedules": [
            {"Monday": ["09:00-11:00"]},
            {"Thursday": ["13:00-15:00"]},
        ]
    },
    {
        "name": "IT",
        "credits": 4,
        "schedules": [
            {"Friday": ["14:00-16:00"], "Monday": ["07:00-09:00"]},
        ]
    },
    {
        "name": "CORE",
        "credits": 3,
        "schedules": [
            {"Tuesday": ["11:00-14:00"]},
        ]
    },
]

# Parámetros
min_credits = 18
max_credits = 18
max_gap_minutes = 180
max_classes_per_day = 3
max_days_per_week = 4  # ✅ Filtro nuevo
mandatory_classes = ["Cyber Security", "CORE"]
sort_by = "both"  # ✅ Opciones: "gaps", "days", "both"

# Utilidades
def parse_time(time_str):
    start_str, end_str = time_str.split('-')
    return int(start_str[:2]) * 60 + int(start_str[3:]), int(end_str[:2]) * 60 + int(end_str[3:])

def has_collision(schedule1, schedule2):
    for day in schedule1:
        if day in schedule2:
            for t1 in schedule1[day]:
                start1, end1 = parse_time(t1)
                for t2 in schedule2[day]:
                    start2, end2 = parse_time(t2)
                    if not (end1 <= start2 or end2 <= start1):
                        return True
    return False

def calculate_gaps(schedule):
    day_times = {day: [] for day in WEEK_DAYS}
    for sched in schedule:
        for day, times in sched.items():
            for time in times:
                start, end = parse_time(time)
                day_times[day].append((start, end))
    total_gap = 0
    for times in day_times.values():
        times.sort()
        for i in range(1, len(times)):
            gap = times[i][0] - times[i - 1][1]
            if gap > 0:
                total_gap += gap
    return total_gap

def exceeds_max_classes_per_day(schedule):
    counts = {day: 0 for day in WEEK_DAYS}
    for sched in schedule:
        for day in sched:
            counts[day] += 1
    return any(count > max_classes_per_day for count in counts.values())

def exceeds_max_days(schedule):
    days_with_classes = set()
    for sched in schedule:
        days_with_classes.update(sched.keys())
    return len(days_with_classes) > max_days_per_week

def count_days(schedule):
    days_with_classes = set()
    for sched in schedule:
        days_with_classes.update(sched.keys())
    return len(days_with_classes)

# Generación
results = []

for r in range(1, len(classes) + 1):
    for subset in itertools.combinations(classes, r):
        total_credits = sum(c["credits"] for c in subset)
        if not (min_credits <= total_credits <= max_credits):
            continue
        if not all(m in [c["name"] for c in subset] for m in mandatory_classes):
            continue

        for combo in itertools.product(*[c["schedules"] for c in subset]):
            if any(has_collision(combo[i], combo[j]) for i in range(len(combo)) for j in range(i + 1, len(combo))):
                continue
            if calculate_gaps(combo) > max_gap_minutes:
                continue
            if exceeds_max_classes_per_day(combo):
                continue
            if exceeds_max_days(combo):
                continue

            week_schedule = {day: [] for day in WEEK_DAYS}
            for c, sched in zip(subset, combo):
                for day, times in sched.items():
                    week_schedule[day].append((c["name"], times))

            results.append({
                "schedule_id": len(results) + 1,
                "total_credits": total_credits,
                "gap_minutes": calculate_gaps(combo),
                "num_days": count_days(combo),
                "classes": week_schedule
            })

# Ordenamiento
if sort_by == "gaps":
    results.sort(key=lambda x: x["gap_minutes"])
elif sort_by == "days":
    results.sort(key=lambda x: x["num_days"])
elif sort_by == "both":
    results.sort(key=lambda x: (x["num_days"], x["gap_minutes"]))

# Mostrar resultados
def print_schedule(sched):
    print(f"\n🗓️ Schedule {sched['schedule_id']} | Credits: {sched['total_credits']} | Gaps: {sched['gap_minutes']} min | Days: {sched['num_days']}")
    print("-" * 60)
    for day in WEEK_DAYS:
        if sched["classes"][day]:
            print(f"{day}:")
            for cls, times in sched["classes"][day]:
                print(f"  📘 {cls}: {', '.join(times)}")
    print("-" * 60)

if results:
    for sched in results[:5]:
        print_schedule(sched)
else:
    print("⚠️ No valid schedules found.")
