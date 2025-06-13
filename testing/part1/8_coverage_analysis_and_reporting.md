## Coverage Analysis

Code coverage measures how much of the code is executed when tests run, It helps find:

- Unused / untested parts of your code
    
- Missing edge-case tests
    

```bash
pytest --cov=your_package tests/
```

Output Example

```bash
Name                        Stmts   Miss  Cover
-----------------------------------------------
your_package/__init__.py       1      0   100%
your_package/api.py           20      2    90%
your_package/utils.py         50     10    80%
-----------------------------------------------
TOTAL                         71     12    83%

```
- it will show for each file
    - Total number of executable statements (lines of code) in the file.
    - Number of statements that were not executed during the test run
    - Percentage of statements that were covered by tests
 
### Generate HTML Repor

```bash
pytest --cov=your_package --cov-report=html
```


### Kind of coverage 
- `Statement Coverage (--cov)`, Whether each line of code was executed at least once during the test run.
- `Branch Coverage (--cov-branch)`, Whether each possible path (True/False) of conditionals was executed.



### Acording to Google the Aim should be to achive 80–90% coverage

###  High coverage doesn’t mean your tests are good — but low coverage almost always means your tests are insufficient (Martin Fowler) 