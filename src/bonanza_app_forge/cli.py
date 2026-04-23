"""Bonanza App Forge CLI — Visual idea → working app."""

import os
import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@click.group()
@click.version_option("0.1.0", prog_name="bonanza-app-forge")
def main():
    """🔨 Bonanza App Forge — Visual idea → working app."""
    pass


@main.command()
@click.argument("prompt", required=False)
@click.option("--from-image", "image_path", help="Use existing image instead of generating mockup")
@click.option("--provider", type=click.Choice(["openai", "claude", "ollama"]), default="openai", help="AI provider for mockup generation")
@click.option("--coder", type=click.Choice(["claude", "openai", "ollama"]), default="claude", help="AI provider for code generation")
@click.option("--output", "-o", default="./forge-output", help="Output directory")
@click.option("--name", "-n", help="App name (auto-generated if not set)")
@click.option("--build/--no-build", default=True, help="Build the project after generating")
@click.option("--deploy", type=click.Choice(["tiiny", "local", "none"]), default="none", help="Deploy target")
@click.option("--domain", help="Custom domain for deployment")
@click.option("--local", is_flag=True, help="Use local Ollama for everything")
def app(
    prompt: str | None,
    image_path: str | None,
    provider: str,
    coder: str,
    output: str,
    name: str | None,
    build: bool,
    deploy: str,
    domain: str | None,
    local: bool,
):
    """Generate a working app from a visual idea."""

    if local:
        provider = "ollama"
        coder = "ollama"

    if not prompt and not image_path:
        console.print("[red]Error: Provide a prompt or use --from-image[/red]")
        console.print("Example: bonanza-forge app 'SaaS dashboard with charts'")
        sys.exit(1)

    if not name and prompt:
        # Generate app name from prompt
        words = prompt.lower().split()[:3]
        name = "-".join(words).replace(" ", "-")

    console.print(Panel(
        f"[bold]🔨 Bonanza App Forge[/bold]\n\n"
        f"Prompt: {prompt or '(from image)'}\n"
        f"Mockup: {provider}\n"
        f"Coder: {coder}\n"
        f"Name: {name}",
        title="App Forge",
        border_style="green",
    ))

    mockup_path = image_path

    # Step 1: Generate mockup
    if not mockup_path:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("🎨 Generating mockup...", total=None)
            try:
                from .mockup import generate_mockup_openai, generate_mockup_ollama
                mockup_dir = Path(output) / name / "mockup"
                mockup_dir.mkdir(parents=True, exist_ok=True)
                mockup_path = str(mockup_dir / "mockup.png")

                if provider == "openai":
                    generate_mockup_openai(prompt, mockup_path)
                elif provider == "ollama":
                    generate_mockup_ollama(prompt, mockup_path)
                else:
                    generate_mockup_openai(prompt, mockup_path)

                progress.update(task, completed=True)
                console.print(f"[green]✅ Mockup saved: {mockup_path}[/green]")
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]❌ Mockup generation failed: {e}[/red]")
                sys.exit(1)

    # Step 2: Generate code from mockup
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("💻 Generating code from mockup...", total=None)
        try:
            from .codegen import generate_code_claude, generate_code_openai, generate_code_ollama

            if coder == "claude":
                code = generate_code_claude(mockup_path, prompt or "Match this design")
            elif coder == "openai":
                code = generate_code_openai(mockup_path, prompt or "Match this design")
            elif coder == "ollama":
                code = generate_code_ollama(mockup_path, prompt or "Match this design")
            else:
                code = generate_code_claude(mockup_path, prompt or "Match this design")

            progress.update(task, completed=True)
            console.print("[green]✅ Code generated[/green]")
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"[red]❌ Code generation failed: {e}[/red]")
            sys.exit(1)

    # Step 3: Create project
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("📁 Creating project...", total=None)
        try:
            from .builder import create_project, build_project, deploy_tiiny

            project_dir = create_project(name, code, output)
            progress.update(task, completed=True)
            console.print(f"[green]✅ Project created: {project_dir}[/green]")
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"[red]❌ Project creation failed: {e}[/red]")
            sys.exit(1)

    # Step 4: Build
    if build:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("🏗️ Building project...", total=None)
            success = build_project(project_dir)
            progress.update(task, completed=True)
            if success:
                console.print(f"[green]✅ Build complete: {project_dir}/out/[/green]")
            else:
                console.print("[yellow]⚠️ Build failed — you can build manually with: cd {project_dir} && npm run build[/yellow]")

    # Step 5: Deploy
    if deploy == "tiiny":
        tiiny_key = os.environ.get("TIINY_API_KEY")
        domain = domain or f"{name}.tiiny.site"
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task(f"🚀 Deploying to {domain}...", total=None)
            if tiiny_key:
                success = deploy_tiiny(project_dir, domain, tiiny_key)
                progress.update(task, completed=True)
                if success:
                    console.print(Panel(f"[bold green]🚀 Deployed![/bold green]\n\nURL: https://{domain}", border_style="green"))
                else:
                    console.print("[red]❌ Deploy failed[/red]")
            else:
                progress.update(task, completed=True)
                console.print("[yellow]⚠️ TIINY_API_KEY not set. Deploy manually or set the env var.[/yellow]")

    console.print(Panel(
        f"[bold]🔨 App Forge Complete[/bold]\n\n"
        f"Project: {project_dir}\n"
        f"Mockup: {mockup_path}\n"
        f"Preview: cd {project_dir} && npm run dev",
        border_style="green",
    ))


@main.command()
@click.option("--local", is_flag=True, help="Configure for local Ollama")
def config(local: bool):
    """Configure Bonanza App Forge."""
    console.print("[bold]🔨 Bonanza App Forge Configuration[/bold]\n")

    if local:
        console.print("[green]✅ Configured for local mode (Ollama)[/green]")
    else:
        has_openai = bool(os.environ.get("OPENAI_API_KEY"))
        has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))

        console.print(f"OpenAI API Key: {'✅ Set' if has_openai else '❌ Not set'}")
        console.print(f"Anthropic API Key: {'✅ Set' if has_anthropic else '❌ Not set'}")

        if not has_openai and not has_anthropic:
            console.print("\n[yellow]Set at least one API key:[/yellow]")
            console.print("  export OPENAI_API_KEY=sk-...")
            console.print("  export ANTHROPIC_API_KEY=sk-...")


if __name__ == "__main__":
    main()