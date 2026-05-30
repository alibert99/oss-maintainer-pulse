from setuptools import find_packages, setup


setup(
    name="oss-maintainer-pulse",
    version="0.1.1",
    description="Offline-first GitHub issue and pull request health reports for open-source maintainers.",
    url="https://github.com/alibert99/oss-maintainer-pulse",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={"dev": ["pytest>=8", "ruff>=0.5"]},
    entry_points={"console_scripts": ["maintainer-pulse=maintainer_pulse.cli:main"]},
)
