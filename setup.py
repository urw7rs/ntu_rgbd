import setuptools


def main():
    setuptools.setup(
        name="ntu_rgbd",
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        version="0.0.1",
        description="NTU RGB+D Dataset helper library: download, extract and prepare dataset",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
        install_requires=[
            "numpy",
        ],
    )


if __name__ == "__main__":
    main()
