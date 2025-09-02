"""Test more character creation approaches focusing on guidance rather than seeds."""

import asyncio
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


# Test different guidance approaches
GUIDANCE_STRATEGIES = {
    "simple_specific": """Create a character for a multiplayer dungeon crawler.
Make them specific rather than generic. Use concrete details.
Avoid fantasy clichés.""",
    "anti_trope_list": """Create a character for a multiplayer dungeon crawler.

NEVER use these cliché elements:
- Mysterious past, dark secret, haunted by memories
- Chosen one, prophecy, destiny, ancient bloodline  
- Lone wolf, last of their kind, seeking revenge
- Names like: Shadow, Storm, Raven, Phoenix, Blade, Whisper

Instead focus on ordinary people in extraordinary circumstances.""",
    "question_based": """Create a character by answering these:
1. What mundane job did they have last week?
2. What everyday item are they weirdly protective of?
3. What normal thing scares them?
4. Why are they here (wrong place/time, not destiny)?

Build a coherent character from these answers.""",
    "one_rule": """Create a character following only this rule:
Every single detail must be something you could find in a modern suburb.
No fantasy elements. Make them interesting through specificity.""",
    "contradiction_method": """Create a character built on ONE interesting contradiction:
Examples: Huge but timid, educated but superstitious, organized but always lost.
Pick your own contradiction and build everything from it.""",
    "mundane_dramatic": """Create a character whose biggest problem is completely mundane.
Examples: Lost their keys, late for appointment, forgot someone's name.
This mundane problem defines who they are.""",
    "specific_vague": """Create a character using this principle:
Be EXTREMELY specific about trivial things.
Be vague about important things.
Example: Know exact shoe size but unsure of their age.""",
    "real_person_displaced": """Create a character as if you're describing someone from a real office/shop/school
who suddenly found themselves here. Include:
- Their actual job title
- A specific complaint they have
- What they miss most from normal life""",
    "no_guidance": """Create a character for a multiplayer dungeon crawler.""",
    "single_anchor": """Create a character starting from ONE specific detail:
Pick something worth less than $20 that they own.
Everything else about them stems from this one object.
Don't make it magical or significant - just theirs.""",
    "routine_disrupted": """Create a character whose daily routine was interrupted:
- What were they doing when they ended up here?
- What time was it supposed to happen?
- Who's waiting for them?
Build from this disruption.""",
    "memory_gap": """Create a character who clearly remembers everything EXCEPT how they got here.
They know their job, their debts, their dentist appointment next Tuesday.
But the last 10 minutes? Complete blank.
Build from this specific confusion.""",
    "wrong_gear": """Create a character dressed/equipped for something completely different.
Examples: Wedding attire, scuba gear, fast food uniform.
They're stuck with what they were wearing when they arrived.
Build identity from this mismatch.""",
    "overqualified": """Create a character hilariously overqualified for adventure.
They have a PhD in something useless here.
They speak 4 languages, none helpful.
They're an expert in something completely irrelevant.
Make them detailed and real.""",
    "list_avoidance": """Create a character while avoiding ALL of these:
- Any form of combat training
- Any mystical/magical background
- Any tragic backstory
- Any special destiny
- Any unusual abilities
Make them interesting anyway.""",
    "interview_style": """You're interviewing someone who stumbled in here by accident.
They're confused but trying to be helpful.
Ask them:
- Name and occupation?
- What's in your pockets?
- Last thing you remember?
Create character from their answers.""",
    "negative_space": """Define your character by what they're NOT:
- Not brave (but here anyway)
- Not special (completely average)
- Not prepared (wrong everything)
- Not chosen (total accident)
Build interest from these limitations.""",
    "specific_numbers": """Your character is defined by specific numbers:
- Exactly how much money they have ($X.XX)
- Exactly how many days since something happened
- Exactly what time they need to be somewhere
- Exactly how many of something they own
Make the numbers mundane but specific.""",
    "borrowed_thing": """Your character has something that isn't theirs:
- What is it?
- Who does it belong to?
- Why can't they return it?
- How does this complicate everything?
Build from this borrowed item.""",
    "sensory_specific": """Describe your character through specific sensory details:
- They smell like [specific thing]
- They sound like [specific noise when moving]
- They feel [specific texture] to touch
- They taste [specific thing] constantly
Make it mundane but memorable.""",
}


async def generate_character(
    strategy_name: str, prompt: str, run_number: int
) -> Character:
    """Generate a single character."""

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=prompt,
        output_type=Character,
    )

    result = await agent.run(f"Create character #{run_number}")
    return result.output


async def test_strategy(
    strategy_name: str, prompt: str, runs: int = 5
) -> List[Character]:
    """Test a strategy multiple times in parallel."""

    print(f"Testing {strategy_name}...")

    tasks = [generate_character(strategy_name, prompt, i + 1) for i in range(runs)]

    characters = await asyncio.gather(*tasks)
    return characters


def calculate_diversity(characters: List[Character]) -> Dict:
    """Calculate diversity metrics for a set of characters."""

    names = [c.name for c in characters]
    names_lower = [n.lower() for n in names]

    # 1. Name uniqueness (all different = good)
    unique_names = len(set(names_lower))
    name_similarity = 0
    for i, n1 in enumerate(names_lower):
        for n2 in names_lower[i + 1 :]:
            # Check if names share words
            words1 = set(n1.split())
            words2 = set(n2.split())
            if words1 & words2:  # Intersection
                name_similarity += 1

    # 2. Cliché detection
    cliche_name_patterns = [
        "shadow",
        "storm",
        "raven",
        "blade",
        "whisper",
        "dark",
        "moon",
        "star",
        "wolf",
        "phoenix",
        "frost",
        "ember",
        "thorn",
        "mystic",
        "zephyr",
    ]
    cliche_names = sum(
        1
        for name in names_lower
        if any(pattern in name for pattern in cliche_name_patterns)
    )

    # 3. Description analysis
    descriptions = [c.description.lower() for c in characters]

    # Fantasy/generic tropes (bad)
    fantasy_patterns = [
        "mysterious",
        "ancient",
        "prophecy",
        "chosen",
        "destiny",
        "dark past",
        "lone wolf",
        "last of",
        "seeking revenge",
        "haunted by",
        "sworn to",
        "magical",
        "mystical",
        "ethereal",
        "otherworldly",
        "legendary",
        "mythical",
    ]
    fantasy_count = sum(
        1
        for desc in descriptions
        if any(pattern in desc for pattern in fantasy_patterns)
    )

    # Specific mundane details (good)
    specific_patterns = [
        "$",
        "dollars",
        "cents",
        "brand",
        "model",
        "size",
        "color",
        "flavor",
        "street",
        "avenue",
        "apartment",
        "suite",
        "floor",
        "room",
    ]
    specific_count = sum(
        1
        for desc in descriptions
        if any(pattern in desc for pattern in specific_patterns)
    )

    # 4. Check for repeated concepts across characters
    all_descriptions = " ".join(descriptions)

    # Common professions that get overused
    profession_patterns = [
        "guard",
        "merchant",
        "accountant",
        "clerk",
        "baker",
        "farmer",
    ]
    profession_repeats = sum(
        all_descriptions.count(prof) for prof in profession_patterns
    ) - len(characters)  # Subtract expected count

    # 5. Measure true diversity - are the characters actually different from each other?
    character_concepts = []
    for c in characters:
        # Extract core concept words (nouns, verbs)
        words = c.description.lower().split()
        core_words = [
            w
            for w in words
            if len(w) > 5
            and w
            not in ["their", "these", "those", "where", "which", "while", "though"]
        ]
        character_concepts.append(set(core_words))

    # How much overlap in concepts?
    concept_overlap = 0
    for i, concepts1 in enumerate(character_concepts):
        for concepts2 in character_concepts[i + 1 :]:
            overlap = len(concepts1 & concepts2)
            concept_overlap += overlap

    # 6. Calculate final score
    score = 0
    score += unique_names * 20
    score -= name_similarity * 15  # Penalize similar names
    score -= cliche_names * 10
    score -= fantasy_count * 8
    score += specific_count * 5
    score -= profession_repeats * 3
    score -= concept_overlap * 2  # Penalize conceptual overlap

    # Bonus for perfect uniqueness
    if unique_names == 5 and name_similarity == 0:
        score += 25

    return {
        "unique_names": unique_names,
        "name_similarity": name_similarity,
        "cliche_names": cliche_names,
        "fantasy_tropes": fantasy_count,
        "specific_details": specific_count,
        "concept_overlap": concept_overlap,
        "score": score,
        "names": names,
    }


async def main():
    """Test all strategies."""

    print("Testing character creation guidance strategies...\n")
    print("=" * 80)

    # Select strategies to test
    strategies_to_test = [
        "no_guidance",
        "simple_specific",
        "one_rule",
        "real_person_displaced",
        "wrong_gear",
        "borrowed_thing",
    ]

    # Run ALL strategies in parallel
    print("Running all strategies in parallel...")
    strategy_tasks = [
        test_strategy(strategy, GUIDANCE_STRATEGIES[strategy], runs=5)
        for strategy in strategies_to_test
    ]

    all_characters = await asyncio.gather(*strategy_tasks)

    # Analyze results
    results = {}
    for strategy, characters in zip(strategies_to_test, all_characters):
        results[strategy] = calculate_diversity(characters)
        results[strategy]["characters"] = characters

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS BY STRATEGY")
    print("=" * 80)

    for strategy, metrics in results.items():
        print(f"\n### {strategy.upper()} ###")
        print(f"Score: {metrics['score']}")
        print(
            f"Unique names: {metrics['unique_names']}/5 (similarity: {metrics['name_similarity']})"
        )
        print(f"Cliché names: {metrics['cliche_names']}/5")
        print(f"Fantasy tropes: {metrics['fantasy_tropes']}/5")
        print(f"Specific details: {metrics['specific_details']}/5")
        print(f"Concept overlap: {metrics['concept_overlap']}")
        print(f"Names: {metrics['names']}")

        # Show sample description
        if metrics.get("characters"):
            sample = metrics["characters"][0].description[:200]
            print(f"Sample: {sample}...")

    # Ranking
    print("\n" + "=" * 80)
    print("FINAL RANKING")
    print("=" * 80)

    sorted_results = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)

    print(
        f"\n{'Rank':<6} {'Strategy':<25} {'Score':<8} {'Fantasy':<10} {'Specific':<10}"
    )
    print("-" * 65)

    for i, (strategy, metrics) in enumerate(sorted_results, 1):
        print(
            f"{i:<6} {strategy:<25} {metrics['score']:<8} {metrics['fantasy_tropes']}/5{'':<6} {metrics['specific_details']}/5"
        )

    # Show winner details
    winner = sorted_results[0]
    print(f"\n🏆 WINNER: {winner[0]}")
    print(f"Score: {winner[1]['score']}")
    print("\nSample characters:")
    for i, char in enumerate(winner[1]["characters"][:3], 1):
        print(f"\n{i}. {char.name}")
        print(f"   {char.description}")


if __name__ == "__main__":
    asyncio.run(main())
