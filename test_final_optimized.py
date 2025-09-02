"""Test the final optimized character generation approach."""

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


class OptimizedCharacterProcess(BaseModel):
    """Optimized character generation process."""

    concepts: List[str] = Field(description="5 wildly different character concepts")
    selected_concept: str = Field(description="The most unique concept selected")
    why_unique: str = Field(
        description="Why this is most different from typical fantasy"
    )
    avoided_patterns: List[str] = Field(
        description="Cliché patterns explicitly avoided"
    )
    specific_details: List[str] = Field(description="Concrete mundane details added")
    character: Character = Field(description="The final character")


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


# The optimized prompt based on our findings
OPTIMIZED_PROMPT = """Create a character following these EXACT steps:

STEP 1: Generate EXACTLY 5 wildly different one-sentence character concepts.
CRITICAL: Each must be COMPLETELY different from the others in ALL of these:
- Age (span from teen to elderly)  
- Background (different fields/lifestyles)
- Core problem (mundane vs existential vs practical)
- Personality (opposite types)
- Social class/education

Make them specific people with real problems, NOT fantasy archetypes.

STEP 2: Select the ONE concept that would be MOST UNUSUAL in a fantasy game.
Ask yourself: Which person would players LEAST expect to encounter?
Choose the one that breaks the most genre expectations.

STEP 3: List 3 cliché patterns to AVOID:
- Generic fantasy names (Shadow, Storm, Raven, etc.)
- Vague descriptors (mysterious, ancient, haunted)
- Standard motivations (revenge, destiny, dark past)

STEP 4: Add 3 extremely specific mundane details:
- Exact amount of money in their pocket ($X.XX)
- Specific brand/model of something they own
- Precise time/date that matters to them

STEP 5: Expand into a full character using Steps 3-4:
- Give them a normal first and last name
- Include the specific details from Step 4
- Make them feel like someone you'd meet at a bus stop
- Explain why they're here (wrong place/time, NOT destiny)

Execute ALL steps, showing your work:"""


# Baseline for comparison
BASELINE_PROMPT = """Create a unique character for a multiplayer dungeon crawler game.
Be creative and avoid clichés."""


async def generate_characters(prompt: str, output_type, count: int = 5) -> List:
    """Generate multiple characters with given prompt."""

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=prompt,
        output_type=output_type,
    )

    tasks = [agent.run(f"Create character #{i + 1}") for i in range(count)]
    results = await asyncio.gather(*tasks)

    if output_type == Character:
        return [r.output for r in results]
    else:
        return [r.output.character for r in results], [r.output for r in results]


async def evaluate_characters(
    approach_name: str, characters: List[Character]
) -> CharacterEvaluation:
    """Evaluate character diversity and quality."""

    character_text = "\n\n".join([f"**{c.name}**\n{c.description}" for c in characters])

    evaluation_prompt = f"""Evaluate these {len(characters)} characters from approach: {approach_name}

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
    """Test the final optimized approach."""

    print("Testing Final Optimized Character Generation")
    print("=" * 80)

    # Generate characters with both approaches
    print("\nGenerating characters...")

    print("Testing baseline approach...")
    baseline_chars = await generate_characters(BASELINE_PROMPT, Character, count=5)

    print("Testing optimized approach...")
    optimized_chars, optimized_processes = await generate_characters(
        OPTIMIZED_PROMPT, OptimizedCharacterProcess, count=5
    )

    # Evaluate both
    print("\nEvaluating...")
    baseline_eval = await evaluate_characters("Baseline", baseline_chars)
    optimized_eval = await evaluate_characters("Optimized", optimized_chars)

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    print("\n### BASELINE ###")
    print(f"Overall Score: {baseline_eval.overall_score}/100")
    print(f"Diversity: {baseline_eval.diversity_score}/100")
    print(f"Clichés: {baseline_eval.cliche_score}/100 (lower is better)")
    print(f"Specificity: {baseline_eval.specificity_score}/100")
    print(f"Memorability: {baseline_eval.memorability_score}/100")
    print(f"Summary: {baseline_eval.summary}")
    print("\nCharacters:")
    for char in baseline_chars:
        print(f"- {char.name}")

    print("\n### OPTIMIZED ###")
    print(f"Overall Score: {optimized_eval.overall_score}/100")
    print(f"Diversity: {optimized_eval.diversity_score}/100")
    print(f"Clichés: {optimized_eval.cliche_score}/100 (lower is better)")
    print(f"Specificity: {optimized_eval.specificity_score}/100")
    print(f"Memorability: {optimized_eval.memorability_score}/100")
    print(f"Summary: {optimized_eval.summary}")
    print("\nCharacters:")
    for char in optimized_chars:
        print(f"- {char.name}")

    # Show improvement
    improvement = optimized_eval.overall_score - baseline_eval.overall_score
    print("\n" + "=" * 80)
    if improvement > 0:
        print(
            f"✅ IMPROVEMENT: +{improvement} points ({baseline_eval.overall_score} → {optimized_eval.overall_score})"
        )
    else:
        print(f"❌ No improvement: {improvement} points")

    # Show sample process
    print("\n" + "=" * 80)
    print("SAMPLE OPTIMIZED PROCESS")
    print("=" * 80)

    sample = optimized_processes[0]
    print("\n5 Initial Concepts:")
    for i, concept in enumerate(sample.concepts, 1):
        print(f"{i}. {concept}")

    print(f"\nSelected: {sample.selected_concept}")
    print(f"Why unique: {sample.why_unique}")

    print(f"\nAvoided patterns: {sample.avoided_patterns}")
    print(f"Specific details added: {sample.specific_details}")

    print(f"\nFinal character: {sample.character.name}")
    print(f"Description: {sample.character.description}")

    # If optimized wins by a lot, show the winning prompt
    if improvement >= 10:
        print("\n" + "=" * 80)
        print("🏆 WINNING PROMPT (for implementation)")
        print("=" * 80)
        print("\n" + OPTIMIZED_PROMPT)


if __name__ == "__main__":
    asyncio.run(main())
