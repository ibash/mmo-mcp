"""Test if multi-stage approach works when embedded in a single prompt."""

import asyncio
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


async def create_character_with_prompt(prompt: str) -> Character:
    """Create a single character with given prompt."""
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


async def test_approach(name: str, prompt: str, count: int = 5) -> List[Character]:
    """Test an approach by generating multiple characters."""
    print(f"Testing {name}...")
    tasks = [create_character_with_prompt(prompt) for _ in range(count)]
    characters = await asyncio.gather(*tasks)
    return characters


async def evaluate_characters(
    approach_name: str, characters: List[Character]
) -> CharacterEvaluation:
    """Evaluate character diversity and quality."""

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


# Different prompt strategies
PROMPTS = {
    "baseline": """Create a unique character for a multiplayer dungeon crawler game.
Be creative and avoid clichés.""",
    "single_prompt_multistage": """Create a character using this EXACT mental process:

STEP 1: First, mentally generate 20 completely different one-sentence character concepts.
Think of wildly different: professions, ages, problems, backgrounds, personalities.

STEP 2: From those 20, select the ONE that would be MOST different from typical fantasy characters.
Pick something unexpected, specific, grounded in reality.

STEP 3: Expand that concept into a full character with:
- A realistic name (not fantasy)
- Specific, concrete details
- Memorable quirks from real life
- Clear motivations that aren't epic/mystical

Follow these steps internally, then output the final character.""",
    "explicit_diversity": """Before creating this character, think about what everyone else creates:
- They create mysterious warriors with dark pasts
- They create wise mages with ancient knowledge  
- They create rogues with hearts of gold
- They use names like Shadow, Storm, Raven

Now create a character that is NOTHING like those.
Someone specific, mundane, real. With actual problems, not epic quests.""",
    "negative_space": """Create a character by first deciding what they're NOT:
- NOT trained in combat
- NOT mystically gifted
- NOT on a quest
- NOT tragic or mysterious
- NOT named something fantasy-like

Build a specific, memorable character from these constraints.""",
    "random_seed_internal": """Create a character by:
1. Pick a random two-letter combination in your mind
2. Think of a mundane word starting with those letters
3. Free-associate 5 times from that word
4. Build a character connected to your final association

Make them specific and real, not generic.""",
    "forced_mundane": """You're creating a character who was living a completely normal life until 5 minutes ago.

Pick a SPECIFIC person:
- Exact job title (not "merchant" but "night shift convenience store clerk")
- Exact location (not "a village" but "Apartment 4B on Maple Street")  
- Exact problem they're dealing with (not "dark past" but "car payment is due Tuesday")
- Exact thing in their pocket (not "mysterious amulet" but "expired gym membership card")

Make them memorable through specificity.""",
    "anti_ai_patterns": """Most AIs create characters that are:
- Middle-aged and weathered
- Carrying mysterious objects
- Having tragic backstories
- Named with fantasy words
- Described as "meticulous" or "grizzled"

Create someone who breaks ALL these patterns.
Young or old, specific modern problems, normal names, different adjectives.""",
    "structured_diversity": """Create a character by rolling mental dice for each attribute:

AGE: Pick from [17-25, 26-40, 41-55, 56-70, 70+]
PROBLEM: Pick from [physical, social, financial, technological, existential]
BACKGROUND: Pick from [rural, suburban, urban, academic, transient]
TRAIT: Pick from [anxious, optimistic, obsessive, forgetful, argumentative]

Don't pick the "middle" option. Pick something extreme.
Build a specific character from these random choices.""",
    "iterative_refinement": """Create a character through refinement:

1. Start with the most generic character possible (mysterious warrior)
2. Change ONE thing to make them specific (mysterious warranty claims adjuster)
3. Change ANOTHER thing (elderly warranty claims adjuster)
4. Add a specific detail (elderly warranty claims adjuster who collects bottle caps)
5. Add a real problem (elderly warranty claims adjuster who can't find his reading glasses)

Output only the final, refined version.""",
    "documentary_style": """Imagine you're a documentary filmmaker who just found this person.
They're not a hero. They're just someone who ended up here.

Describe them like a documentary subject:
- Their actual name and occupation
- What they were doing when you found them
- Their immediate concerns
- The mundane objects they have with them

No fantasy elements. Just a real person in a weird situation.""",
}


async def main():
    """Test different prompt strategies."""

    print("Testing Single-Prompt Character Generation Strategies")
    print("=" * 80)

    results = {}

    # Test all approaches in parallel
    print("\nRunning all approaches in parallel...")

    async def test_and_evaluate(name: str, prompt: str):
        try:
            characters = await test_approach(name, prompt, count=5)
            evaluation = await evaluate_characters(name, characters)
            print(f"Completed {name}")
            return name, {"characters": characters, "evaluation": evaluation}
        except Exception as e:
            print(f"Error in {name}: {e}")
            return name, None

    tasks = [test_and_evaluate(name, prompt) for name, prompt in PROMPTS.items()]
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
        print(f"Summary: {eval.summary}")

        # Show character names
        names = [c.name for c in data["characters"]]
        print(f"Characters: {names}")

    # Ranking
    print("\n" + "=" * 80)
    print("FINAL RANKING")
    print("=" * 80)

    sorted_results = sorted(
        results.items(), key=lambda x: x[1]["evaluation"].overall_score, reverse=True
    )

    print(f"\n{'Rank':<6} {'Strategy':<30} {'Score':<8} {'Diversity':<10}")
    print("-" * 60)

    for i, (strategy, data) in enumerate(sorted_results, 1):
        eval = data["evaluation"]
        print(
            f"{i:<6} {strategy:<30} {eval.overall_score:<8} {eval.diversity_score:<10}"
        )

    # Winner
    winner = sorted_results[0]
    print(f"\n🏆 WINNER: {winner[0]}")
    print(f"Score: {winner[1]['evaluation'].overall_score}/100")
    print("\nWinning prompt:")
    print(PROMPTS[winner[0]][:500] + "...")


if __name__ == "__main__":
    asyncio.run(main())
