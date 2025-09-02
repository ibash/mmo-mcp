"""Test to optimize the multi-stage approach - finding minimum concepts needed and adding stages."""

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


class CharacterWithProcess(BaseModel):
    """A character with the generation process shown."""

    concepts_list: List[str] = Field(description="The initial concepts")
    selected_concept: str = Field(description="The concept selected as most unique")
    selection_reasoning: str = Field(description="Why this concept was selected")
    character: Character = Field(description="The final expanded character")


class CharacterWithEnhancedProcess(BaseModel):
    """A character with enhanced multi-stage process."""

    concepts_list: List[str] = Field(description="The initial concepts")
    selected_concept: str = Field(description="The concept selected as most unique")
    selection_reasoning: str = Field(description="Why this concept was selected")
    anti_patterns_identified: List[str] = Field(description="Cliché patterns to avoid")
    specific_details_added: List[str] = Field(description="Concrete details added")
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


def create_multistage_prompt(num_concepts: int) -> str:
    """Create a multi-stage prompt with specified number of concepts."""
    return f"""Create a character following these EXACT steps:

STEP 1: Generate {num_concepts} COMPLETELY DIFFERENT one-sentence character concepts.
Each must be wildly different from the others in:
- Profession/background
- Personality type  
- Age/generation
- Cultural background
- Core problem/concern

Make them specific and unusual. No generic fantasy archetypes.

STEP 2: From your {num_concepts} concepts, select the ONE that would be MOST DIFFERENT from the other {num_concepts - 1} and from typical fantasy characters.
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


ENHANCED_MULTISTAGE_PROMPT = """Create a character following these EXACT steps:

STEP 1: Generate 15 COMPLETELY DIFFERENT one-sentence character concepts.
Each must be wildly different from the others in:
- Profession/background
- Personality type  
- Age/generation
- Cultural background
- Core problem/concern

Make them specific and unusual. No generic fantasy archetypes.

STEP 2: From your 15 concepts, select the ONE that would be MOST DIFFERENT from the other 14 and from typical fantasy characters.
Choose the one that shares the LEAST in common with standard game characters. Maximum uniqueness.

STEP 3: ANTI-PATTERN CHECK
List 5 cliché patterns this character must avoid:
- Generic names (Shadow, Storm, Whisper)
- Vague descriptions (mysterious, ancient, ethereal)
- Fantasy tropes (dark past, chosen one, seeking revenge)
- Generic items (mysterious amulet, ancient tome)
- Undefined motivations (searching for purpose, haunted by memories)

STEP 4: ADD CONCRETE DETAILS
Add 5 specific, mundane details:
- Exact amount of money they have
- Specific brand/model of something they own
- Precise time they need to be somewhere
- Specific food they're craving
- Exact address or location they remember

STEP 5: FINAL EXPANSION
Create the full character incorporating steps 3-4:
- Use a realistic, non-fantasy name
- Include the specific details from step 4
- Avoid all patterns from step 3
- Make them feel like a real person, not a game character

Execute these steps now, showing your work:"""


VERIFICATION_STAGE_PROMPT = """Create a character following these EXACT steps:

STEP 1: Generate 12 COMPLETELY DIFFERENT one-sentence character concepts.
Each must be wildly different from the others.
Make them specific and unusual. No generic fantasy archetypes.

STEP 2: From your 12 concepts, select the ONE that would be MOST DIFFERENT from typical fantasy characters.

STEP 3: Expand this concept into a character draft.

STEP 4: VERIFICATION CHECK
Review your character for these red flags:
- Is the name fantasy-sounding? (Shadow, Storm, etc.)
- Are there vague descriptors? (mysterious, ancient)
- Is there a tragic backstory?
- Are they on a quest or journey?
- Do they have special powers or destiny?

If ANY red flags exist, REVISE the character to remove them.

STEP 5: OUTPUT FINAL CHARACTER
Present the verified, cliché-free character.

Execute these steps now, showing your work:"""


CONTRAST_EMPHASIS_PROMPT = """Create a character following these EXACT steps:

STEP 1: LIST WHAT EVERYONE ELSE CREATES
Write down 5 typical character patterns:
- Mysterious warriors with dark pasts
- Wise mages with ancient knowledge
- Rogues with hearts of gold
- Characters named Shadow/Storm/Raven
- People on epic quests

STEP 2: Generate 10 character concepts that are OPPOSITE to the above.
Each concept must actively contradict typical patterns.

STEP 3: Select the concept that contrasts MOST with typical fantasy.

STEP 4: Expand into a full character, ensuring every detail contrasts with fantasy norms.

Execute these steps now, showing your work:"""


async def test_concept_count(count: int) -> Dict:
    """Test a specific number of concepts."""
    prompt = create_multistage_prompt(count)

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=prompt,
        output_type=CharacterWithProcess,
    )

    # Generate 3 characters for faster testing
    tasks = [
        agent.run(f"Execute the multi-stage character creation process #{i + 1}")
        for i in range(3)
    ]
    results = await asyncio.gather(*tasks)
    characters = [r.output.character for r in results]

    # Evaluate
    evaluation = await evaluate_characters(f"{count} concepts", characters)

    return {
        "count": count,
        "characters": characters,
        "evaluation": evaluation,
        "sample_process": results[0].output,  # Keep one example of the process
    }


async def test_enhanced_approach(
    name: str, prompt: str, output_type=CharacterWithProcess
) -> Dict:
    """Test an enhanced multi-stage approach."""

    agent = Agent(
        AnthropicModel(
            "claude-3-7-sonnet-latest",
            provider=AnthropicProvider(api_key=settings.anthropic_api_key),
        ),
        system_prompt=prompt,
        output_type=output_type,
    )

    # Generate 3 characters for faster testing
    tasks = [
        agent.run(f"Execute the character creation process #{i + 1}") for i in range(3)
    ]
    results = await asyncio.gather(*tasks)
    characters = [r.output.character for r in results]

    # Evaluate
    evaluation = await evaluate_characters(name, characters)

    return {
        "name": name,
        "characters": characters,
        "evaluation": evaluation,
        "sample_process": results[0].output,
    }


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
    """Test optimizations to multi-stage approach."""

    print("Testing Multi-Stage Optimizations")
    print("=" * 80)

    # Part 1: Test different concept counts
    print("\nPART 1: OPTIMAL CONCEPT COUNT")
    print("-" * 40)
    print("Testing different numbers of initial concepts...")

    concept_counts = [5, 10, 15, 20]
    count_tasks = [test_concept_count(count) for count in concept_counts]
    count_results = await asyncio.gather(*count_tasks)

    print("\nConcept Count Results:")
    print(
        f"{'Count':<8} {'Overall':<10} {'Diversity':<12} {'Clichés':<10} {'Specificity':<12}"
    )
    print("-" * 60)

    for result in count_results:
        eval = result["evaluation"]
        print(
            f"{result['count']:<8} {eval.overall_score:<10} {eval.diversity_score:<12} {eval.cliche_score:<10} {eval.specificity_score:<12}"
        )

    # Find optimal count
    best_count_result = max(count_results, key=lambda x: x["evaluation"].overall_score)
    print(
        f"\n✓ Optimal concept count: {best_count_result['count']} (Score: {best_count_result['evaluation'].overall_score}/100)"
    )

    # Show sample from best count
    print(f"\nSample concepts from {best_count_result['count']}-concept approach:")
    sample = best_count_result["sample_process"]
    for i, concept in enumerate(sample.concepts_list[:5], 1):
        print(f"{i}. {concept}")
    print(f"Selected: {sample.selected_concept}")

    # Part 2: Test enhanced approaches
    print("\n" + "=" * 80)
    print("PART 2: ENHANCED MULTI-STAGE APPROACHES")
    print("-" * 40)
    print("Testing approaches with additional stages...")

    enhanced_approaches = [
        (
            "Enhanced (Anti-patterns + Details)",
            ENHANCED_MULTISTAGE_PROMPT,
            CharacterWithEnhancedProcess,
        ),
        ("Verification Stage", VERIFICATION_STAGE_PROMPT, CharacterWithProcess),
        ("Contrast Emphasis", CONTRAST_EMPHASIS_PROMPT, CharacterWithProcess),
    ]

    enhanced_tasks = [
        test_enhanced_approach(name, prompt, output_type)
        for name, prompt, output_type in enhanced_approaches
    ]
    enhanced_results = await asyncio.gather(*enhanced_tasks)

    # Add baseline for comparison (original 20-concept approach)
    baseline = await test_enhanced_approach(
        "Baseline (20 concepts)", create_multistage_prompt(20), CharacterWithProcess
    )

    print("\nEnhanced Approach Results:")
    print(
        f"{'Approach':<35} {'Overall':<10} {'Diversity':<12} {'Clichés':<10} {'Specificity':<12}"
    )
    print("-" * 85)

    print(
        f"{'Baseline (20 concepts)':<35} {baseline['evaluation'].overall_score:<10} {baseline['evaluation'].diversity_score:<12} {baseline['evaluation'].cliche_score:<10} {baseline['evaluation'].specificity_score:<12}"
    )

    for result in enhanced_results:
        eval = result["evaluation"]
        print(
            f"{result['name']:<35} {eval.overall_score:<10} {eval.diversity_score:<12} {eval.cliche_score:<10} {eval.specificity_score:<12}"
        )

    # Find best approach
    all_results = enhanced_results + [baseline]
    best_approach = max(all_results, key=lambda x: x["evaluation"].overall_score)

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(f"\n🏆 BEST CONCEPT COUNT: {best_count_result['count']} concepts")
    print(f"   Score: {best_count_result['evaluation'].overall_score}/100")

    print(f"\n🏆 BEST APPROACH: {best_approach['name']}")
    print(f"   Score: {best_approach['evaluation'].overall_score}/100")
    print(f"   Summary: {best_approach['evaluation'].summary}")

    print("\nTop 3 characters from best approach:")
    for i, char in enumerate(best_approach["characters"][:3], 1):
        print(f"\n{i}. {char.name}")
        print(f"   {char.description}")

    # If enhanced approach has special process info, show it
    if hasattr(best_approach["sample_process"], "anti_patterns_identified"):
        print("\nSample process details from enhanced approach:")
        print(
            "Anti-patterns identified:",
            best_approach["sample_process"].anti_patterns_identified[:3],
        )
        print(
            "Specific details added:",
            best_approach["sample_process"].specific_details_added[:3],
        )


if __name__ == "__main__":
    asyncio.run(main())
