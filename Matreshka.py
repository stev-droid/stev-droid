import tarfile
import gzip
import bz2
import os
import magic


def extract(filename, dest_dir='./extracted'):
    os.makedirs(dest_dir, exist_ok=True)

    if not os.path.exists(filename):
        return 'Файл не найден'

    file_mime = magic.from_file(filename, mime=True)

    if file_mime == 'application/x-tar':
        files = extract_tar(filename, dest_dir)
        for f in files:
            full_path = os.path.join(dest_dir, f)
            extract(full_path, dest_dir)

    elif file_mime == 'application/gzip':
        files = extract_gzip(filename, dest_dir)
        for f in files:
            extract(f, dest_dir)

    elif file_mime == 'application/x-bzip2':
        files = extract_bzip2(filename, dest_dir)
        for f in files:
            extract(f, dest_dir)

    elif file_mime == 'text/plain':
        print_content(filename)

    else:
        print(f"Неизвестный тип: {file_mime}")

def extract_tar(filename, dest_dir):
    with tarfile.open(filename) as tar:
        tar.extractall(dest_dir)  # распаковывает все файлы в dest_dir
        return tar.getnames()     #

def extract_gzip(filename, dest_dir):
    # убираем .gz из названия
    output_file = os.path.join(dest_dir, os.path.basename(filename)[:-3])
    with gzip.open(filename, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(f_in.read())
    return [output_file]

def extract_bzip2(filename, dest_dir):
    # убираем .bz2 из названия
    output_file = os.path.join(dest_dir, os.path.basename(filename)[:-4])
    with bz2.open(filename, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(f_in.read())
    return [output_file]

def print_content(filename):
    file_mime = magic.from_file(filename, mime=True)
    if file_mime == 'text/plain':
        print(f"\n=== Нашли файл: {filename} ===")
        with open(filename, 'r') as f:
            print(f.read())

if __name__ == '__main__':
    file_path = input("write a path to a file:")
    extract(file_path)
