# 2FA-Spider
This repo is for the 2fa research, including spider and other stuff.

## Build

This project is built on Python 3.8.

If you want to run this project, you first need to install the packages that this project depends on:

```sh
pip install -r requirements.txt
```

Then you need to run all the test cases to prove that the program can run correctly on your computer.

```sh
python -m unittest discover -s tests -p "test_*.py"
```

If all the above are OK, enter the following command to run the program:

```sh
python main.py
```

## Other

If you want to limit the scope of the crawl, please modify the start and end ranges in the main function in main.py. The default is to crawl the first 10,000 domains.

```python
def main():
    end = 10000  # don't need to change 
```

**Attention**

To ensure the consistency of the crawler, it is strongly recommended that you do not modify the start and end ranges after running the program for the first time, because the program will record the results of failed crawls in the progress. If you modify the range, it is easy to cause some domains to not be covered.

Therefore, after you run `python main.py` and end the program, if there are domains in progress.json that **failed to crawl**, you only need to run `python main.py` again!
