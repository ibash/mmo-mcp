"""Test seed-based character creation methods to ensure variety."""

import asyncio
import random
import string
from typing import List, Dict
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


def generate_random_seeds() -> Dict:
    """Generate random seeds for character creation."""
    return {
        "letters": "".join(random.choices(string.ascii_lowercase, k=2)),
        "number": random.randint(1, 999),
        "time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
        "color": random.choice(
            ["red", "blue", "green", "yellow", "purple", "orange", "brown", "gray"]
        ),
        "texture": random.choice(
            ["smooth", "rough", "sticky", "fuzzy", "cold", "wet", "brittle", "soft"]
        ),
        "price": random.randint(1, 20),
        "distance": random.randint(1, 500),
        "verb": random.choice(
            [
                "stumbled",
                "crawled",
                "fell",
                "wandered",
                "slipped",
                "backed",
                "rolled",
                "tumbled",
            ]
        ),
        "emotion": random.choice(
            [
                "annoyed",
                "confused",
                "bored",
                "anxious",
                "exhausted",
                "suspicious",
                "embarrassed",
                "hungry",
            ]
        ),
    }


# Different seed-based strategies to test
SEED_STRATEGIES = {
    "baseline_no_seeds": """Create a unique character for a multiplayer dungeon crawler game.
Be creative and avoid fantasy clichés like Zephyr, Shadow, Raven, Phoenix.
Focus on making them specific and memorable.""",
    "fixed_list_objects": """Create a character for a multiplayer dungeon crawler.
Your character must have ONE of these objects as important to them:
- bent spoon
- single shoe
- empty jar
- broken compass
- torn map

Build their entire identity around why this object matters to them.""",
    "letter_association": """Create a character using this method:
1. Start with the letters "{letters}" - think of a word beginning with these
2. Free associate from that word {number} times (each based on the previous)
3. Your character must be connected to your FINAL association
4. Don't mention the associations explicitly - just use them as inspiration

Example: "br" → bread → bakery → early morning → insomnia → counting sheep → wool
Result: An insomniac wool merchant

Start with "{letters}" and make {number} jumps.""",
    "generated_object": """Create a character following this method:
1. Think of a specific object that costs less than ${price}
2. This object is the ONLY thing they care about protecting
3. Build their entire identity around this object
4. Make the connection unusual but logical

Don't use generic objects - be extremely specific.""",
    "random_constraints": """Create a character with these exact constraints:
- They arrived here by: {verb} through a {texture} surface
- Their primary emotion right now: {emotion}
- They're exactly {distance} miles from where they should be
- The time {time} is significant to them somehow
- They associate everything with the color {color}

Make these random elements form a coherent character.""",
    "multi_seed_fusion": """Create a character by combining these seeds:
- Letters "{letters}" inspire their name (not literally, but through association)
- The number {number} appears in their life somehow
- They {verb} into this place while feeling {emotion}
- Something {texture} and {color} is important to them

Don't force all elements - pick 2-3 that work together naturally.""",
    "procedural_details": """Create a character by inventing specific details:
1. Think of a job that pays less than ${price}k per year
2. Think of something specific they're bad at (not generic like "social skills")
3. Think of a fear related to the texture "{texture}"
4. Give them a routine that happens at {time}

Build a character from these self-generated specifics.""",
    "anti_seed": """Create a character but you MUST avoid:
- Any name starting with "{letters}"
- The number {number}
- Anything {color} colored
- Any {texture} textures
- Anyone who {verb}

Work around these constraints to create someone unique.""",
    "improv_seed": """Using improv technique with seeds:
1. They entered feeling {emotion} (play this at maximum intensity)
2. They {verb} here (this is their physical memory of arrival)
3. Something about {time} drives their actions
4. The letters "{letters}" mean something to them (not their name)

Start with the emotion and build everything from there.""",
    "economy_seed": """Character economics:
1. They have exactly ${price} to their name
2. They traveled {distance} miles to get here
3. They lost something {color} and {texture}
4. This happened at {time}

Their entire motivation stems from these economic realities.""",
}


async def generate_character_with_seeds(
    strategy_name: str, prompt_template: str, run_number: int
) -> Character:
    """Generate a single character with unique random seeds."""

    # Generate unique seeds for this character
    seeds = generate_random_seeds()

    # Format the prompt with seeds
    prompt = prompt_template.format(**seeds)

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=prompt,
        output_type=Character,
    )

    print(
        f"  Run {run_number} for {strategy_name} (seeds: {seeds['letters']}, #{seeds['number']})"
    )
    result = await agent.run(f"Create character #{run_number}")
    return result.output


async def test_strategy(
    strategy_name: str, prompt_template: str, runs: int = 5
) -> List[Character]:
    """Test a strategy multiple times in parallel."""

    tasks = [
        generate_character_with_seeds(strategy_name, prompt_template, i + 1)
        for i in range(runs)
    ]

    characters = await asyncio.gather(*tasks)
    return characters


def analyze_variety(strategy_name: str, characters: List[Character]) -> Dict:
    """Analyze the variety in generated characters."""

    names = [c.name for c in characters]
    unique_names = len(set(names))

    # Check for common fantasy tropes
    fantasy_words = [
        "mysterious",
        "ancient",
        "destiny",
        "chosen",
        "shadow",
        "power",
        "magical",
        "dark",
        "whisper",
        "storm",
        "phoenix",
        "raven",
    ]
    fantasy_count = sum(
        1
        for c in characters
        if any(
            word in c.name.lower() or word in c.description.lower()
            for word in fantasy_words
        )
    )

    # Check for repeated words across descriptions (indicates patterns)
    all_descriptions = " ".join([c.description for c in characters])
    word_freq = {}
    for word in all_descriptions.lower().split():
        if len(word) > 4:  # Only count substantial words
            word_freq[word] = word_freq.get(word, 0) + 1

    # Find words that appear in multiple character descriptions
    repeated_words = [word for word, count in word_freq.items() if count >= 3]

    # Calculate diversity score
    diversity_score = unique_names * 10
    diversity_score -= fantasy_count * 5
    diversity_score -= len(repeated_words) * 2

    return {
        "unique_names": unique_names,
        "fantasy_tropes": fantasy_count,
        "repeated_words": repeated_words[:5],  # Top 5 repeated words
        "diversity_score": diversity_score,
        "characters": characters,
    }


async def main():
    """Test all strategies and compare results."""

    print("Testing seed-based character generation strategies...\n")

    # Strategies to test
    strategies = [
        "baseline_no_seeds",
        "fixed_list_objects",
        "letter_association",
        "generated_object",
        "random_constraints",
        "multi_seed_fusion",
        "procedural_details",
        "improv_seed",
    ]

    # Run tests in parallel
    print("Running all strategies in parallel (5 characters each)...\n")

    strategy_tasks = [
        test_strategy(strategy, SEED_STRATEGIES[strategy], runs=5)
        for strategy in strategies
    ]

    all_results = await asyncio.gather(*strategy_tasks)

    # Analyze results
    results = {}
    for strategy, characters in zip(strategies, all_results):
        results[strategy] = analyze_variety(strategy, characters)

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    for strategy, data in results.items():
        print(f"\n### {strategy.upper()} ###")
        print(f"Unique names: {data['unique_names']}/5")
        print(f"Fantasy tropes: {data['fantasy_tropes']}/5")
        print(f"Repeated words: {data['repeated_words']}")
        print(f"Diversity score: {data['diversity_score']}")

        # Show sample names
        print(f"Names: {[c.name for c in data['characters']]}")

        # Show one sample description
        if data["characters"]:
            print(f"Sample: {data['characters'][0].description[:150]}...")

    # Find best performers
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)

    sorted_by_diversity = sorted(
        results.items(), key=lambda x: x[1]["diversity_score"], reverse=True
    )

    print(f"\n{'Strategy':<25} {'Score':<10} {'Unique':<10} {'Tropes':<10}")
    print("-" * 55)
    for strategy, data in sorted_by_diversity:
        print(
            f"{strategy:<25} {data['diversity_score']:<10} {data['unique_names']}/5{'':<6} {data['fantasy_tropes']}/5"
        )

    print(f"\nBest performer: {sorted_by_diversity[0][0]}")
    print(f"Worst performer: {sorted_by_diversity[-1][0]}")


if __name__ == "__main__":
    asyncio.run(main())
