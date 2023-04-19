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
        --configure)
            CONFIGURE=1
            shift
            ;;
        --build)
            BUILD=1
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
if [ -n "$HELP" ] || [ -z "$1" ] || [ -z "$GENERATE$CONFIGURE$BUILD" ]; then
    cat <<EOF
Usage: $0 [--generate] [--configure] [--build] [-h/--help] <fonts...>

Arguments (one of these must be used):
    --generate          Generates the assets used in the font, not needed
                        unless generator script is modified
    --configure         Applies the changes to fontforge project
    --build             Builds the font files, format depends on the font

Optional arguments:
    --ci                Packages the fonts, used for the CI builds
    -h/--help           Shows this message

EOF
    exit
fi

fonts=$*

for font in $fonts; do
    if [ -n "$GENERATE" ]; then
        # this cannot be run with the fontforge python
        python "$FONTS_DIR/$font/generator.py"
    fi

    if [ -n "$CONFIGURE" ]; then
        # using module to specify what to do as passing arguments via fontforge
        # is really finnicky
        fontforge -quiet -script -m "$FONTS_DIR.$font.configure"
    fi

    if [ -n "$BUILD" ]; then
        # fonts should build by default when ran as package
        fontforge -quiet -script -m "$FONTS_DIR.$font"
    fi

    if [ -n "$CI" ]; then
        echo "CI build is not yet implemented"
        exit 1
    fi
done

