from setuptools import setup, find_packages

setup(
    name="todo-app",
    version="0.1.0",
    description="Phase I: In-Memory Python Console Todo App",
    author="Spec-Driven Development",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # No external dependencies for this phase - using only built-in Python libraries
    ],
    entry_points={
        'console_scripts': [
            'todo=cli.main:main',
        ],
    },
    python_requires='>=3.13',
)