import json
import os

BOOKS_FILE = "books.json"


def load_books():
    """Загрузка списка книг из JSON-файла."""
    if not os.path.exists(BOOKS_FILE):
        return []

    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except (json.JSONDecodeError, OSError):
        print("Ошибка: не удалось загрузить данные, файл повреждён или недоступен.")
        return []


def save_books(books):
    """Сохранение списка книг в JSON-файл."""
    try:
        with open(BOOKS_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    except OSError:
        print("Ошибка: не удалось сохранить данные в файл.")


def print_menu():
    """Печать текстового меню."""
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Показать среднюю оценку")
    print("4. Статистика по авторам")
    print("5. Удалить книгу")
    print("6. Выход")


def input_rating():
    """Ввод и проверка оценки от 1 до 5."""
    while True:
        value = input("Введите оценку (1–5): ").strip()
        if not value.isdigit():
            print("Ошибка: введите число от 1 до 5.")
            continue
        rating = int(value)
        if 1 <= rating <= 5:
            return rating
        print("Ошибка: оценка должна быть от 1 до 5.")


def add_book(books):
    """Добавление новой книги в список с проверкой дубликатов."""
    author = input("Автор: ").strip()
    title = input("Название: ").strip()
    rating = input_rating()
    date = input("Дата прочтения (например, 2024-12-31): ").strip()

    # Проверка дубликатов по паре автор + название
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print("Такая книга уже есть в списке.")
            return

    book = {
        "author": author,
        "title": title,
        "rating": rating,
        "date": date,
    }
    books.append(book)
    save_books(books)
    print("Книга добавлена.")


def show_all_books(books):
    """Вывод всех книг."""
    if not books:
        print("Список книг пуст.")
        return

    for idx, book in enumerate(books, start=1):
        print(
            f"{idx}. {book['author']} — \"{book['title']}\" "
            f"(оценка: {book['rating']}, дата: {book['date']})"
        )


def show_average_rating(books):
    """Вывод средней оценки по всем книгам."""
    if not books:
        print("Нет книг для расчёта средней оценки.")
        return

    total = sum(book["rating"] for book in books)
    avg = total / len(books)
    print(f"Средняя оценка: {avg:.2f}")


def show_author_stats(books):
    """Статистика: сколько книг у каждого автора."""
    if not books:
        print("Список книг пуст.")
        return

    stats = {}
    for book in books:
        author = book["author"]
        stats[author] = stats.get(author, 0) + 1

    print("Статистика по авторам:")
    for author, count in stats.items():
        print(f"{author}: {count} книг(и)")


def delete_book(books):
    """Удаление книги по номеру в списке."""
    if not books:
        print("Список книг пуст, нечего удалять.")
        return

    show_all_books(books)

    value = input("Введите номер книги для удаления: ").strip()
    if not value.isdigit():
        print("Ошибка: нужно ввести номер книги.")
        return

    idx = int(value)
    if not 1 <= idx <= len(books):
        print("Ошибка: нет книги с таким номером.")
        return

    removed = books.pop(idx - 1)
    save_books(books)
    print(f"Книга \"{removed['title']}\" автора {removed['author']} удалена.")


def main():
    books = load_books()

    while True:
        print()
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            show_all_books(books)
        elif choice == "3":
            show_average_rating(books)
        elif choice == "4":
            show_author_stats(books)
        elif choice == "5":
            delete_book(books)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 1 до 6.")


if __name__ == "__main__":
    main()