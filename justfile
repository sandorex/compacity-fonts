FONTS_DIR_ABS := join(justfile_directory(), 'fonts')
BUILD_DIR := join(justfile_directory(), 'build')
PACKAGE_DIR := join(justfile_directory(), 'package')
FONTFORGE_EXE := env_var_or_default('FONTFORGE_EXE', 'fontforge')

_default:
    @just --justfile {{ justfile() }} --list

# list all font names
_list *target:
    #!/usr/bin/env bash
    set -euo pipefail

    # just pass target to this recipe and it will either find all fonts or return target
    if [[ -z "{{ target }}" ]]; then
        for i in {{ FONTS_DIR_ABS }}/*; do
            if [[ -d "$i" && -f "$i"/README.md ]]; then
                echo "$(basename "$i")"
            fi
        done
    else
        echo "{{ target }}"
    fi

# build the fonts
build *target:
    #!/usr/bin/env bash
    set -euo pipefail

    # clean build dir
    mkdir -p "{{ BUILD_DIR }}"
    rm -f "{{ BUILD_DIR }}/*"

    FONTS="$(just --justfile {{ justfile() }} _list "{{ target }}" | xargs)"

    # print fontforge version for log
    "{{ FONTFORGE_EXE }}" -quiet -version | head -n 1

    # go to root of the project
    cd "{{ justfile_directory() }}"

    # run build module for each font
    for i in $FONTS; do
        "{{ FONTFORGE_EXE }}" -quiet -lang=py -script -m "fonts.$i.build"
    done

# package the fonts in zip archives
package *target: (build target)
    #!/usr/bin/env bash
    set -euo pipefail

    # clean build dir
    mkdir -p "{{ PACKAGE_DIR }}"
    rm -f "{{PACKAGE_DIR }}"/*

    FONTS="$(just --justfile {{ justfile() }} _list "{{ target }}" | xargs)"

    # move to package build dir
    cd "{{ PACKAGE_DIR }}"

    if command -v 7za &>/dev/null; then
        _7ZIP=7za
    else
        _7ZIP=7z
    fi

    # package each font
    for i in $FONTS; do
        echo "Packaging font $i"
        "$_7ZIP" a "Compacity${i^}.zip" "{{ BUILD_DIR }}/Compacity${i^}"* >/dev/null
    done

    # package all the fonts for the CI
    "$_7ZIP" a CompacityFonts.zip "{{ BUILD_DIR }}"/* >/dev/null

