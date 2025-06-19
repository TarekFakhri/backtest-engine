from setuptools import setup, find_packages

setup(
    name="backtest_engine",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "pytest",
        "yfinance"
    ],
    python_requires=">=3.8",
)
