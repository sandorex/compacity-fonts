#!/usr/bin/env bash
#
# build.sh

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
        --ci)
            CI=1
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

# restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

# print help if no args, or if no command is supplied
if [ -n "$HELP" ] || [ -z "$1" ]; then
    cat <<EOF
Usage: $0 [--regenerate] [--ci] [-h/--help] <fonts...>

Optional arguments:
    --generate          Generates the assets used in the font, not needed
                        unless generator script is modified
    --ci                Packages the fonts, used for the CI builds
    -h/--help           Shows this message

EOF
    exit
fi

# show fontforge version in log
echo -n "INFO: "
fontforge -quiet -version | head -n 1

for font in "$@"; do
    if [ -n "$GENERATE" ]; then
        # this cannot be run with the fontforge python
        python3 "$FONTS_DIR/$font/generator.py"
    fi

    # the module is responsible for building itself
    fontforge -quiet -script -m "$FONTS_DIR.$font"

    if [ -n "$CI" ]; then
        for i in "$@"; do
            7za a "compacity-$i.7z" ./build/compacity-"$i"*
        done

        if [[ "$#" -gt 1 ]]; then
            7za a compacity-fonts.7z ./build/*
        fi
    fi
done

