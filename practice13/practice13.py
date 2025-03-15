import sqlite3
import pandas as pd

# Створення бази даних
db_name = "MilitaryEquipmentDB.sqlite"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Створення таблиці EquipmentRegistry
cursor.execute("""
CREATE TABLE IF NOT EXISTS EquipmentRegistry (
    EquipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Type TEXT NOT NULL,
    Status TEXT NOT NULL CHECK(Status IN ('Operational', 'Under Maintenance', 'Decommissioned')),
    Location TEXT NOT NULL,
    LastMaintenanceDate DATE NOT NULL
)
""")

# Додавання тестових даних
test_data = [
    ("Tank T-80", "Tank", "Operational", "Base Alpha", "2025-01-10"),
    ("BMP-2", "Infantry Fighting Vehicle", "Under Maintenance", "Base Bravo", "2025-02-20"),
    ("S-300", "Air Defense System", "Operational", "Base Delta", "2025-03-05"),
    ("Msta-S", "Self-propelled Artillery", "Decommissioned", "Base Gamma", "2024-12-15"),
    ("Mi-24", "Helicopter", "Operational", "Base Echo", "2025-01-30")
]

cursor.executemany("""
INSERT INTO EquipmentRegistry (Name, Type, Status, Location, LastMaintenanceDate)
VALUES (?, ?, ?, ?, ?)
""", test_data)

conn.commit()

# Отримання всіх записів
cursor.execute("SELECT * FROM EquipmentRegistry")
data = cursor.fetchall()

# Закриття з'єднання
conn.close()

# Перетворення в DataFrame для зручного перегляду
df_equipment = pd.DataFrame(data, columns=["EquipmentID", "Name", "Type", "Status", "Location", "LastMaintenanceDate"])

# Вивід результату
print(df_equipment)
