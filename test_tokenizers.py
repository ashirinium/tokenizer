# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-return-statements, too-many-branches, too-many-statements, too-many-locals
# pylint: disable=invalid-name

import pytest
import tokenizer as tk_recursive
import tokenizer_stack as tk_stack

@pytest.fixture
def sample_data():
    sample_input = None
    with open("sample_input.txt", "r", encoding="utf-8") as file:
        sample_input = file.read()
    expected_output = None
    with open("sample_output.txt", "r", encoding="utf-8") as file:
        expected_output = file.read()
    return sample_input, expected_output

def test_tokenizer_recursive(sample_data):
    sample_input, expected_output = sample_data
    print("Running test on recursive tokenizer...", end=" ")
    tokens = tk_recursive.tokenize(sample_input)
    __test_tokenizer(tokens, expected_output)

def test_tokenizer_stack(sample_data):
    sample_input, expected_output = sample_data
    print("Running test on stack tokenizer...", end=" ")
    tokens = tk_stack.tokenize(sample_input)
    __test_tokenizer(tokens, expected_output)

def __test_tokenizer(tokens: [str], expected_output: [str]):
    try:
        curr_idx = 0
        for token in tokens:
            assert token == expected_output[curr_idx], f"Expected {expected_output[curr_idx]} but got {token} instead. Index: {curr_idx}"
            curr_idx += 1
        print("Successfully passed test!")
    except AssertionError as err:
        print("Failed test!")
        print(err)
