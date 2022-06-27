PKGVER:=$(GIT_TAG)
arch-clean:
	rm -rf archbuild/pkg
	rm -rf archbuild/src
	rm -rf archbuild/otpgui*
	rm -f archbuild/*
	rm -f archbuild/.SRCINFO
	docker-compose down
arch-pkg:
	docker-compose run --rm archpy /home/testuser/archpkg/create-pkg.sh $(PKGVER)
arch-install:
	docker-compose run --rm archpy /home/testuser/archpkg/install-pkg.sh $(PKGVER)
python-clean:
	rm -f dist/otpgui*
	rm -f build/python/artifacts/otpgui*
python-build:
	./build/python/scripts/build.sh $(PKGVER)
deb-clean:
	rm -rf build/deb/artifacts/otpgui*
	rm -f build/deb/artifacts/python3-otpgui*
deb-pkg:
	docker-compose run --rm ubuntupy /home/testuser/scripts/create-pkg.sh $(PKGVER)
deb-install:
	docker-compose run --rm ubuntupy /home/testuser/scripts/install-pkg.sh $(PKGVER)
