import os
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server


def get_files_path(folder):
    files = []
    for file_name in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file_name)):
            files.append(os.path.join(folder, file_name))
    return files


def get_files_content(file_names):
    files_content = []
    for file in file_names:
        with open(file, 'r', encoding='utf8') as my_file:
            files_content.append(json.load(my_file))
    return files_content


def on_reload():
    cars_folder = 'json_database'
    media_folder = 'media'
    cars_files = get_files_path(cars_folder)
    img_path = get_files_path(media_folder)
    cars = get_files_content(cars_files)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    page_cars_limit = 20
    cars_pages = list(chunked(cars, page_cars_limit))
    pages_count = len(cars_pages)

    for page_number, cars_on_page in enumerate(cars_pages, 1):
        sorted_cars = list(chunked(cars_on_page, 1))
        rendered_page = template.render(
            pages=pages_count,
            page_number=page_number,
            cars=sorted_cars,
            images=img_path
        )
        with open(f'pages/index{page_number}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    Path('pages').mkdir(parents=True, exist_ok=True)
    on_reload()
    
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.',  default_filename='pages/index1.html')
    

if __name__ == '__main__':
    main()


# #list(chunked(books_on_page, row_cars_limit))
    # for carss in cars:
    #     for car in carss:
    #         print(car)
