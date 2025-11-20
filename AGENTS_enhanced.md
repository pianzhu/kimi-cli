# Kimi CLI - AI Coding Agent

## Project Overview

Kimi CLI is an interactive command-line interface agent specializing in software engineering tasks. It's built with Python and provides a modular architecture for AI-powered development assistance. The project uses a sophisticated agent system with customizable tools, multiple UI modes, and extensive configuration options.

## Technology Stack

- **Language**: Python 3.13+
- **Package Management**: uv (modern Python package manager)
- **Build System**: uv_build
- **CLI Framework**: Typer
- **LLM Integration**: kosong (custom LLM framework)
- **Async Runtime**: asyncio
- **Testing**: pytest with asyncio support
- **Code Quality**: ruff (linting/formatting), pyright (type checking)
- **Distribution**: PyInstaller for standalone executables

## Architecture

### Core Components

1. **Agent System** (`src/kimi_cli/agent.py`)
   - YAML-based agent specifications
   - System prompt templating with builtin arguments
   - Tool loading and dependency injection
   - Subagent support for task delegation

2. **Soul Architecture** (`src/kimi_cli/soul/`)
   - `KimiSoul`: Main agent execution engine
   - `Context`: Session history management
   - `DenwaRenji`: Communication hub for tools
   - Event-driven architecture with retry mechanisms

3. **UI Modes** (`src/kimi_cli/ui/`)
   - **Shell**: Interactive terminal interface (default)
   - **Print**: Non-interactive mode for scripting
   - **ACP**: Agent Client Protocol server mode
   - **Wire**: Experimental wire protocol server

4. **Tool System** (`src/kimi_cli/tools/`)
   - Modular tool architecture with dependency injection
   - Built-in tools: bash, file operations, web search, task management
   - MCP (Model Context Protocol) integration for external tools
   - Custom tool development support

### Key Directories

```
src/kimi_cli/
├── agents/           # Default agent configurations
├── soul/            # Core agent execution logic
├── tools/           # Tool implementations
│   ├── bash/       # Shell command execution
│   ├── file/       # File operations (read, write, grep, etc.)
│   ├── web/        # Web search and URL fetching
│   ├── task/       # Subagent task delegation
│   ├── think/      # Internal reasoning tool
│   ├── todo/       # Task management
│   └── dmail/      # Time-travel messaging system
└── ui/              # User interface implementations
```

## Build and Development

### Installation

```bash
# Install with uv
uv sync

# Install development dependencies
uv sync --group dev
```

### Build Commands

```bash
# Format code
make format
# or: uv run ruff check --fix && uv run ruff format

# Run linting and type checking
make check
# or: uv run ruff check && uv run ruff format --check && uv run pyright

# Run tests
make test
# or: uv run pytest tests -vv

# Build standalone executable
uv run pyinstaller kimi.spec
```

### Additional Build Commands

```bash
# Prepare environment with locked dependencies
make prepare

# Run specific test files
uv run pytest tests/test_bash.py -vv

# Run tests with coverage
uv run pytest tests --cov=src/kimi_cli

# Type check specific files
uv run pyright src/kimi_cli/soul/
```

### Configuration

Configuration file: `~/.kimi/config.json`

Default configuration includes:

- LLM provider settings (Kimi API by default)
- Model configurations with context size limits
- Loop control parameters (max steps, retries)
- Service configurations (Moonshot Search API)

### Project Configuration Files

- **pyproject.toml**: Primary build configuration with dependencies and tool settings
- **kimi.spec**: PyInstaller specification for standalone executable
- **pyrightconfig.json**: Type checker configuration
- **.python-version**: Python version specification (3.13)
- **Makefile**: Build automation with common development tasks

## Testing Strategy

- **Unit Tests**: Comprehensive test coverage for all tools and core components
- **Integration Tests**: End-to-end testing of agent workflows
- **Mock Providers**: LLM interactions mocked for consistent testing
- **Fixtures**: Extensive pytest fixtures for agent components and tools
- **Async Testing**: Full async/await testing support

Test files follow the pattern `test_*.py` and are organized by component:

- `test_load_agent.py`: Agent loading and configuration
- `test_bash.py`: Shell command execution
- `test_*_file.py`: File operation tools
- `test_task_subagents.py`: Subagent functionality
- `test_session.py`: Session management
- `test_soul_message.py`: Core messaging system

### Test Organization

```
tests/
├── test_*.py          # Unit tests for core functionality
tests_ai/
└── test_*.py          # AI-related integration tests
```

## Code Style Guidelines

- **Line Length**: 100 characters maximum
- **Formatter**: ruff with specific rule selection
- **Type Hints**: Enforced by pyright
- **Import Organization**: isort rules applied
- **Error Handling**: Specific exception types with proper chaining
- **Logging**: Structured logging with loguru

Selected ruff rules:

- E: pycodestyle
- F: Pyflakes
- UP: pyupgrade
- B: flake8-bugbear
- SIM: flake8-simplify
- I: isort

### Type Checking

- **Strict Mode**: Applied to core modules in `src/kimi_cli/soul/`
- **Basic Mode**: Applied to other modules
- **Configuration**: Defined in `pyrightconfig.json`

## Security Considerations

- **File System Access**: Restricted to working directory by default
- **API Keys**: Handled as SecretStr with proper serialization
- **Shell Commands**: Executed with caution, user awareness emphasized
- **Network Requests**: Web tools with configurable endpoints
- **Session Management**: Persistent sessions with history tracking

### Safety Features

- **Approval System**: Tool execution requires user approval
- **Timeout Controls**: Configurable timeouts for command execution
- **Error Handling**: Comprehensive error handling with retry mechanisms
- **Logging**: Structured logging with rotation and retention policies
- **Directory Restrictions**: File operations limited to working directory

## Agent Development

### Custom Agent Creation

1. Create agent specification file (YAML format)
2. Define system prompt with template variables
3. Select and configure tools
4. Optionally extend existing agents

### Available Tools

- **Bash**: Execute shell commands
- **ReadFile**: Read file contents with line limits
- **WriteFile**: Write content to files
- **Glob**: File pattern matching
- **Grep**: Content searching with regex
- **StrReplaceFile**: String replacement in files
- **PatchFile**: Apply patches to files
- **SearchWeb**: Web search functionality
- **FetchURL**: Download web content
- **Task**: Delegate to subagents
- **SendDMail**: Time-travel messaging
- **Think**: Internal reasoning tool
- **SetTodoList**: Task management

### System Prompt Arguments

Builtin variables available in system prompts:

- `${KIMI_NOW}`: Current timestamp
- `${KIMI_WORK_DIR}`: Working directory path
- `${KIMI_WORK_DIR_LS}`: Directory listing output
- `${KIMI_AGENTS_MD}`: Project AGENTS.md content

## Deployment

- **PyPI Package**: Distributed as `kimi-cli`
- **Standalone Binary**: Built with PyInstaller
- **Entry Point**: `kimi` command-line tool
- **Configuration**: User-specific config in `~/.kimi/`

### CI/CD Pipeline

GitHub Actions workflow provides:
- **Multi-platform Builds**: Ubuntu, Windows, macOS support
- **Automated Testing**: Full test suite on all platforms
- **Binary Distribution**: Standalone executables via PyInstaller
- **Release Process**: Automated releases on tag push

### Distribution Methods

1. **PyPI Package**: `uv tool install kimi-cli`
2. **Standalone Binary**: Download from releases
3. **Development Install**: `uv sync` in project directory

## Dependencies

### Core Dependencies
- **LLM Framework**: `kosong==0.23.0` (custom LLM framework)
- **CLI Framework**: `typer==0.20.0`
- **Async Support**: `aiofiles==25.1.0`, `aiohttp==3.13.2`
- **UI/UX**: `rich==14.2.0`, `prompt-toolkit==3.0.52`
- **Data Processing**: `pyyaml==6.0.3`, `streamingjson==0.0.5`
- **Web Tools**: `trafilatura==2.0.0` (web content extraction)
- **MCP Support**: `fastmcp==2.12.5` (Model Context Protocol)

### Development Dependencies
- **Linting/Formatting**: `ruff>=0.14.4`
- **Type Checking**: `pyright>=1.1.407`
- **Testing**: `pytest>=9.0.0`, `pytest-asyncio>=1.3.0`
- **Build**: `pyinstaller>=6.16.0`

### Additional References

- For a Mandarin deep dive into the D-Mail/time-travel workflow, see `docs/dmail_time_travel_zh.md`.

## Version History

This project follows semantic versioning. For detailed version history, release notes, and changes across all versions, please refer to `CHANGELOG.md` in the project root.

---

*This document was generated based on the enhanced project information provided during the /init command execution.*
