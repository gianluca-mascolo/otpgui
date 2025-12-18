PKGVER:=$(GIT_TAG)
fmt:
	poetry run black .
	poetry run isort .
	poetry run flake8
arch-clean:
	rm -rf build/arch/artifacts/pkg
	rm -rf build/arch/artifacts/src
	rm -rf build/arch/artifacts/otpgui*
	rm -f build/arch/artifacts/*
	rm -f build/arch/artifacts/.SRCINFO
	docker compose down
arch-pkg:
	docker compose run --rm archpy /home/testuser/scripts/create-pkg.sh $(PKGVER)
arch-install:
	docker compose run --rm archpy /home/testuser/scripts/install-pkg.sh $(PKGVER)
python-clean:
	rm -f dist/otpgui*
	rm -f build/python/artifacts/otpgui*
python-build:
	./build/python/scripts/build.sh $(PKGVER)
deb-clean:
	rm -rf build/deb/artifacts/otpgui*
	rm -f build/deb/artifacts/python3-otpgui*
deb-pkg:
	docker compose run --rm ubuntupy /home/testuser/scripts/create-pkg.sh $(PKGVER)
deb-install:
	docker compose run --rm ubuntupy /home/testuser/scripts/install-pkg.sh $(PKGVER)
python: python-clean python-build
deb: deb-clean deb-pkg deb-install
arch: arch-clean arch-pkg arch-install
