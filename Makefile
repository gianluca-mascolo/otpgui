PKGVER:=$(GIT_TAG)
arch-clean:
	find archbuild -type f ! -path '*.gitkeep' -exec rm -f '{}' ';'
	docker-compose down
arch-pkg:
	docker-compose run --rm archpy /home/testuser/archpkg/create-pkg.sh $(PKGVER)
arch-install:
	docker-compose run --rm archpy /home/testuser/archpkg/install-pkg.sh $(PKGVER)