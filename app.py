
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

from cli.models.address_book import AddressBook
from cli.models.notebook import Notebook

from cli.services.address_book_service import add_contact, change_contact, get_phone, get_all_contacts, add_birthday, \
    show_birthday, delete_contact, change_birthday, change_email, change_name, get_birthdays, \
    add_email, add_address, add_phone, get_all_contacts_object, get_contacts_content
from cli.services.file_service import write_data_to_file, read_data_from_file
from cli.services.input_helper import get_help, prompt_handler
from cli.services.notebook_service import add_note, get_all_notes, edit_note, delete_note, get_all_notes_object, \
    get_notes_content
from cli.services.search_service import search

from cli.utils.helpers import parse_input, hello, rich_console, rich_console_error, progress_bar


def main():
    book = AddressBook()
    notebook = Notebook()
    console = Console()
    book_from_file = read_data_from_file("book.pkl")
    notebook_from_file = read_data_from_file("notebook.pkl")

    if book_from_file is not None:
        book = book_from_file

    if notebook_from_file is not None:
        notebook = notebook_from_file

    print("Welcome to the assistant bot!")
    print(get_help())
    hello()

    while True:
        user_input = prompt_handler("Enter a command: ")
        command, *args = parse_input(user_input)

        progress_bar()

        if command in ["close", "exit"]:
            rich_console("Good bye!")
            break
        elif command == "hello":
            rich_console("Hi! How can I help you?")
            print("Hi! How can I help you?")
        elif command == "help":
            pass
        elif command == "add":
            rich_console(add_contact(args, book=book))
        elif command == "add-phone":
            rich_console(add_phone(args, book=book))
        elif command == "add-birthday":
            rich_console(add_birthday(args, book=book))
        elif command == "add-address":
            rich_console(add_address(args, book=book))
        elif command == "add-email":
            rich_console(add_email(args, book=book))
        elif command == "add-note":
            rich_console(add_note(args, notebook=notebook))
        elif command == "change":
            rich_console(change_contact(args, book=book))
        elif command == "change-birthday":
            rich_console(change_birthday(args, book=book))
        elif command == "change-email":
            rich_console(change_email(args, book=book))
        elif command == "change-name":
            rich_console(change_name(args, book=book))
        elif command == "edit-note":
            rich_console(edit_note(args, notebook=notebook))
        elif command == "delete":
            rich_console(delete_contact(args, book=book))
        elif command == "delete-note":
            rich_console(delete_note(args, notebook=notebook))
        elif command == "all":
            users = get_all_contacts_object(book)
            user_renderables = [Panel(get_contacts_content(user), expand=True) for user in users]
            if user_renderables:
                console.print(Columns(user_renderables))
            else:
                console.print("Contact book is empty.")
        elif command == "all-notes":
            notes = get_all_notes_object(notebook)
            note_renderables = [Panel(get_notes_content(note), expand=True) for note in notes]
            console.print(Columns(note_renderables, equal=True, expand=True))
        elif command == "show-birthday":
            rich_console(show_birthday(args, book=book))
        elif command == "birthdays":
            rich_console(get_birthdays(book=book, days_in_advance=args[0] if args else None))
        elif command == "phone":
            rich_console(get_phone(args, book=book))
        elif command == "search":
            rich_console(search(args, book=book))
        else:
            rich_console_error("Invalid command.")

        write_data_to_file("book.pkl", book)
        write_data_to_file("notebook.pkl", notebook)


if __name__ == "__main__":
    main()
