import sys
import random
import json
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent

# ASCII Art Logo with Beta label
ASCII_LOGO = """
   /\\_/\\
  ( o.o )   [BETA]
   > ^ <
  /     \\
 |       |
  \\__/\\_/
  CatMCP Server - Fun Cat Jokes at Your Fingertips!
"""

# print logo to stderr on import/startup so it doesn't corrupt stdout (JSON-RPC)
sys.stderr.write(ASCII_LOGO + "\n")

# Initialize FastMCP Server
mcp = FastMCP(
    "CatMCP",
    instructions="A playful MCP server that serves purr-fect cat jokes, categorized, searchable, and ready to brighten anyone's day!"
)

# Core Joke Database
JOKES: List[Dict[str, Any]] = [
    {"id": 1, "category": "tech", "setup": "Why did the cat sit on the computer?", "punchline": "To keep an eye on the mouse!"},
    {"id": 2, "category": "classic", "setup": "What is a cat's favorite color?", "punchline": "Purr-ple!"},
    {"id": 3, "category": "puns", "setup": "What do you call a pile of kittens?", "punchline": "A meow-ntain!"},
    {"id": 4, "category": "tech", "setup": "Why was the cat sitting on the scanner?", "punchline": "It wanted to make a cat-py!"},
    {"id": 5, "category": "work", "setup": "What do you call a cat that can bowl?", "punchline": "An alley cat!"},
    {"id": 6, "category": "tech", "setup": "What is a cat's favorite software?", "punchline": "Claw-d services!"},
    {"id": 7, "category": "classic", "setup": "Why did the cat cross the road?", "punchline": "It was the chicken's day off!"},
    {"id": 8, "category": "classic", "setup": "What is a cat's favorite cereal?", "punchline": "Mice Krispies!"},
    {"id": 9, "category": "puns", "setup": "What did the cat say when it lost its toy?", "punchline": "You've got to be kitten me!"},
    {"id": 10, "category": "silly", "setup": "How do cats paint their claws?", "punchline": "With claw-polish!"},
    {"id": 11, "category": "classic", "setup": "What is a cat's favorite song?", "punchline": "Three Blind Mice!"},
    {"id": 12, "category": "silly", "setup": "Why do cats make terrible storytellers?", "punchline": "Because they only have one tail!"},
    {"id": 13, "category": "work", "setup": "What is a cat's favorite school subject?", "punchline": "His-tory!"},
    {"id": 14, "category": "tech", "setup": "Why are cats so bad at video games?", "punchline": "They keep getting distracted by the mouse on the screen!"},
    {"id": 15, "category": "puns", "setup": "What do you call a cat that is a magician?", "punchline": "A magic-claw-n!"},
    {"id": 16, "category": "silly", "setup": "What do cats like to eat on hot days?", "punchline": "Mice-cream cones!"},
    {"id": 17, "category": "work", "setup": "What did the cat say when it got graded?", "punchline": "I got a purr-fect score!"},
    {"id": 18, "category": "puns", "setup": "Why don't cats play poker in the jungle?", "punchline": "Too many cheetahs!"},
    {"id": 19, "category": "silly", "setup": "What is a cat's favorite discount?", "punchline": "Buy one, get one furry!"},
    {"id": 20, "category": "puns", "setup": "What did the cat say when it got confused?", "punchline": "I am completely fur-plexed!"},
    {"id": 21, "category": "tech", "setup": "How does a cat write a database query?", "punchline": "SELECT * FROM cats WHERE tail_wag = True;"},
    {"id": 22, "category": "work", "setup": "Why did the cat go to medical school?", "punchline": "To become a purr-geon!"},
    {"id": 23, "category": "puns", "setup": "What do cats do when they are mad?", "punchline": "They throw a hiss-ty fit!"},
    {"id": 24, "category": "classic", "setup": "Why are cats so good at singing?", "punchline": "They are natural meow-sicians!"}
]


@mcp.tool()
def get_random_joke(category: Optional[str] = None) -> str:
    """
    Retrieve a random cat joke.

    Args:
        category: Optional category to filter jokes (e.g. 'tech', 'classic', 'puns', 'silly', 'work').
    """
    if category:
        normalized_cat = category.strip().lower()
        filtered = [j for j in JOKES if j["category"] == normalized_cat]
        if not filtered:
            valid_cats = ", ".join(list_categories())
            raise ValueError(f"Category '{category}' not found. Choose from: {valid_cats}")
        joke = random.choice(filtered)
    else:
        joke = random.choice(JOKES)

    return f"{joke['setup']}\n\n{joke['punchline']}"


@mcp.tool()
def list_categories() -> List[str]:
    """
    Get a list of all available cat joke categories.
    """
    categories = sorted(list(set(joke["category"] for joke in JOKES)))
    return categories


@mcp.tool()
def search_jokes(keyword: str) -> List[str]:
    """
    Search jokes for a specific keyword in the setup or punchline.

    Args:
        keyword: Case-insensitive search keyword.
    """
    normalized_kw = keyword.strip().lower()
    if not normalized_kw:
        return []

    matches = []
    for j in JOKES:
        if normalized_kw in j["setup"].lower() or normalized_kw in j["punchline"].lower() or normalized_kw in j["category"].lower():
            matches.append(f"[{j['category'].upper()}] {j['setup']} -> {j['punchline']}")

    return matches


@mcp.resource("jokes://all")
def get_all_jokes() -> str:
    """
    Get the complete list of cat jokes in JSON format.
    """
    return json.dumps(JOKES, indent=2)


@mcp.resource("jokes://categories")
def get_categories_info() -> str:
    """
    Get a summary of categories and their joke counts in JSON format.
    """
    counts: Dict[str, int] = {}
    for j in JOKES:
        counts[j["category"]] = counts.get(j["category"], 0) + 1

    summary = {
        "total_jokes": len(JOKES),
        "categories": counts
    }
    return json.dumps(summary, indent=2)


@mcp.resource("jokes://random")
def get_random_joke_resource() -> str:
    """
    Get a dynamically selected random cat joke in plain text.
    """
    joke = random.choice(JOKES)
    return f"Category: {joke['category'].upper()}\n\n{joke['setup']}\n{joke['punchline']}"


@mcp.prompt()
def tell_cat_joke(category: Optional[str] = None, tone: Optional[str] = "funny") -> List[PromptMessage]:
    """
    Create a prompt instructing the LLM to deliver a cat joke in a specific tone.

    Args:
        category: Optional joke category to base the joke on.
        tone: The tone the comedian should adopt (e.g. 'hilarious', 'dry', 'enthusiastic', 'sarcastic').
    """
    # Select a joke for inspiration
    if category:
        normalized_cat = category.strip().lower()
        filtered = [j for j in JOKES if j["category"] == normalized_cat]
        if filtered:
            joke = random.choice(filtered)
        else:
            joke = random.choice(JOKES)
            category = joke["category"]
    else:
        joke = random.choice(JOKES)
        category = joke["category"]

    system_instructions = (
        "You are CatComedian, an extremely witty and charismatic stand-up comedian whose material is strictly cat-themed. "
        "You speak with enthusiasm, adore cat puns, and always aim to bring a smile. "
        "Your task is to take a given cat joke and deliver it to the user in a theatrical, highly engaging way."
    )

    user_message = (
        f"Please tell me a joke about cats! Use a '{tone}' tone.\n\n"
        f"Here is a joke for your inspiration (Category: {category}):\n"
        f"Setup: {joke['setup']}\n"
        f"Punchline: {joke['punchline']}\n\n"
        f"Do not just repeat the joke verbatim. Build up a humorous story or monologue around it, "
        f"adopting your persona and the '{tone}' tone requested!"
    )

    return [
        PromptMessage(
            role="user",
            content=TextContent(type="text", text=f"System Prompt: {system_instructions}\n\nUser Request: {user_message}")
        )
    ]


def main():
    mcp.run()


if __name__ == "__main__":
    main()