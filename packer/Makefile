BUILDER_TYPES = vmware virtualbox
TEMPLATE_PATHS := $(wildcard template/*.json)
TEMPLATE_FILENAMES := $(notdir ${TEMPLATE_PATHS})
BOX_FILENAMES := $(TEMPLATE_FILENAMES:.json=.box)

vpath %.json template

.PHONY: list clean-output clean-packer-cache

list:
	@for builder in $(BUILDER_TYPES) ; do \
		for box_filename in $(BOX_FILENAMES) ; do \
			echo $$builder/$$box_filename ; \
		done ; \
	done

vmware/%.box: %.json
	cd $(dir $<); \
	rm -rf output-vmware; \
	mkdir -p ../vmware; \
	packer build -only=vmware $(notdir $<)

virtualbox/%.box: %.json
	cd $(dir $<); \
	rm -rf output-virtualbox; \
	mkdir -p ../virtualbox; \
	packer build -only=virtualbox $(notdir $<)

clean-output:
	@for builder in $(BUILDER_TYPES) ; do \
		if test -d template/output-$$builder ; then \
			echo Deleting template/output-$$builder ; \
			rm -rf template/output-$$builder ; \
		fi ; \
	done

clean-packer-cache:
	@if test -d template/packer_cache ; then \
		echo Deleting template/packer_cache ; \
		rm -rf template/packer_cache ; \
	fi ; \
