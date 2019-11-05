from setuptools import setup

setup(
    name="ipinfo",
    packages=["ipinfo"],
    version="0.0.2",
    entry_points={
        'console_scripts': [
            'ipinfo=ipinfo.scripts.ipinfo_cli:stub',
            'ipinfodbupdate=ipinfo.scripts.ipinfo_db_update:stub'
        ],
    },
    include_package_data=True,
    install_requires=[
        "geoip2",
        "IPy",
        "dnspython",
        "PyYAML",
        "requests",
        "tabulate"
    ],
    tests_require=[
        "pytest"
    ]
)
