#!/usr/bin/env bash
#
# build.sh

set -e

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

# directory where the fonts are located
FONTS_DIR=fonts

POSITIONAL_ARGS=()

while [ $# -gt 0 ]; do
    case $1 in
        --generate)
            GENERATE=1
            shift
            ;;
        --all)
            ALL=1
            shift
            ;;
        --package)
            PACKAGE=1
            shift
            ;;
        -h|--help)
            HELP=1
            shift
            ;;
        -*)
            echo "Unknown option $1"
            exit 1
            ;;
        *)
            # save positional arg
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# find all projects automatically
if [[ -n "$ALL" ]]; then
    # clear previous ones as they are useless
    POSITIONAL_ARGS=()

    for i in "$FONTS_DIR"/*/; do
        # filter only python packages
        if [[ -f "$i/__init__.py" ]]; then
            POSITIONAL_ARGS+=("$(basename "$i")")
        fi
    done
fi

# restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

# print help if no args, or if no command is supplied
if [ -n "$HELP" ] || [ -z "$1" ]; then
    cat <<EOF
Usage: $0 [<arguments...>] <fonts...>

Optional arguments:
    --all                   Builds all fonts, any positional argument is ignored
    --generate              Generates the assets used in the font, not needed
                            unless generator script is modified
    --package               Package the fonts
    --help                  Shows this message

EOF
    exit
fi

# make sure dir exists
mkdir -p ./build

# remove all the old fonts
rm -f ./build/*

# show fontforge version in log
echo -n "INFO: "
fontforge -quiet -version | head -n 1

for font in "$@"; do
    if [ -n "$GENERATE" ]; then
        echo "INFO: Generating assets for $font"

        # this cannot be run with the fontforge python
        python3 "$FONTS_DIR/$font/generator.py"
    fi

    # the module is responsible for building itself
    fontforge -quiet -script -m "$FONTS_DIR.$font"

    if [ -n "$PACKAGE" ]; then
        echo "INFO: Packaging the fonts"

        for i in "$@"; do
            7za a "Compacity${i^}.zip" ./build/Compacity"${i^}"* >/dev/null
        done

        # a complete package with all fonts for the CI
        7za a CompacityFonts.zip ./build/* >/dev/null
    fi
done

