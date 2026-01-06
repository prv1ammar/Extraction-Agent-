import langchain
import pkgutil

print("Exploring langchain package structure...")
print(f"Langchain version: {langchain.__version__}")

# List all modules in langchain
modules = []
for _, name, _ in pkgutil.iter_modules(langchain.__path__):
    modules.append(name)

print("\nAvailable modules in langchain:")
for m in sorted(modules):
    print(f"  - {m}")

# Check for agent-related modules
print("\nAgent-related modules:")
agent_modules = [m for m in modules if 'agent' in m.lower()]
for m in sorted(agent_modules):
    print(f"  - {m}")

# Try to find AgentExecutor
print("\nSearching for AgentExecutor...")
try:
    # Check if it's directly importable
    from langchain import AgentExecutor
    print("Found: from langchain import AgentExecutor")
except ImportError:
    pass

# Check common locations
import importlib
possible_locations = [
    'langchain.agents.AgentExecutor',
    'langchain.agents.agent_executor.AgentExecutor',
    'langchain.agents.executor.AgentExecutor',
    'langchain.agents.agent.AgentExecutor',
    'langchain.chains.AgentExecutor',
    'langchain.schema.AgentExecutor',
]

for location in possible_locations:
    try:
        module_path, class_name = location.rsplit('.', 1)
        module = importlib.import_module(module_path)
        if hasattr(module, class_name):
            print(f"Found: {location}")
            break
    except (ImportError, AttributeError):
        continue
else:
    print("AgentExecutor not found in common locations")

# Check what's in langchain.agents
print("\nContents of langchain.agents:")
import langchain.agents
for attr in dir(langchain.agents):
    if not attr.startswith('_'):
        print(f"  - {attr}")
