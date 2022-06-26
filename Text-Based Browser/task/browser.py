import os
import argparse
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore


# Get arguments from command line
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_name')
    return parser.parse_args()


# Make a directory with the arguments if it doesn't exist
def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass


# Read a page after it's been saved to a file
def read_page_from_file(file_name):
    file = open(f'{args.folder_name}/{url[:-4]}', 'r')
    text = file.read()
    file.close()
    return text


# Write to file after parsing
def write_to_file(file_name, text):
    file = open(f'{args.folder_name}/{url[:-4]}', 'w')
    formatted_text = parse_page(text)
    file.write(formatted_text)
    file.close()
    return formatted_text


# Get web page with valid URL
def get_web_page(link):
    if 'https://' not in link:
        link = 'https://' + link

    r = requests.get(link)
    return r.content


# Parse readable text from HTML
def parse_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    tag_list = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'a', 'ul', 'ol', 'li'])
    cleaned_list = []

    for line in tag_list:
        if line.text != '' and line.text != '\n':
            text = line.text
            if line.name == 'a':
                text = Fore.BLUE + text

            cleaned_list.append(text)

    return '\n'.join(str(e) for e in cleaned_list)


args = get_args()
stack = deque()

make_dir(args.folder_name)

while True:
    url = input()
    # If URL, get it from web, print it, and save it
    if "." in url:
        page = get_web_page(url)
        print(write_to_file(url[:-4], page))
        stack.append(url)
    # Exit procedure
    elif url == 'exit':
        sys.exit()
    # Pop stack
    elif url == 'back':
        try:
            stack.pop()
            file_name = stack.pop()
            # Read and print the file
            print(read_page_from_file(file_name))

        except IndexError:
            continue
    # Read from file
    elif os.access(f'{args.folder_name}/{url[:-4]}', os.F_OK):
        print(read_page_from_file(url[:-4]))
    else:
        print('Incorrect URL')
