import sqlite3

def create_database():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    
    # Create the 'persons' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            given_name TEXT,
            second_name TEXT
        )
    ''')

    # Create the 'scores' table with a foreign key reference to 'persons'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            task_number INTEGER,
            points INTEGER,
            person_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

    


def import_data():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()

    with open("lab11/score2.txt", "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:
                given_name, second_name, task_number, points = parts[2], parts[3], int(parts[1]), int(parts[4])

                # Insert or ignore into 'persons' table 
                cursor.execute("INSERT OR IGNORE INTO persons (given_name, second_name) VALUES (?, ?)", (given_name, second_name))

                # Get the person_id from 'persons' table
                cursor.execute("SELECT id FROM persons WHERE given_name = ? AND second_name = ?", (given_name, second_name))
                person_id = cursor.fetchone()[0]

                # Check if the entry already exists in 'scores' table   #ADDAT NU
                cursor.execute("SELECT COUNT(*) FROM scores WHERE person_id = ? AND task_number = ?", (person_id, task_number))
                existing_entry_count = cursor.fetchone()[0]

                if existing_entry_count > 0:
                    # Update the existing entry
                    cursor.execute("UPDATE scores SET points = ? WHERE person_id = ? AND task_number = ?", (points, person_id, task_number))
                else:
                    # Insert into 'scores' table
                    cursor.execute("INSERT INTO scores (task_number, points, person_id) VALUES (?, ?, ?)", (task_number, points, person_id))

    conn.commit()
    conn.close()


def print_tables(conn, c):
    print("Table: persons")
    for row in c.execute("SELECT * FROM persons;"):
        print(row)

def query_and_print_results():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()


    # (a) List the 10 persons with the highest total points
    query_a = '''
    SELECT p.given_name, p.second_name, SUM(s.points) AS total_points
    FROM persons AS p
    JOIN scores AS s ON p.id = s.person_id
    GROUP BY p.id
    ORDER BY total_points DESC
    LIMIT 10
    '''
    result_a = cursor.execute(query_a).fetchall()

    print("(a) List of 10 persons with the highest total points:")
    for row in result_a:
        print(row[0], row[1], row[2])

    # (b) List the 10 most difficult tasks
    query_b = '''
    SELECT task_number, SUM(points) AS total_points
    FROM scores 
    GROUP BY task_number
    ORDER BY total_points
    LIMIT 10
    '''
    result_b = cursor.execute(query_b).fetchall()

    print("\n(b) List of 10 most difficult tasks:")
    for row in result_b:
        print("Task", row[0], "Total Points:", row[1])

    conn.close()

if __name__ == "__main__":
    create_database()
    import_data()
    
    print("\nDo you want to print the generated tables? (yes/no)")
    user_input = input().lower()
    if user_input == 'yes':
        conn = sqlite3.connect("scores.db")
        cursor = conn.cursor()
        print_tables(conn, cursor)
        conn.close()
        

    query_and_print_results() 
