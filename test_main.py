import pytest
import json
from mcp.types import PromptMessage, TextContent
from main import (
    get_random_joke,
    list_categories,
    search_jokes,
    get_all_jokes,
    get_categories_info,
    get_random_joke_resource,
    tell_cat_joke,
    JOKES
)

def test_list_categories():
    categories = list_categories()
    assert isinstance(categories, list)
    assert len(categories) > 0
    # Expected categories in our database
    assert "tech" in categories
    assert "classic" in categories
    assert "puns" in categories
    assert "silly" in categories
    assert "work" in categories

def test_get_random_joke_no_category():
    joke = get_random_joke()
    assert isinstance(joke, str)
    assert "\n\n" in joke # Separator between setup and punchline

    # Verify the joke is indeed from our list
    parts = joke.split("\n\n")
    setup, punchline = parts[0], parts[1]
    matching_jokes = [j for j in JOKES if j["setup"] == setup and j["punchline"] == punchline]
    assert len(matching_jokes) == 1

def test_get_random_joke_valid_category():
    joke = get_random_joke("tech")
    assert isinstance(joke, str)
    parts = joke.split("\n\n")
    setup, punchline = parts[0], parts[1]
    matching_jokes = [j for j in JOKES if j["setup"] == setup and j["punchline"] == punchline]
    assert len(matching_jokes) == 1
    assert matching_jokes[0]["category"] == "tech"

def test_get_random_joke_invalid_category():
    with pytest.raises(ValueError) as excinfo:
        get_random_joke("nonexistent_category_xyz")
    assert "Category 'nonexistent_category_xyz' not found" in str(excinfo.value)

def test_search_jokes_matches():
    results = search_jokes("computer")
    assert isinstance(results, list)
    assert len(results) >= 1
    assert any("computer" in r.lower() for r in results)

def test_search_jokes_case_insensitive():
    results_upper = search_jokes("COMPUTER")
    results_lower = search_jokes("computer")
    assert results_upper == results_lower

def test_search_jokes_no_match():
    results = search_jokes("dog_barking_sound")
    assert isinstance(results, list)
    assert len(results) == 0

def test_get_all_jokes_resource():
    jokes_json = get_all_jokes()
    assert isinstance(jokes_json, str)
    data = json.loads(jokes_json)
    assert isinstance(data, list)
    assert len(data) == len(JOKES)
    assert data[0]["setup"] == JOKES[0]["setup"]

def test_get_categories_info_resource():
    categories_json = get_categories_info()
    assert isinstance(categories_json, str)
    data = json.loads(categories_json)
    assert "total_jokes" in data
    assert "categories" in data
    assert data["total_jokes"] == len(JOKES)
    assert data["categories"]["tech"] >= 1

def test_get_random_joke_resource():
    res = get_random_joke_resource()
    assert isinstance(res, str)
    assert "Category:" in res

def test_tell_cat_joke_prompt():
    messages = tell_cat_joke(category="tech", tone="sarcastic")
    assert isinstance(messages, list)
    assert len(messages) == 1
    msg = messages[0]
    assert isinstance(msg, PromptMessage)
    assert msg.role == "user"
    assert isinstance(msg.content, TextContent)
    assert "sarcastic" in msg.content.text
    assert "CatComedian" in msg.content.text
