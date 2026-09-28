from pathlib import Path


def test_dockerfile_exists_and_exposes_port():
    dockerfile = Path("Dockerfile")
    assert dockerfile.exists()
    content = dockerfile.read_text()
    assert "EXPOSE 8000" in content
    assert "uvicorn" in content.lower()


def test_readme_has_quickstart_steps():
    readme = Path("README.md").read_text()
    assert "docker compose up -d" in readme
    assert "uvicorn" in readme.lower()
