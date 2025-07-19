# Unit and Integration Tests

This project contains unit and integration tests for the `utils.py` and `client.py` modules. The tests cover the `access_nested_map`, `get_json`, and `memoize` functions in `utils.py`, and the `GithubOrgClient` class in `client.py`, using Python's `unittest` framework, `unittest.mock`, and `parameterized`.

## Files
- `test_utils.py`: Unit tests for `utils.py`.
- `test_client.py`: Unit and integration tests for `client.py`.
- `utils.py`, `client.py`, `fixtures.py`: Provided files containing the code and data to test.

## Running Tests
Run the tests with:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py