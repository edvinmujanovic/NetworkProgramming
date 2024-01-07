name_to_points = {}

with open('lab2/score2.txt', 'r') as file:
    for line in file:
        parts = line.split()
        
        exercise_number = parts[1]
        firstName = parts[2]
        lastName = parts[3]
        points = int(parts[4])
        
        fullName = f"{firstName} {lastName}"
        
        if fullName in name_to_points:
            name_to_points[fullName] += points
        else:
            name_to_points[fullName] = points


max_points = max(name_to_points.values())
top_scorers = [name for name, points in name_to_points.items() if points == max_points]


print(f"Person(s) with the most points ({max_points} points):")
for scorer in top_scorers:
    print(scorer)
