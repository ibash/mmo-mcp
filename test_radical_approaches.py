"""Test radical new approaches for character generation."""

import asyncio
import random
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


class CharacterConcept(BaseModel):
    """A single-sentence character concept."""

    concept: str = Field(description="One sentence character concept")
    uniqueness_score: int = Field(description="How unique is this concept? 1-10")


class ConceptBatch(BaseModel):
    """A batch of character concepts."""

    concepts: List[CharacterConcept] = Field(
        description="List of 20 different character concepts"
    )


class SelectedConcepts(BaseModel):
    """Selected most diverse concepts."""

    selected: List[str] = Field(description="The 5 most different concepts")
    reasoning: str = Field(
        description="Why these 5 are the most different from each other"
    )


class CharacterEvaluation(BaseModel):
    """Evaluation of a set of characters."""

    diversity_score: int = Field(
        description="Score 1-100 for how different the characters are from each other"
    )
    cliche_score: int = Field(
        description="Score 1-100 where 100 means very cliché/generic, 1 means unique"
    )
    specificity_score: int = Field(
        description="Score 1-100 for how specific vs vague the details are"
    )
    memorability_score: int = Field(
        description="Score 1-100 for how memorable/distinctive the characters are"
    )
    overall_score: int = Field(description="Overall score 1-100")
    summary: str = Field(description="2-3 sentence summary of strengths and weaknesses")


def generate_random_seeds():
    """Generate truly random seeds for character creation."""

    # Random "Wikipedia articles" (simulated)
    wikipedia_titles = [
        "History of the Potato Chip",
        "Lighthouse of Alexandria",
        "1904 St. Louis World's Fair",
        "Typewriter Repair Manual",
        "Antarctic Research Station McMurdo",
        "Chess Boxing",
        "Library of Ashurbanipal",
        "Velcro Manufacturing Process",
        "Pigeon Racing",
        "Dewey Decimal System",
        "Subway Map Design",
        "Beekeeping in Slovenia",
        "Morse Code Operators Union",
        "Elevator Music Industry",
        "Parallel Parking",
        "Dust Bowl Migration",
        "Stamp Collecting",
        "Air Traffic Control",
        "Vending Machine History",
        "Public Library Late Fees",
        "Laundromat Economics",
        "Crossword Puzzle Construction",
        "Television Test Pattern",
        "Phone Book Publishing",
        "Mall Security",
        "DMV Operations",
        "Parking Meter Design",
        "Bus Route Planning",
    ]

    # Random real names from different cultures
    first_names = [
        "Dmitri",
        "Yuki",
        "Fatima",
        "Lars",
        "Priya",
        "Santiago",
        "Ingrid",
        "Chen",
        "Kwame",
        "Astrid",
        "Omar",
        "Helga",
        "Raj",
        "Svetlana",
        "Miguel",
        "Ling",
        "Jamal",
        "Brigitte",
        "Tariq",
        "Greta",
        "Pavel",
        "Amara",
        "Klaus",
        "Nalini",
    ]

    last_names = [
        "Petrov",
        "Tanaka",
        "Al-Rashid",
        "Andersson",
        "Patel",
        "Rodriguez",
        "Berg",
        "Wu",
        "Okonkwo",
        "Nielsen",
        "Hassan",
        "Schmidt",
        "Singh",
        "Volkov",
        "Garcia",
        "Zhang",
        "Williams",
        "Larsson",
        "Ibrahim",
        "Müller",
        "Kowalski",
        "Dubois",
    ]

    # Random specific items under $10
    cheap_items = [
        "rubber band ball",
        "expired bus pass",
        "single shoelace",
        "hotel pen",
        "fortune from cookie",
        "arcade token",
        "library card from 1987",
        "bent paperclip",
        "grocery list",
        "parking stub",
        "chewed pencil",
        "foreign coin",
        "bottle cap",
        "twist tie",
        "promotional fridge magnet",
        "dead AA battery",
        "pocket lint",
        "crumpled receipt",
        "broken rubber band",
        "sticky note",
        "paper clip chain",
    ]

    # Random specific times
    times = [f"{h:02d}:{m:02d}" for h in range(24) for m in [0, 15, 30, 45]]

    # Random specific numbers
    numbers = [random.randint(1, 999) for _ in range(20)]

    # Random actions/states
    actions = [
        "waiting for",
        "arguing about",
        "measuring",
        "organizing",
        "avoiding",
        "counting",
        "searching for",
        "complaining about",
        "fixing",
        "documenting",
    ]

    return {
        "wikipedia": random.sample(wikipedia_titles, 5),
        "names": [
            (random.choice(first_names), random.choice(last_names)) for _ in range(5)
        ],
        "items": random.sample(cheap_items, 5),
        "times": random.sample(times, 5),
        "numbers": random.sample(numbers, 5),
        "actions": random.sample(actions, 5),
    }


async def force_randomness_approach() -> List[Character]:
    """Generate characters using forced random elements."""

    seeds = generate_random_seeds()

    async def create_random_character(i: int) -> Character:
        first_name, last_name = seeds["names"][i]
        wikipedia = seeds["wikipedia"][i]
        item = seeds["items"][i]
        time = seeds["times"][i]
        number = seeds["numbers"][i]
        action = seeds["actions"][i]

        prompt = f"""Create a character with these EXACT specifications:

NAME: Must be exactly "{first_name} {last_name}"

REQUIRED ELEMENTS:
- Their profession or background must relate to: {wikipedia}
- They are carrying exactly this item: {item}
- The time {time} is important to them
- The number {number} appears in their life
- They were {action} something when they arrived here

BUILD a coherent character from these random elements. Make the connections logical even if unusual.
The character should feel like a real person despite the random constraints."""

        agent = Agent(
            AnthropicModel(
                "claude-3-7-sonnet-latest",
                provider=AnthropicProvider(api_key=settings.anthropic_api_key),
            ),
            system_prompt=prompt,
            output_type=Character,
        )

        result = await agent.run("Create the character")
        return result.output

    # Create all 5 characters in parallel
    tasks = [create_random_character(i) for i in range(5)]
    characters = await asyncio.gather(*tasks)

    return characters


async def multi_stage_generation() -> List[Character]:
    """Generate characters using multi-stage refinement."""

    # Stage 1: Generate 20 concepts
    concept_prompt = """Generate 20 COMPLETELY DIFFERENT one-sentence character concepts.
Each must be wildly different from the others in:
- Profession/background
- Personality type  
- Age/generation
- Cultural background
- Core problem/concern

Make them specific and unusual. No generic fantasy archetypes."""

    agent1 = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=concept_prompt,
        output_type=ConceptBatch,
    )

    print("Stage 1: Generating 20 concepts...")
    concepts_result = await agent1.run("Generate the concepts")
    concepts = concepts_result.output

    # Stage 2: Select the 5 most different
    selection_prompt = f"""From these concepts, select the 5 that are MOST DIFFERENT from each other:

{chr(10).join([f"{i + 1}. {c.concept}" for i, c in enumerate(concepts.concepts)])}

Choose the 5 that share the LEAST in common. Maximum diversity."""

    agent2 = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt="You are selecting the most diverse character concepts.",
        output_type=SelectedConcepts,
    )

    print("Stage 2: Selecting 5 most diverse...")
    selected_result = await agent2.run(selection_prompt)
    selected = selected_result.output

    # Stage 3: Expand the selected concepts IN PARALLEL
    print("Stage 3: Expanding selected concepts...")

    async def expand_concept(concept: str) -> Character:
        expand_prompt = f"""Expand this concept into a full character:

CONCEPT: {concept}

Create a specific, memorable character with:
- A distinctive name (not generic fantasy)
- Concrete physical details
- Specific items/possessions
- Clear motivations
- Memorable quirks

Make them feel real and three-dimensional."""

        agent = Agent(
            AnthropicModel(
                "claude-3-7-sonnet-latest",
                provider=AnthropicProvider(api_key=settings.anthropic_api_key),
            ),
            system_prompt=expand_prompt,
            output_type=Character,
        )

        result = await agent.run("Expand the concept")
        return result.output

    # Expand all selected concepts in parallel
    expansion_tasks = [expand_concept(concept) for concept in selected.selected]
    characters = await asyncio.gather(*expansion_tasks)

    return characters


async def wikipedia_approach() -> List[Character]:
    """Generate characters inspired by random Wikipedia articles."""

    # Simulate random Wikipedia articles with diverse topics
    articles = [
        (
            "Ballpoint Pen Manufacturing",
            "The modern ballpoint pen relies on a tiny ball bearing and gravity-fed ink",
        ),
        (
            "Ghost Towns of Nevada",
            "Rhyolite was once a gold mining town with 10,000 residents, now completely abandoned",
        ),
        (
            "Refrigerator Organization",
            "The crisper drawer maintains 95% humidity for leafy vegetables",
        ),
        (
            "Subway Tile Installation",
            "Traditional subway tiles are exactly 3 inches by 6 inches",
        ),
        (
            "Library Fine Collection",
            "The largest library fine ever paid was $345,000 in Chicago",
        ),
    ]

    characters = []

    for title, fact in articles:
        prompt = f"""Create a character inspired by this random Wikipedia article:

ARTICLE: {title}
FACT: {fact}

The character should:
- Have a connection to this topic (profession, obsession, memory, etc.)
- Include the specific detail from the fact somehow
- Be a normal person, not a fantasy archetype
- Have a reason for being in a dungeon that relates to their background

Make them specific and real, not generic."""

        agent = Agent(
            AnthropicModel(
                "claude-3-7-sonnet-latest",
                provider=AnthropicProvider(api_key=settings.anthropic_api_key),
            ),
            system_prompt=prompt,
            output_type=Character,
        )

        result = await agent.run("Create the character")
        characters.append(result.output)

    return characters


async def constraint_cascade() -> List[Character]:
    """Each character must be different from all previous ones."""

    characters = []
    constraints = []

    for i in range(5):
        if i == 0:
            prompt = "Create a character for a multiplayer dungeon crawler. Be specific and avoid clichés."
        else:
            previous_summary = "\n".join(
                [
                    f"Character {j + 1}: {c.name} - {c.description[:100]}..."
                    for j, c in enumerate(characters)
                ]
            )

            prompt = f"""Create a character that is COMPLETELY DIFFERENT from these existing characters:

{previous_summary}

Your character must:
- Use a different naming convention
- Have a different type of problem/concern
- Come from a different background/era/culture
- Have different physical characteristics
- Speak/act differently

Make them as different as possible while still being specific and real."""

        agent = Agent(
            AnthropicModel(
                "claude-3-7-sonnet-latest",
                provider=AnthropicProvider(api_key=settings.anthropic_api_key),
            ),
            system_prompt=prompt,
            output_type=Character,
        )

        result = await agent.run("Create the character")
        characters.append(result.output)

    return characters


async def evaluate_characters(
    approach_name: str, characters: List[Character]
) -> CharacterEvaluation:
    """Use an LLM to evaluate character quality and diversity."""

    character_text = "\n\n".join([f"**{c.name}**\n{c.description}" for c in characters])

    evaluation_prompt = f"""Evaluate these 5 characters from approach: {approach_name}

CHARACTERS:
{character_text}

Evaluate on:
1. Diversity (how different from each other?)
2. Clichés (generic fantasy or unique?)
3. Specificity (vague or concrete details?)
4. Memorability (would players remember them?)

Be extremely harsh. Most attempts score 30-50. Only truly exceptional sets should score above 70."""

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt="You are an extremely harsh critic. Most character sets are mediocre.",
        output_type=CharacterEvaluation,
    )

    result = await agent.run(evaluation_prompt)
    return result.output


async def main():
    """Test radical new approaches."""

    print("Testing Radical Character Generation Approaches")
    print("=" * 80)

    approaches = [
        ("Force Randomness", force_randomness_approach),
        ("Multi-Stage Generation", multi_stage_generation),
        ("Wikipedia Inspiration", wikipedia_approach),
        ("Constraint Cascade", constraint_cascade),
    ]

    # Run all approaches in parallel
    print("\nRunning all approaches in parallel...")

    async def test_approach(name: str, func):
        try:
            print(f"Starting {name}...")
            characters = await func()
            evaluation = await evaluate_characters(name, characters)
            print(f"Completed {name}")
            return name, {"characters": characters, "evaluation": evaluation}
        except Exception as e:
            print(f"Error in {name}: {e}")
            return name, None

    tasks = [test_approach(name, func) for name, func in approaches]
    results_list = await asyncio.gather(*tasks)

    results = {name: data for name, data in results_list if data is not None}

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    for approach, data in results.items():
        eval = data["evaluation"]
        print(f"\n### {approach.upper()} ###")
        print(f"Overall Score: {eval.overall_score}/100")
        print(f"Diversity: {eval.diversity_score}/100")
        print(f"Clichés: {eval.cliche_score}/100 (lower is better)")
        print(f"Specificity: {eval.specificity_score}/100")
        print(f"Memorability: {eval.memorability_score}/100")
        print(f"Summary: {eval.summary}")

        # Show characters
        print("\nCharacters:")
        for c in data["characters"]:
            print(f"- {c.name}: {c.description[:100]}...")

    # Find winner
    if results:
        winner = max(results.items(), key=lambda x: x[1]["evaluation"].overall_score)
        print("\n" + "=" * 80)
        print(f"🏆 WINNER: {winner[0]}")
        print(f"Score: {winner[1]['evaluation'].overall_score}/100")
        print("\nFull character list:")
        for i, char in enumerate(winner[1]["characters"], 1):
            print(f"\n{i}. {char.name}")
            print(f"   {char.description}")


if __name__ == "__main__":
    asyncio.run(main())
