"""Test different character creation prompts to find what generates variety."""

import asyncio
import random
import string
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from mmo.settings import settings


class Character(BaseModel):
    """A character for the game."""

    name: str = Field(description="Character's name")
    description: str = Field(description="3-4 sentence description that others see")
    backstory: str = Field(description="Fuller backstory for the player's reference")


# Different prompt strategies to test
PROMPT_STRATEGIES = {
    "baseline": """Create a unique character for a multiplayer dungeon crawler game.
Be creative and avoid clichés.""",
    "banned_names": """Create a unique character for a multiplayer dungeon crawler game.
AVOID these overused names: Zephyr, Shadow, Raven, Phoenix, Storm, Whisper, Luna, Orion.
Be creative and avoid clichés.""",
    "mundane_focus": """Create a character for a multiplayer dungeon crawler.
Focus on mundane, specific details rather than epic or mystical elements.
Think about ordinary people who ended up in an extraordinary situation.
Make them feel real through small, concrete details.""",
    "association_method": """Create a character using this method:
1. Start with the letters "{letters}" - think of an ordinary word that begins with these
2. Free associate from that word 4-5 times 
3. Use your final association as inspiration for the character
4. Give them a specific, non-dramatic flaw
5. Explain why they're here through mundane circumstances, not destiny""",
    "constraint_based": """Create a character with these constraints:
- They must have worked an ordinary job (not warrior/mage/thief)
- They have an irrational fear of something common
- They ended up here by accident, not purpose
- Include one specific physical detail that's memorable but not dramatic
Build a coherent character from these constraints.""",
    "specificity_guide": """Create a character following these principles:
- Replace every vague word with something specific
  (not "warrior" but "third-shift security guard at the mall")
- Give them a problem that isn't dramatic
  (not "haunted past" but "owes three months rent")  
- Include exactly ONE memorable detail
  (not paragraphs of description, just one thing that sticks)
- Make them feel out of place here""",
    "object_anchor": """Create a character by:
1. Think of an object that costs less than $10
2. Decide why this character treasures it
3. Build their entire identity from this relationship
4. Make them specific and flawed
Don't mention the object directly in their name.""",
    "anti_fantasy": """Create a character who absolutely doesn't belong in a fantasy setting.
They should feel like they wandered in from real life.
No mystical backgrounds, no chosen one narratives, no dark secrets.
Just a specific person dealing with a weird situation.
Give them concerns that have nothing to do with adventure.""",
    "improv_method": """Create a character using improv techniques:
1. Start with a strong emotion (not epic - think everyday emotions)
2. Add a specific physical mannerism
3. Give them an immediate want (something small and achievable)
4. Ground them with a mundane fear or dislike
Build from these anchors naturally.""",
    "writer_method": """Create a character as a fiction writer would:
1. Start with their greatest mundane failure
2. Add a specific skill they're surprisingly good at
3. Give them a routine they can't break
4. Include one lie they tell themselves
Let these elements inform everything else about them.""",
}


async def generate_single_character(
    strategy_name: str, prompt_template: str, run_number: int
) -> Character:
    """Generate a single character with unique random seeds."""

    # Generate unique seeds for this character
    prompt = prompt_template.format(
        letters="".join(random.choices(string.ascii_lowercase, k=2)),
        number=random.randint(1, 999),
    )

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",  # Same as effects agent
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=prompt,
        output_type=Character,
    )

    print(f"  Starting run {run_number} for {strategy_name}...")
    result = await agent.run(f"Create character #{run_number}")
    print(f"  Completed run {run_number} for {strategy_name}")
    return result.output


async def test_prompt(
    strategy_name: str, prompt_template: str, runs: int = 3
) -> List[Character]:
    """Test a prompt strategy multiple times in parallel."""

    # Create all tasks at once - each will get unique random seeds
    tasks = [
        generate_single_character(strategy_name, prompt_template, i + 1)
        for i in range(runs)
    ]

    # Run them all in parallel
    characters = await asyncio.gather(*tasks)

    return characters


def analyze_characters(strategy_name: str, characters: List[Character]):
    """Analyze the variety in generated characters."""
    print(f"\n=== {strategy_name.upper()} ===")
    print(f"Generated {len(characters)} characters:")

    names = [c.name for c in characters]
    print(f"\nNames: {names}")

    # Check for variety
    unique_names = len(set(names))
    print(f"Unique names: {unique_names}/{len(names)}")

    # Show sample descriptions
    print("\nSample descriptions:")
    for i, char in enumerate(characters[:3], 1):
        print(f"\n{i}. {char.name}")
        print(f"   {char.description[:200]}...")

    # Look for patterns
    fantasy_words = [
        "mysterious",
        "ancient",
        "destiny",
        "chosen",
        "dark",
        "shadow",
        "power",
        "magical",
    ]
    fantasy_count = sum(
        1
        for c in characters
        if any(
            word in c.description.lower() or word in c.backstory.lower()
            for word in fantasy_words
        )
    )
    print(f"\nCharacters with fantasy tropes: {fantasy_count}/{len(characters)}")

    return {
        "unique_names": unique_names,
        "fantasy_tropes": fantasy_count,
        "characters": characters,
    }


async def main():
    """Test all strategies and compare results."""

    # Test each strategy
    strategies_to_test = [
        "baseline",
        "mundane_focus",
        "specificity_guide",
        "anti_fantasy",
    ]

    print("Starting parallel tests for all strategies...")

    # Run all strategies in parallel
    strategy_tasks = [
        test_prompt(strategy, PROMPT_STRATEGIES[strategy], runs=3)
        for strategy in strategies_to_test
    ]

    all_characters = await asyncio.gather(*strategy_tasks)

    # Analyze results
    results = {}
    for strategy, characters in zip(strategies_to_test, all_characters):
        results[strategy] = analyze_characters(strategy, characters)

    # Compare results
    print("\n\n=== COMPARISON ===")
    print(f"{'Strategy':<20} {'Unique Names':<15} {'Fantasy Tropes':<15}")
    print("-" * 50)
    for strategy, data in results.items():
        print(
            f"{strategy:<20} {data['unique_names']}/3 names{' ':<6} {data['fantasy_tropes']}/3 chars"
        )

    # Find best performing strategy
    best_variety = max(results.items(), key=lambda x: x[1]["unique_names"])
    least_tropey = min(results.items(), key=lambda x: x[1]["fantasy_tropes"])

    print(f"\nMost name variety: {best_variety[0]}")
    print(f"Least fantasy tropes: {least_tropey[0]}")


if __name__ == "__main__":
    asyncio.run(main())
