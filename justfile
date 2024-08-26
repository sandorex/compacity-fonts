FONTS_DIR_ABS := join(justfile_directory(), 'fonts')
BUILD_DIR := join(justfile_directory(), 'build')
PACKAGE_DIR := join(justfile_directory(), 'package')
VENV_DIR := join(justfile_directory(), 'venv')
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

# create venv if it does not exist
_venv:
    #!/usr/bin/env bash
    if [[ ! -d "{{ VENV_DIR }}" ]]; then
        echo Creating python virtualenv
        python3 -m venv "{{ VENV_DIR }}"

        # TODO this should probably be a requirements.txt file
        # install generator script dependency
        source "{{ VENV_DIR }}"/bin/activate
        pip install drawsvg
    fi

# build assets for fonts, required only when generator.py script was modified
assets *target: _venv
    #!/usr/bin/env bash
    set -euo pipefail

    FONTS="$(just --justfile {{ justfile() }} _list "{{ target }}" | xargs)"

    source "{{ VENV_DIR }}"/bin/activate

    for i in $FONTS; do
        if [[ -f "{{ FONTS_DIR_ABS }}/$i"/generator.py ]]; then
            echo "Generating assets for '$i'"
            python3 "{{ FONTS_DIR_ABS }}/$i/generator.py"
        fi
    done

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

    # run build module
    for i in $FONTS; do
        echo "Building font '$i'"
        "{{ FONTFORGE_EXE }}" -quiet -lang=py -script "{{ FONTS_DIR_ABS }}/$i/build.py"
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

    # package each font
    for i in $FONTS; do
        echo "Packaging font $i"
        7za a "Compacity${i^}.zip" "{{ BUILD_DIR }}/Compacity${i^}"* >/dev/null
    done

    # package all the fonts for the CI
    7za a CompacityFonts.zip "{{ BUILD_DIR }}"/* >/dev/null

