from src.search import SearxngSearch
from src.context import TOP_WEBSITES_CSV_PATH, PROGRESS_FILE, RESULTS_FILE_PATH


def main():
    # start = 1 start must from 1
    end = 20  # don't need to change 
    searxng_search = SearxngSearch(TOP_WEBSITES_CSV_PATH)
    searxng_search.run(end)
    print(f"\033[91m[END] Congratulations! You has crawled all domains, the failed domains are stored in {PROGRESS_FILE}, the results are stored in {RESULTS_FILE_PATH}. If you want to resume the progress, you can run it again, and don't worry it will be repeated.\033[0m")
    
if __name__ == "__main__":
    main()