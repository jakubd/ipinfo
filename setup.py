from setuptools import setup

setup(
    name="ipinfo",
    packages=["ipinfo"],
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'ipinfo=ipinfo.scripts.ipinfo_cli:stub',
        ],
    },
    include_package_data=True,
    install_requires=[
        "geoip2",
        "IPy",
        "dnspython",
        "PyYAML",
        "requests"
    ],
    tests_require=[
        "pytest"
    ]
)
