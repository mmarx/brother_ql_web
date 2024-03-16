from setuptools import setup, find_namespace_packages
from pathlib import Path


ROOT_DIRECTORY = Path(__file__).parent.resolve()


setup(
    name="brother_ql_web",
    description="Simple label designer API and web API for Brother QL label printers",
    version="0.2.1",
    license="GPL-3.0-only",
    long_description=(ROOT_DIRECTORY / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Philipp Klaus (initial), FriedrichFröbel",
    url="https://github.com/FriedrichFroebel/brother_ql_web/",
    packages=find_namespace_packages(include=["brother_ql_web", "brother_ql_web.*"]),
    include_package_data=True,
    python_requires=">=3.8, <4",
    install_requires=[
        "brother_ql",
        "bottle",
        "jinja2",
        "Pillow>=8",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "pep8-naming",
            "flake8-bugbear",
            "requests",
            'importlib-resources; python_version < "3.9"',
        ],
        "mypy": [
            "mypy",
            "types-Pillow",
            "types-requests",
        ],
    },
    entry_points={
        "console_scripts": [
            "brother_ql_web=brother_ql_web.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Bottle",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Multimedia :: Graphics",
    ],
)
