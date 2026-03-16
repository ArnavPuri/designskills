# Contributing to designskills

Thank you for your interest in contributing design skills. This guide covers everything you need to create, validate, and submit a new skill.

## Creating a New Skill

### Directory Structure

Each skill lives in its own directory at the repository root:

```
your-skill-name/
  SKILL.md
```

The directory name must be lowercase, use hyphens for spaces, and match the `name` field in the SKILL.md frontmatter.

### SKILL.md Format

Every skill file must start with YAML frontmatter followed by the skill content in Markdown:

```markdown
---
name: your-skill-name
description: A concise one-line description of what this skill does
license: MIT
---

# Your Skill Name

## Overview

Brief explanation of the skill's purpose and when to use it.

## Steps

1. Step one...
2. Step two...
3. Step three...

## Frameworks & Principles

- Principle or framework details...

## Examples

Concrete examples of inputs and expected outputs.
```

### YAML Frontmatter Requirements

The following fields are required in the frontmatter:

| Field | Description |
|-------|-------------|
| `name` | Must exactly match the directory name |
| `description` | One-line summary, under 120 characters |
| `license` | Must be `MIT` |

## Content Guidelines

- **Under 500 lines.** Skills should be focused and concise. If your skill exceeds 500 lines, consider splitting it into multiple skills.
- **Step-by-step structure.** Use numbered steps or clear sections so the agent can follow a predictable workflow.
- **Include frameworks.** Encode expert-level design knowledge as reusable frameworks, checklists, or decision trees rather than vague advice.
- **Be opinionated.** Good skills make specific recommendations. Instead of "choose appropriate colors," say "use a 60-30-10 color ratio with the primary brand color at 60%."
- **Reference design-context.** Where applicable, instruct the agent to pull brand parameters from the `design-context` skill output.
- **Provide examples.** Include at least one concrete example showing expected input and output.

## Validation

Before submitting, run the validation script:

```bash
bash validate-skills.sh
```

This checks:

- YAML frontmatter is present and valid
- `name` field matches the directory name
- `description` and `license` fields are present
- File is under 500 lines
- File uses `.md` extension

You can also validate a single skill:

```bash
bash validate-skills.sh your-skill-name
```

## Pull Request Process

1. **Fork** the repository and create a feature branch (`feat/your-skill-name`).
2. **Create** the skill directory and `SKILL.md` following the format above.
3. **Validate** your skill by running `validate-skills.sh`.
4. **Update** the README.md to include your skill in the appropriate category table.
5. **Submit** a pull request with:
   - A clear title: `Add skill: your-skill-name`
   - A description explaining what the skill does and why it belongs in the collection
   - Any references to design resources or frameworks the skill is based on
6. **Review.** A maintainer will review for quality, consistency, and overlap with existing skills.

## Questions?

Open an issue with the `question` label and we will get back to you.
