## Parametrization

- Parametrize lets you test a single test function with multiple sets of data.

### Example 

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 7, 12),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```
### Benefits

- Avoids **code repetition**.
    
- Keeps your test cases **organized and readable**.
    
- Very helpful when testing functions with **lots of input variations**.

### Note
- Parametrize + Fixtur

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3, 4]

@pytest.mark.parametrize("item", [1, 3, 4])
def test_item_in_list(item, sample_list):
    assert item in sample_list

```