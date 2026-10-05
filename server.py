from fastmcp import FastMCP

mcp = FastMCP("hello-world")


@mcp.tool
def hello(name: str = "world") -> str:
    """Return a friendly greeting for the given name."""
    return f"Hello, {name}!"


@mcp.resource("greeting://hello")
def greeting() -> str:
    """A static hello world greeting."""
    return "Hello, world!"


if __name__ == "__main__":
    mcp.run()
