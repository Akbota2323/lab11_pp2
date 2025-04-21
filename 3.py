import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="neondb",
    user="neondb_owner",
    password="npg_rh8LOJKZfYV6",
    host="ep-black-poetry-a4mrtnaa-pooler.us-east-1.aws.neon.tech",
    port="5432",
    sslmode="require"
)
cur = conn.cursor()

# Функция для добавления или обновления контакта (Upsert)
def upsert_entry(name, phone):
    try:
        cur.execute("CALL upsert_phonebook(%s, %s)", (name, phone))
        conn.commit()
        print(f"Контакт {name} добавлен или обновлён!")
    except Exception as e:
        print(f"Ошибка при добавлении или обновлении контакта: {e}")
        conn.rollback()

# Функция для удаления контакта
def delete_entry(keyword):
    try:
        cur.execute("CALL delete_phonebook_entry(%s)", (keyword,))
        conn.commit()
        print(f"Контакт с {keyword} удалён!")
    except Exception as e:
        print(f"Ошибка при удалении контакта: {e}")
        conn.rollback()

# Функция для поиска по имени или номеру телефона
def search_entries(pattern):
    try:
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Контакты не найдены!")
    except Exception as e:
        print(f"Ошибка при поиске контактов: {e}")

# Функция для просмотра с пагинацией
def paginate_entries(limit, offset):
    try:
        cur.execute("SELECT * FROM paginate_phonebook(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Нет данных для отображения!")
    except Exception as e:
        print(f"Ошибка при пагинации: {e}")

# Меню для работы с базой данных
def main():
    while True:
        print("\n--- Телефонная книга ---")
        print("1. Поиск")
        print("2. Добавить или обновить контакт")
        print("3. Просмотр с пагинацией")
        print("4. Удалить контакт")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            keyword = input("Введите имя или номер для поиска: ")
            search_entries(keyword)
        elif choice == "2":
            name = input("Введите имя: ")
            phone = input("Введите номер телефона: ")
            upsert_entry(name, phone)
        elif choice == "3":
            limit = int(input("Введите количество записей на странице: "))
            offset = int(input("Введите смещение (номер страницы): ")) * limit
            paginate_entries(limit, offset)
        elif choice == "4":
            keyword = input("Введите имя или номер для удаления: ")
            delete_entry(keyword)
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
