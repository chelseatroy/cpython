# AI Coding Tools Summary

Summary of conversation about AI coding assistants, agents, and configuration.

---

## Tools Discussed

| Tool | Type | Made By |
|------|------|---------|
| **Claude Code** | CLI coding assistant | Anthropic |
| **GitHub Copilot** | IDE extension + chat | GitHub/Microsoft |
| **Cursor** | AI-native code editor (VS Code fork) | Cursor Inc |
| **Aider** | CLI coding assistant | Paul Gauthier (open source) |
| **Continue** | IDE extension | Continue (open source) |
| **ChatGPT/Codex** | Web/API-based assistant | OpenAI |

---

## How Each Tool Relates to "Agentic"

The term "agent" means different things across tools:

| Tool | What "Agentic" Means |
|------|---------------------|
| **Claude Code** | Subprocesses spawned for parallel/specialized tasks (Explore, Plan, Bash agents). Claude itself is already agentic by default (reads files, runs commands, edits code). |
| **GitHub Copilot** | Scoped contexts (`@workspace`, `@terminal`, `@vscode`) that determine what the AI can access. These are more like "permission scopes" than autonomous agents. |
| **Cursor** | Similar to Copilot - the AI can access codebase context. "Agentic" features are built into the editor experience. |
| **Aider** | The tool itself is agentic (edits files, makes git commits). No sub-agents; the whole tool is one agent. |
| **Continue** | Custom slash commands and tool use. Agentic in the sense of taking actions. |
| **ChatGPT/Codex** | "Agents" typically means tool-use capabilities (code execution, web browsing) or custom GPTs (pre-configured personas). |

**Key insight:** The industry uses "agent" loosely to mean "AI that can take actions," but architectures vary significantly.

---

## Claude Code Agent Types

Claude Code can spawn these specialized sub-agents via the Task tool:

| Agent Type | Purpose | Tools Available |
|------------|---------|-----------------|
| **Explore** | Fast codebase exploration - find files, search code, answer questions about structure | Glob, Grep, Read, WebFetch, WebSearch |
| **Plan** | Design implementation strategies, identify critical files, consider trade-offs | All read-only tools |
| **Bash** | Command execution specialist for git, npm, terminal tasks | Bash |
| **general-purpose** | Multi-step research, complex searches, autonomous task handling | All tools |

**When Claude uses agents:**
- Exploring unfamiliar codebases
- Planning complex implementations
- Running background/parallel tasks
- Deep searches that may require multiple rounds

---

## Configuration for Agentic Features

### Claude Code

**Files:**
- `CLAUDE.md` (project root) - Project context and behavioral instructions
- `.claude/settings.local.json` (project) - Hooks, permissions, project settings
- `~/.claude/settings.json` (global) - Global settings

**Format:** Markdown for CLAUDE.md, JSON for settings

**Example CLAUDE.md:**
```markdown
# Project Overview
This is a Python project using FastAPI.

## Build Commands
- `make test` - Run tests
- `make build` - Build project

## Coding Conventions
- Follow PEP 8
- Never commit to main directly
```

**Example settings.local.json (hooks):**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "python path/to/script.py"
          }
        ]
      }
    ]
  }
}
```

---

### GitHub Copilot

**Files:**
- `.github/copilot-instructions.md` - Project-level instructions

**Format:** Markdown

**Example:**
```markdown
# Copilot Instructions

This is a TypeScript React project.

## Conventions
- Use functional components with hooks
- Prefer named exports
- Use CSS modules for styling
```

---

### Cursor

**Files:**
- `.cursorrules` (project root) - Project instructions and coding rules

**Format:** Markdown or plain text

**Example:**
```markdown
You are an expert in TypeScript and React.

Key conventions:
- Use functional components
- Use TypeScript strict mode
- Prefer composition over inheritance
```

---

### Aider

**Files:**
- `.aider.conf.yml` (project root) - Operational configuration
- Can also use command-line flags or environment variables

**Format:** YAML

**Example:**
```yaml
model: gpt-4
auto-commits: true
gitignore: true
attribute-author: true
attribute-committer: false
```

**Note:** Aider config is primarily operational (which model, git behavior) rather than behavioral (how to code).

---

### Continue

**Files:**
- `~/.continue/config.json` - Global configuration

**Format:** JSON

**Example:**
```json
{
  "models": [
    {
      "title": "GPT-4",
      "provider": "openai",
      "model": "gpt-4"
    }
  ],
  "customCommands": [
    {
      "name": "test",
      "prompt": "Write unit tests for this code"
    }
  ]
}
```

---

## Key Differences Summary

| Aspect | Claude Code | Cursor | Copilot | Aider | Continue |
|--------|-------------|--------|---------|-------|----------|
| **Config format** | MD + JSON | MD/text | MD | YAML | JSON |
| **Behavioral instructions** | CLAUDE.md | .cursorrules | copilot-instructions.md | Limited | Limited |
| **Operational settings** | settings.json | In-app | In-app | .aider.conf.yml | config.json |
| **Hooks/automation** | Yes | No | No | Git hooks only | Custom commands |
| **Sub-agents** | Yes (Explore, Plan, etc.) | No | Scoped contexts | No | No |
| **Model choice** | Claude family | Curated (GPT, Claude) | GPT/Claude | Any (bring your own) | Configurable |

---

## Also Built in This Conversation

We created a query tracking system for Claude Code:

- **`ai-coding-tools/track_queries.py`** - Tracks query type, risk level, token counts (estimated via hybrid heuristic), and cost
- **`.ai-data/query_log.csv`** - Output CSV with historical data
- **`.ai-data/query_analysis.ipynb`** - Jupyter notebook for analyzing the data
- **`.claude/settings.local.json`** - Hook configuration to run tracker automatically

The hybrid token estimation heuristic uses:
1. Character-based input estimation (~4 chars = 1 token)
2. Daily aggregate calibration from Claude's stats
3. Query-type output multipliers (code_generation: 5x, explanation: 3x, etc.)

===

 Hi Claude! If I open multiple claudes in multiple terminal windows, is that effectively separate
  agents who do not share contexts?

⏺ Yes, exactly. Each Claude Code instance in a separate terminal window is independent:

  - Separate contexts: Each instance maintains its own conversation history and has no knowledge of what's
  happening in other windows
  - No shared state: They don't communicate with each other or share memory
  - Independent working directories: Each can be in different directories and work on different tasks

  This can be useful for parallelizing work across different parts of a codebase, but you'll need to
  coordinate manually (e.g., making sure two instances don't edit the same file simultaneously, which could
  cause conflicts).

  If you want coordinated parallel work within a single session, you can ask me to run multiple tasks in the
   background using the Task tool - those share the conversation context and I can coordinate their work.

❯ Great. How is the task tool different from a skill?

⏺ Good question. Here's the distinction:

  Task tool - Spawns autonomous subagents that work independently:
  - Creates a separate agent process with its own context
  - Has specialized agent types (Explore, Plan, Bash, etc.) with specific toolsets
  - Can run in the background while I continue other work
  - Returns results when done
  - Useful for parallelizing complex, multi-step work

  Skills - Named workflows/commands that run in the main conversation:
  - Invoked via slash commands like /commit or /review-pr
  - Execute within the current conversation context (not a separate agent)
  - Predefined sequences of actions for common tasks
  - Think of them as macros or recipes

  In short: Tasks are about delegating work to parallel workers. Skills are about invoking specific named
  workflows inline.

❯ Ah. Tasks are the thing that you were saying you can spawn automatically. Can you please remind me:
  1. When do you spawn these automatically and how do you pick which type to spawn, and 2. How would I
  spawn a task manually?

⏺ 1. When I spawn automatically:

  I spawn tasks when work matches an agent's specialty. The main triggers:

  - Explore agent: When you ask open-ended questions about a codebase (e.g., "How does authentication work
  here?" or "What's the project structure?") rather than asking for a specific file/function
  - Plan agent: When designing implementation strategy for complex features
  - Bash agent: For git operations or command execution tasks
  - General-purpose agent: For multi-step research or searches where I'm not confident I'll find the right
  match quickly

  The agent descriptions in my instructions guide the selection.

  2. How you spawn manually:

  You can't invoke the Task tool directly, but you can ask me to:
  - "Use an agent to explore how the API layer works"
  - "Spawn a background agent to run the tests while we keep talking"
  - "Search for X in parallel with Y" (I'll spawn multiple agents)

  Or just describe work that fits an agent's specialty and I'll use one. You can also explicitly say "use
  the Explore agent" or "run this in the background" if you want to be specific about the approach.

⏺ I understand the frustration. Let me explain the Task system.

  Agent Types Available
  Agent: Explore
  Purpose: Fast codebase exploration - finding files by pattern, searching for keywords,

    answering questions about code structure
  Tools Available: Read-only tools (no editing)
  ────────────────────────────────────────
  Agent: Plan
  Purpose: Designing implementation strategies, identifying critical files, considering
    architectural trade-offs
  Tools Available: Read-only tools (no editing)
  ────────────────────────────────────────
  Agent: Bash
  Purpose: Command execution - git operations, builds, terminal tasks
  Tools Available: Bash only
  ────────────────────────────────────────
  Agent: general-purpose
  Purpose: Complex multi-step research, code searching when multiple rounds might be
    needed
  Tools Available: All tools
  ────────────────────────────────────────
  Agent: claude-code-guide
  Purpose: Questions about Claude Code features, Agent SDK, or Claude API
  Tools Available: Read, search, web tools
  When I Start Them Automatically

  - Explore agent: When you ask open-ended questions about the codebase (e.g., "How does
   error handling work?" or "What's the codebase structure?")
  - Plan agent: When you need implementation strategy designed before coding
  - general-purpose: When searching for something where I'm not confident I'll find it
  quickly, or for complex multi-step research

  How to Start One Manually

  Just ask directly:
  - "Use an Explore agent to find all the parser-related code"
  - "Spawn a Plan agent to design how we'd add feature X"
  - "Run agents in parallel to search for X and Y" (I'll launch multiple simultaneously)

  You can also specify thoroughness for Explore: "quick", "medium", or "very thorough".

  Want me to demonstrate any of these?


