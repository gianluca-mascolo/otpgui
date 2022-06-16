PKGVER:=$(GIT_TAG)
arch-clean:
	rm -rf archbuild/pkg
	rm -rf archbuild/src
	rm -rf archbuild/otpgui*
	rm -f archbuild/*
	docker-compose down
arch-pkg:
	docker-compose run --rm archpy /home/testuser/archpkg/create-pkg.sh $(PKGVER)
arch-install:
	docker-compose run --rm archpy /home/testuser/archpkg/install-pkg.sh $(PKGVER)
