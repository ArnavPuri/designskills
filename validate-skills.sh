#!/usr/bin/env bash
#
# validate-skills.sh
# Validates skill format for the designskills repository.
#
# Usage:
#   bash validate-skills.sh              # validate all skills
#   bash validate-skills.sh skill-name   # validate a single skill

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
MAX_LINES=500
ERRORS=0
CHECKED=0

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow(){ printf '\033[0;33m%s\033[0m\n' "$*"; }

validate_skill() {
    local dir_name="$1"
    local skill_dir="$SKILLS_DIR/$dir_name"
    local skill_file="$skill_dir/SKILL.md"

    CHECKED=$((CHECKED + 1))

    # Check SKILL.md exists
    if [[ ! -f "$skill_file" ]]; then
        red "FAIL: $dir_name - missing SKILL.md"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Check YAML frontmatter exists (file starts with ---)
    local first_line
    first_line="$(head -n 1 "$skill_file")"
    if [[ "$first_line" != "---" ]]; then
        red "FAIL: $dir_name - SKILL.md must start with YAML frontmatter (---)"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Extract frontmatter (between first and second ---)
    local frontmatter
    frontmatter="$(awk 'BEGIN{found=0} /^---$/{found++; if(found==2) exit; next} found==1{print}' "$skill_file")"

    if [[ -z "$frontmatter" ]]; then
        red "FAIL: $dir_name - could not parse YAML frontmatter (missing closing ---)"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Check required fields
    local name_field description_field license_field
    name_field="$(echo "$frontmatter" | grep -E '^name:' | sed 's/^name:[[:space:]]*//' | tr -d '"' | tr -d "'")"
    description_field="$(echo "$frontmatter" | grep -E '^description:' | sed 's/^description:[[:space:]]*//')"
    license_field="$(echo "$frontmatter" | grep -E '^license:' | sed 's/^license:[[:space:]]*//' | tr -d '"' | tr -d "'")"

    if [[ -z "$name_field" ]]; then
        red "FAIL: $dir_name - frontmatter missing 'name' field"
        ERRORS=$((ERRORS + 1))
        return
    fi

    if [[ "$name_field" != "$dir_name" ]]; then
        red "FAIL: $dir_name - frontmatter name '$name_field' does not match directory name '$dir_name'"
        ERRORS=$((ERRORS + 1))
        return
    fi

    if [[ -z "$description_field" ]]; then
        red "FAIL: $dir_name - frontmatter missing 'description' field"
        ERRORS=$((ERRORS + 1))
        return
    fi

    if [[ -z "$license_field" ]]; then
        red "FAIL: $dir_name - frontmatter missing 'license' field"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Check name format (lowercase letters, digits, hyphens)
    if ! [[ "$name_field" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        red "FAIL: $dir_name - name must be lowercase letters, digits, and hyphens"
        ERRORS=$((ERRORS + 1))
        return
    fi

    if [[ "$license_field" != "MIT" ]]; then
        red "FAIL: $dir_name - license must be MIT (found '$license_field')"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Full description text (handles folded '>' / '|' multi-line values)
    local description_text
    description_text="$(echo "$frontmatter" | awk '
        /^description:/ { on=1; sub(/^description:[[:space:]]*[>|]?-?[[:space:]]*/, ""); if ($0 != "") printf "%s ", $0; next }
        on && /^[a-zA-Z_-]+:/ { on=0 }
        on { gsub(/^[[:space:]]+/, ""); printf "%s ", $0 }
    ' | sed 's/[[:space:]]*$//')"

    if [[ ${#description_text} -lt 50 ]]; then
        red "FAIL: $dir_name - description is too short (${#description_text} chars); say what the skill does and when to use it"
        ERRORS=$((ERRORS + 1))
        return
    fi

    if [[ ${#description_text} -gt 1024 ]]; then
        red "FAIL: $dir_name - description is ${#description_text} chars (max 1024)"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Referenced skills (`skill-name` followed by "skill") must exist
    local ref missing_refs=""
    while IFS= read -r ref; do
        [[ -z "$ref" ]] && continue
        if [[ ! -d "$SKILLS_DIR/$ref" ]]; then
            missing_refs+=" $ref"
        fi
    done < <(grep -oE '`[a-z0-9]+(-[a-z0-9]+)*` skill' "$skill_file" | sed -E 's/`([^`]*)` skill/\1/' | sort -u)
    if [[ -n "$missing_refs" ]]; then
        red "FAIL: $dir_name - references unknown skill(s):$missing_refs"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Every skill except design-context itself should consume design context
    if [[ "$dir_name" != "design-context" ]] && ! grep -q "design-context" "$skill_file"; then
        yellow "WARN: $dir_name - does not reference design-context"
    fi

    # Check line count
    local line_count
    line_count="$(wc -l < "$skill_file" | tr -d ' ')"
    if [[ "$line_count" -gt "$MAX_LINES" ]]; then
        red "FAIL: $dir_name - SKILL.md is $line_count lines (max $MAX_LINES)"
        ERRORS=$((ERRORS + 1))
        return
    fi

    green "PASS: $dir_name ($line_count lines)"
}

echo "=== designskills validator ==="
echo ""

if [[ $# -gt 0 ]]; then
    # Validate specific skill(s)
    for skill in "$@"; do
        if [[ -d "$SKILLS_DIR/$skill" ]]; then
            validate_skill "$skill"
        else
            red "FAIL: $skill - directory not found"
            ERRORS=$((ERRORS + 1))
            CHECKED=$((CHECKED + 1))
        fi
    done
else
    # Validate all skills (directories containing SKILL.md)
    found_any=false
    for skill_dir in "$SKILLS_DIR"/*/; do
        dir_name="$(basename "$skill_dir")"
        # Skip non-skill directories
        if [[ "$dir_name" == ".github" ]] || [[ "$dir_name" == "node_modules" ]]; then
            continue
        fi
        if [[ -f "$skill_dir/SKILL.md" ]]; then
            found_any=true
            validate_skill "$dir_name"
        fi
    done

    if [[ "$found_any" == false ]]; then
        yellow "No skills found. Create a skill directory with a SKILL.md file to get started."
        exit 0
    fi
fi

echo ""
echo "Checked: $CHECKED | Passed: $((CHECKED - ERRORS)) | Failed: $ERRORS"

if [[ "$ERRORS" -gt 0 ]]; then
    echo ""
    red "Validation failed with $ERRORS error(s)."
    exit 1
else
    echo ""
    green "All skills passed validation."
    exit 0
fi
