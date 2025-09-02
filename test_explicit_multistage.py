"""Test multi-stage approach where LLM explicitly writes out all steps."""

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


class CharacterWithProcess(BaseModel):
    """A character with the generation process shown."""

    concepts_list: List[str] = Field(description="The 20 initial concepts")
    selected_concept: str = Field(description="The concept selected as most unique")
    selection_reasoning: str = Field(description="Why this concept was selected")
    character: Character = Field(description="The final expanded character")


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


EXPLICIT_MULTISTAGE_PROMPT = """Create a character following these EXACT steps:

STEP 1: Generate 20 COMPLETELY DIFFERENT one-sentence character concepts.
Each must be wildly different from the others in:
- Profession/background
- Personality type  
- Age/generation
- Cultural background
- Core problem/concern

Make them specific and unusual. No generic fantasy archetypes.

STEP 2: From your 20 concepts, select the ONE that would be MOST DIFFERENT from the other 19 and from typical fantasy characters.
Choose the one that shares the LEAST in common with standard game characters. Maximum uniqueness.

STEP 3: Expand this concept into a full character:

Create a specific, memorable character with:
- A distinctive name (not generic fantasy)
- Concrete physical details
- Specific items/possessions
- Clear motivations
- Memorable quirks

Make them feel real and three-dimensional.

Execute these steps now, showing your work:"""


BASELINE_PROMPT = """Create a unique character for a multiplayer dungeon crawler game.
Be creative and avoid clichés."""


async def create_character_explicit_multistage() -> CharacterWithProcess:
    """Create a character with explicit multi-stage process."""

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=EXPLICIT_MULTISTAGE_PROMPT,
        output_type=CharacterWithProcess,
    )

    result = await agent.run("Execute the multi-stage character creation process")
    return result.output


async def create_character_baseline() -> Character:
    """Create a character with baseline prompt."""

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=BASELINE_PROMPT,
        output_type=Character,
    )

    result = await agent.run("Create the character")
    return result.output


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


async def main():
    """Test explicit multi-stage vs baseline."""

    print("Testing Explicit Multi-Stage Character Generation")
    print("=" * 80)

    # Generate 5 characters with each approach
    print("\nGenerating characters with EXPLICIT multi-stage...")
    multistage_tasks = [create_character_explicit_multistage() for _ in range(5)]
    multistage_results = await asyncio.gather(*multistage_tasks)

    print("\nGenerating characters with BASELINE...")
    baseline_tasks = [create_character_baseline() for _ in range(5)]
    baseline_chars = await asyncio.gather(*baseline_tasks)

    # Extract just the characters from multistage results
    multistage_chars = [r.character for r in multistage_results]

    # Show the process for one example
    print("\n" + "=" * 80)
    print("EXAMPLE MULTI-STAGE PROCESS (Character #1)")
    print("=" * 80)

    example = multistage_results[0]
    print("\n20 INITIAL CONCEPTS:")
    for i, concept in enumerate(example.concepts_list, 1):
        print(f"{i}. {concept}")

    print(f"\nSELECTED CONCEPT: {example.selected_concept}")
    print(f"REASONING: {example.selection_reasoning}")
    print(f"\nFINAL CHARACTER: {example.character.name}")
    print(f"Description: {example.character.description}")

    # Evaluate both approaches
    print("\n" + "=" * 80)
    print("EVALUATION")
    print("=" * 80)

    multistage_eval = await evaluate_characters(
        "Explicit Multi-Stage", multistage_chars
    )
    baseline_eval = await evaluate_characters("Baseline", baseline_chars)

    # Compare results
    print("\n### EXPLICIT MULTI-STAGE ###")
    print(f"Overall Score: {multistage_eval.overall_score}/100")
    print(f"Diversity: {multistage_eval.diversity_score}/100")
    print(f"Clichés: {multistage_eval.cliche_score}/100 (lower is better)")
    print(f"Summary: {multistage_eval.summary}")
    print(f"Characters: {[c.name for c in multistage_chars]}")

    print("\n### BASELINE ###")
    print(f"Overall Score: {baseline_eval.overall_score}/100")
    print(f"Diversity: {baseline_eval.diversity_score}/100")
    print(f"Clichés: {baseline_eval.cliche_score}/100 (lower is better)")
    print(f"Summary: {baseline_eval.summary}")
    print(f"Characters: {[c.name for c in baseline_chars]}")

    # Winner
    print("\n" + "=" * 80)
    if multistage_eval.overall_score > baseline_eval.overall_score:
        print(
            f"🏆 WINNER: Explicit Multi-Stage ({multistage_eval.overall_score} vs {baseline_eval.overall_score})"
        )
        print(
            "\nThe explicit multi-stage approach where the LLM writes out all steps WORKS!"
        )
    else:
        print(
            f"🏆 WINNER: Baseline ({baseline_eval.overall_score} vs {multistage_eval.overall_score})"
        )
        print("\nThe explicit approach didn't help...")

    # Show concept diversity from all 5 multi-stage generations
    print("\n" + "=" * 80)
    print("CONCEPT SELECTION PATTERNS")
    print("=" * 80)
    print("\nWhat concepts were selected across 5 generations:")
    for i, result in enumerate(multistage_results, 1):
        print(f"{i}. {result.selected_concept}")


if __name__ == "__main__":
    asyncio.run(main())
