import os
import shutil
import zipfile
from typing import List


def normalize(input_str: str, is_unknown: bool = False) -> str:
    """
    Normalize a string by transliterating Cyrillic characters
        and using only letters and digits.

    :param input_str: Input string
    :param is_unknown: Indicates whether the string should
        be treated as an unknown file
    :return: Normalized string
    """
    translit_mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
        'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia'
    }

    name, extension = os.path.splitext(input_str)
    normalized_name = ''

    if len(name) == 1 and name.isalpha():
        return translit_mapping.get(name.lower(), name)

    for orig_char in name:
        if orig_char.lower() in translit_mapping:
            translit_char = translit_mapping[orig_char.lower()]
            if orig_char.isupper():
                translit_char = translit_char.capitalize()
            normalized_name += translit_char
        elif orig_char.isalnum():
            normalized_name += orig_char
        else:
            normalized_name += '_'

    if is_unknown:
        result = f"{normalized_name}{extension.lower()}"
    else:
        result = f"{normalized_name}{extension}"

    print(f"Input: {input_str}, Output: {result}")

    return result


def categorize_file(file_path: str) -> str:
    """
    Categorize a file based on its extension.

    :param file_path: Path to the file
    :return: File category (images, video, documents, audio, archives, unknown)
    """
    extension = file_path.split('.')[-1].upper()
    if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
        return 'images'
    elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
        return 'video'
    elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
        return 'documents'
    elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
        return 'audio'
    elif extension in ('ZIP', 'GZ', 'TAR'):
        return 'archives'
    else:
        return 'unknown'


def extract_archive(archive_path: str, extract_to: str) -> None:
    """
    Extract an archive and transliterate the names of the files in it.

    :param archive_path: Path to the archive
    :param extract_to: Folder for extraction
    """
    if zipfile.is_zipfile(archive_path):
        archive_folder_name = os.path.splitext(
            os.path.basename(archive_path))[0]
        archive_folder = os.path.join(
            extract_to, 'archives', archive_folder_name)
        os.makedirs(archive_folder, exist_ok=True)

        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                file_name_without_extension, file_extension = os.path.splitext(
                    file_info.filename)
                if file_name_without_extension:
                    normalized_name = normalize(
                        file_name_without_extension, is_unknown=True)
                    extracted_file_path = os.path.join(
                        archive_folder, f"{normalized_name}{file_extension}")
                    zip_ref.extract(file_info, archive_folder)
                    os.rename(
                        os.path.join(
                            archive_folder,
                            file_info.filename),
                        extracted_file_path)
                    print(f"Extracted file: {extracted_file_path}")


def remove_old_archives(folder: str) -> None:
    """
    Remove old archives from a folder.

    :param folder: Path to the folder
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if categorize_file(file_path) == 'archives':
                os.remove(file_path)


def process_folder(folder_path: str, destination_folder: str,
                   empty_folders: List[str]) -> None:
    """
    Process the contents of a folder, move files,
        and recursively call itself for subfolders.

    :param folder_path: Path to the folder
    :param destination_folder: Folder for moving files
    :param empty_folders: List of empty folders
    """
    print(f"Processing folder: {folder_path}")

    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            destination = categorize_file(item_path)
            normalized_name = normalize(
                os.path.basename(item_path),
                destination == 'unknown')

            if destination == 'archives':
                extract_archive(item_path, destination_folder)
            else:
                new_file_path = os.path.join(
                    destination_folder, destination, normalized_name)
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                shutil.move(item_path, new_file_path)

        elif os.path.isdir(item_path):
            process_folder(item_path, destination_folder, empty_folders)

    if not os.listdir(folder_path):
        empty_folders.append(folder_path)


def create_category_folders(root_folder: str, destination_folder: str) -> None:
    """
    Create folders for file categories.

    :param root_folder: Root folder where categories are located
    :param destination_folder: Folder for categories
    """
    categories = [
        'images',
        'video',
        'documents',
        'audio',
        'archives',
        'unknown']
    for category in categories:
        if category not in ['archives', 'video',
                            'audio', 'documents', 'images']:
            category_path = os.path.join(destination_folder, category)
            os.makedirs(category_path, exist_ok=True)


def remove_empty_folders(folder: str) -> None:
    """
    Remove empty folders.

    :param folder: Path to the folder
    """
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty folder: {dir_path}")
                except OSError as e:
                    print(f"Failed to remove empty folder {dir_path}: {e}")


def list_files_by_category(folder: str, output_file: str) -> None:
    """
    Create a list of files by category and write it to a text file.

    :param folder: Path to the folder with categories
    :param output_file: Path to the output file
    """
    categories = [
        'images',
        'video',
        'documents',
        'audio',
        'archives',
        'unknown']
    with open(output_file, 'w', encoding='utf-8') as output_file_handle:
        for category in categories:
            output_file_handle.write(f"\nFiles in category {category}:\n")
            category_path = os.path.join(folder, category)
            for root, dirs, files in os.walk(category_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    output_file_handle.write(f"{file_path}\n")


def list_known_extensions(folder: str, output_file: str,
                          known_extensions: set) -> None:
    """
    List known extensions and write them to a text file.

    :param folder: Path to the folder with known extensions
    :param output_file: Path to the output file
    :param known_extensions: List of known extensions
    """
    with open(output_file, 'a', encoding='utf-8') as output_file_handle:
        output_file_handle.write("\nKnown extensions:\n")
        known_extensions_str = ', '.join(sorted(known_extensions))
        output_file_handle.write(known_extensions_str)


def list_unknown_extensions(folder: str, output_file: str) -> None:
    """
    List unknown extensions and write them to a text file.

    :param folder: Path to the folder with unknown extensions
    :param output_file: Path to the output file
    """
    with open(output_file, 'a', encoding='utf-8') as output_file_handle:
        output_file_handle.write("\nUnknown extensions:\n")
        unknown_extensions = set()
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if categorize_file(file_path) == 'unknown':
                    unknown_extensions.add(os.path.splitext(file_name)[-1][1:])
        unknown_extensions_str = ', '.join(sorted(unknown_extensions))
        output_file_handle.write(unknown_extensions_str)


def process_folder(folder_path: str, destination_folder: str, empty_folders: List[str]) -> None:
    """
    Process the contents of a folder, move files,
        and recursively call itself for subfolders.

    :param folder_path: Path to the folder
    :param destination_folder: Folder for moving files
    :param empty_folders: List of empty folders
    """
    print(f"Processing folder: {folder_path}")

    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        try:
            if os.path.isfile(item_path):
                destination = categorize_file(item_path)
                normalized_name = normalize(
                    os.path.basename(item_path),
                    destination == 'unknown')

                if destination == 'archives':
                    extract_archive(item_path, destination_folder)
                else:
                    new_file_path = os.path.join(
                        destination_folder, destination, normalized_name)
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.move(item_path, new_file_path)

            elif os.path.isdir(item_path):
                process_folder(item_path, destination_folder, empty_folders)

        except PermissionError as e:
            print(f"Ignoring Permission error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    if not os.listdir(folder_path):
        empty_folders.append(folder_path)


def sorted_folder(folder_path: str) -> str:
    """
    Sort and categorize files in the specified folder.

    :param folder_path: Path to the folder to be sorted
    """
    destination_folder = folder_path
    output_file = os.path.join(folder_path, 'results.txt')

    create_category_folders(folder_path, destination_folder)
    empty_folders = []
    process_folder(folder_path, destination_folder, empty_folders)
    remove_old_archives(folder_path)
    list_files_by_category(destination_folder, output_file)

    known_extensions = {
        'JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV',
        'MKV', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX',
        'MP3', 'OGG', 'WAV', 'AMR', 'ZIP', 'GZ', 'TAR'
    }

    list_known_extensions(destination_folder, output_file, known_extensions)
    list_unknown_extensions(destination_folder, output_file)
    remove_empty_folders(folder_path)
    remove_empty_folders(destination_folder)

    return output_file