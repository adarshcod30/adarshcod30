# The profile builds itself from the GitHub API. Claiming reproducibility on
# every project and then hand-maintaining this page would be a poor look.
PY ?= python3

.PHONY: all refresh assets index clean help

all: assets index  ## redraw everything from the cached snapshot

refresh:  ## pull the current repository list from the GitHub API (needs gh)
	cd tools && $(PY) fetch.py

assets:  ## redraw the banner, the timeline and the avatars
	cd tools && $(PY) banner.py && $(PY) timeline.py && $(PY) org_avatars.py

index:  ## rewrite PROJECTS.md from the snapshot
	cd tools && $(PY) projects_md.py

clean:  ## remove generated images
	rm -f assets/*.png

help:  ## list the targets
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/' | expand -t22
