import itertools

# Define the class schedule details
classes = [
    {
        "name": "Data Analytics",
        "credits": 3,
        "schedules": [
            {"Monday": ["13:00-15:00"], "Friday": ["09:00-11:00"]},
            {"Wednesday": ["07:00-09:00"], "Friday": ["07:00-09:00"]}
        ]
    },
    {
        "name": "Person - Computer Interaction",
        "credits": 3,
        "schedules": [
            {"Monday": ["13:00-15:00"], "Thursday": ["14:00-16:00"]},
            {"Tuesday": ["14:00-16:00"], "Friday": ["09:00-11:00"]}
        ]
    },
    {
        "name": "IT Infrastructure",
        "credits": 3,
        "schedules": [
            {"Thursday": ["07:00-10:00"]},
            {"Tuesday": ["09:00-12:00"]},
            {"Saturday": ["09:00-12:00"]}
        ]
    },
    {
        "name": "Systemic Thinking",
        "credits": 3,
        "schedules": [
            {"Monday": ["15:00-18:00"]}
        ]
    },
    {
        "name": "Advanced Architectural Patterns",
        "credits": 3,
        "schedules": [
            {"Saturday": ["07:00-10:00"]}
        ]
    },
    {
        "name": "Privacy, Law and Technology",
        "credits": 2,
        "schedules": [
            {"Monday": ["12:00-14:00"]}
        ]
    },
    {
        "name": "IoT",
        "credits": 2,
        "schedules": [
            {"Monday": ["13:00-16:00"]},
            {"Monday": ["07:00-10:00"]},
            {"Wednesday": ["09:00-12:00"]},
            {"Tuesday": ["09:00-12:00"]}
        ]
    },
    {
        "name": "Software Projects",
        "credits": 3,
        "schedules": [
            {"Saturday": ["10:00-13:00"]}
        ]
    },
    {
        "name": "Business Creation Seminary",
        "credits": 2,
        "schedules": [
            {"Friday": ["09:00-11:00"]}
        ]
    }
]

max_credits = 15
max_gap_minutes = 60
max_classes_per_day = 3
max_days_per_week = 4

# Define mandatory classes
mandatory_classes = ["Data Analytics", "Advanced Architectural Patterns"]

# Helper functions
def parse_time(time_str):
    start_str, end_str = time_str.split('-')
    start_time = int(start_str[:2]) * 60 + int(start_str[3:])
    end_time = int(end_str[:2]) * 60 + int(end_str[3:])
    return start_time, end_time

def has_collision(schedule1, schedule2):
    for day in schedule1:
        if day in schedule2:
            for time_range1 in schedule1[day]:
                start_time1, end_time1 = parse_time(time_range1)
                for time_range2 in schedule2[day]:
                    start_time2, end_time2 = parse_time(time_range2)
                    if not (end_time1 <= start_time2 or end_time2 <= start_time1):
                        return True
    return False

def calculate_gaps(schedule):
    gaps = []
    day_times = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}

    for class_schedule in schedule:
        for day, timings in class_schedule.items():
            for timing in timings:
                start_time, end_time = parse_time(timing)
                day_times[day].append((start_time, end_time))

    for day, times in day_times.items():
        times.sort()
        previous_end_time = None
        for start_time, end_time in times:
            if previous_end_time is not None:
                gaps.append(start_time - previous_end_time)
            previous_end_time = end_time

    return sum(gaps)

def exceeds_max_classes_per_day(schedule, max_classes_per_day):
    day_counts = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}
    
    for class_schedule in schedule:
        for day in class_schedule:
            day_counts[day] += 1
    
    return any(count > max_classes_per_day for count in day_counts.values())

def count_days_in_schedule(schedule):
    # Count the distinct days in the schedule
    days = set()
    for class_schedule in schedule:
        for day in class_schedule:
            days.add(day)
    return len(days)

# Generate all combinations of classes
valid_schedules = []
for r in range(1, len(classes) + 1):
    for subset in itertools.combinations(classes, r):
        # Extract names of classes in the current subset
        subset_class_names = [cls["name"] for cls in subset]
        
        # Check if all mandatory classes are in the subset
        if all(cls in subset_class_names for cls in mandatory_classes):
            for combination in itertools.product(*[cls["schedules"] for cls in subset]):
                total_credits = sum(class_info["credits"] for class_info in subset)
                if total_credits == max_credits:
                    collision_found = False
                    for i in range(len(combination)):
                        for j in range(i + 1, len(combination)):
                            if has_collision(combination[i], combination[j]):
                                collision_found = True
                                break
                        if collision_found:
                            break
                    if not collision_found:
                        if calculate_gaps(combination) <= max_gap_minutes:
                            if not exceeds_max_classes_per_day(combination, max_classes_per_day):
                                # Apply the filter for max days per week
                                if count_days_in_schedule(combination) <= max_days_per_week:
                                    valid_schedules.append((subset, combination))

# Print the valid schedules
if valid_schedules:
    for idx, (subset, schedule) in enumerate(valid_schedules):
        print(f"Schedule {idx + 1}:")
        total_credits = sum(class_info["credits"] for class_info in subset)
        print(f"Total credits: {total_credits}")
        print("Classes:")

        # Collect and print schedules sorted by day
        day_wise_schedule = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}
        for class_info, times in zip(subset, schedule):
            for day, timings in times.items():
                day_wise_schedule[day].append((class_info["name"], timings))

        # Print schedules for each day including Saturday
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            if day_wise_schedule[day]:
                print(f"{day}:")
                for class_name, timings in day_wise_schedule[day]:
                    print(f"  {class_name}: {', '.join(timings)}")

        print(f"Total gap between classes: {calculate_gaps(schedule)} minutes")
        print("---------------------------")
else:
    print("No valid schedules found")
