from setuptools import setup

setup(
	name="pygbase-engine",
	version="0.0.1",
	description="A basic engine for Pygame",
	url="https://github.com/Yu266426/pygbase",
	author="Yu266426",
	author_email="yu266426@gmail.com",
	license="MIT",
	packages=["pygbase", "pygbase.graphics", "pygbase.particles", "pygbase.ui", "pygbase.lighting"],
	install_requires=["pygame-ce>=2.3.0"]
)
