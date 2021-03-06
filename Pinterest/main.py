import os
import random
import argparse
from itertools import combinations
from src import PinterestScraper, PinterestConfig

def remove_dir(filename):
    if os.path.exists(filename):
        os.remove(filename)

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", default="keywords.txt", help="path to input image")
    parser.add_argument('--output', help='output dir', default='photos', type=str)
    parser.add_argument("-nw", '--number-of-words', help='number of keywords for search', default=2, type=int)
    args = parser.parse_args()

    #debug
    print('----------------------')
    print(args)

    file = open(args.keywords, "r")
    keywords = file.read().split('\n')
    keywords = [keyword.strip() for keyword in keywords]

    #debug
    print('-------------------')
    print(keywords)

    make_dir('./debug')

    remove_dir('debug/get_urls.json')
    remove_dir('debug/resource_response.json')
    remove_dir('debug/data.json')
    remove_dir('debug/results.json')

    # print("start crawling...")
    random.shuffle(keywords)
    counter = 0
    if len(keywords)==1:args.number_of_words=1
    for item in combinations(keywords, args.number_of_words):
        if counter == 4:
            break

        keyword = " ".join(word for word in item)
        print(keyword)

        while True:
            configs = PinterestConfig(search_keywords=keyword,  # Search word
                                    file_lengths=5000,  # total number of images to download (default = "100")
                                    image_quality="originals",  # image quality (default = "orig")
                                    bookmarks="",  # next page data (default= "")
                                    scroll=10000)

            print('--------------------')
            print(configs.image_data)

            number = PinterestScraper(configs).download_images(args.output)  # download images directly
            print("number:", number)
            if number == 0:
                counter += 1
                break
            else:
                counter = 0

    print("All images in dir:", len(os.listdir(args.output)))