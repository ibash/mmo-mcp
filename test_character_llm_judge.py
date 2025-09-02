"""Test character creation with LLM-based evaluation."""

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
    best_character: str = Field(description="Name of the best character")
    worst_character: str = Field(description="Name of the worst character")
    summary: str = Field(description="2-3 sentence summary of strengths and weaknesses")


# Strategies to test
STRATEGIES = {
    "baseline": """Create a character for a multiplayer dungeon crawler game.""",
    "avoid_generic": """Create a character for a multiplayer dungeon crawler.
Avoid generic fantasy tropes. Be specific and memorable.""",
    "mundane_life": """Create a character who had a completely mundane life until 5 minutes ago.
Include their actual job, what's in their pockets, and what they're worried about missing.""",
    "one_detail": """Create a character by starting with ONE very specific detail 
(like "allergic to wool" or "always carries 37 cents").
Build everything else from that single detail.""",
    "no_fantasy": """Create a character with ZERO fantasy elements.
They're from modern Earth, dressed normally, with normal problems.
Make them interesting through specificity alone.""",
    "contradiction": """Create a character defined by ONE core contradiction.
Examples: terrifying appearance but gentle, highly educated but superstitious.
Pick your own and commit to it.""",
    "interrupted": """Create a character who was in the middle of something specific when they arrived.
What were they doing? What time was it? Who's waiting for them?""",
    "memory_palace": """Create a character who remembers three specific things:
1. The exact price of their last purchase
2. A phone number they need to call
3. Something they were supposed to pick up
Build from these mundane memories.""",
    "physical_state": """Create a character defined by their current physical state:
Are they hungry? Tired? Need the bathroom? Have a headache?
Start with the body, then build the person.""",
    "wrong_place": """Create a character dressed for a completely different occasion.
Wedding? Job interview? Beach day? Gym?
They're stuck in whatever they were wearing.""",
}


async def generate_character(strategy: str, prompt: str) -> Character:
    """Generate a single character."""
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


async def generate_character_set(
    strategy_name: str, prompt: str, count: int = 5
) -> List[Character]:
    """Generate multiple characters in parallel."""
    print(f"Generating {count} characters for {strategy_name}...")

    tasks = [generate_character(strategy_name, prompt) for _ in range(count)]
    characters = await asyncio.gather(*tasks)
    return characters


async def evaluate_characters(
    strategy_name: str, characters: List[Character]
) -> CharacterEvaluation:
    """Use an LLM to evaluate character quality and diversity."""

    # Format characters for evaluation
    character_text = "\n\n".join([f"**{c.name}**\n{c.description}" for c in characters])

    evaluation_prompt = f"""You are evaluating {len(characters)} characters for a multiplayer game.
    
CHARACTERS:
{character_text}

Evaluate these characters on:
1. Diversity (how different are they from each other?)
2. Clichés (are they generic fantasy tropes or unique?)
3. Specificity (vague generalities or concrete details?)
4. Memorability (would players remember them?)

Be harsh but fair. Most fantasy characters are cliché - only give good scores if they truly avoid tropes."""

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt="You are a harsh but fair critic of character creation.",
        output_type=CharacterEvaluation,
    )

    result = await agent.run(evaluation_prompt)
    return result.output


async def main():
    """Test all strategies."""

    print("Testing character generation strategies with LLM evaluation\n")
    print("=" * 80)

    # Test strategies in parallel
    all_results = {}

    # Generate characters for all strategies
    print("\nGenerating characters...")
    strategy_tasks = [
        generate_character_set(name, prompt, count=5)
        for name, prompt in STRATEGIES.items()
    ]

    all_characters = await asyncio.gather(*strategy_tasks)

    # Evaluate all character sets
    print("\nEvaluating with LLM judge...")
    eval_tasks = []
    for (name, _), characters in zip(STRATEGIES.items(), all_characters):
        eval_tasks.append(evaluate_characters(name, characters))

    all_evaluations = await asyncio.gather(*eval_tasks)

    # Compile results
    for (name, _), characters, evaluation in zip(
        STRATEGIES.items(), all_characters, all_evaluations
    ):
        all_results[name] = {"characters": characters, "evaluation": evaluation}

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    for strategy, data in all_results.items():
        eval = data["evaluation"]
        print(f"\n### {strategy.upper()} ###")
        print(f"Overall Score: {eval.overall_score}/100")
        print(f"Diversity: {eval.diversity_score}/100")
        print(f"Clichés: {eval.cliche_score}/100 (lower is better)")
        print(f"Specificity: {eval.specificity_score}/100")
        print(f"Memorability: {eval.memorability_score}/100")
        print(f"Best: {eval.best_character}")
        print(f"Worst: {eval.worst_character}")
        print(f"Summary: {eval.summary}")

        # Show character names
        names = [c.name for c in data["characters"]]
        print(f"Characters: {names}")

    # Ranking
    print("\n" + "=" * 80)
    print("FINAL RANKING BY OVERALL SCORE")
    print("=" * 80)

    sorted_results = sorted(
        all_results.items(),
        key=lambda x: x[1]["evaluation"].overall_score,
        reverse=True,
    )

    print(
        f"\n{'Rank':<6} {'Strategy':<20} {'Overall':<10} {'Diversity':<12} {'Clichés':<10}"
    )
    print("-" * 60)

    for i, (strategy, data) in enumerate(sorted_results, 1):
        eval = data["evaluation"]
        print(
            f"{i:<6} {strategy:<20} {eval.overall_score:<10} {eval.diversity_score:<12} {eval.cliche_score:<10}"
        )

    # Winner details
    winner = sorted_results[0]
    print(f"\n🏆 WINNER: {winner[0]}")
    print(f"Score: {winner[1]['evaluation'].overall_score}/100")
    print("\nTop 3 characters:")
    for i, char in enumerate(winner[1]["characters"][:3], 1):
        print(f"\n{i}. {char.name}")
        print(f"   {char.description}")


if __name__ == "__main__":
    asyncio.run(main())
