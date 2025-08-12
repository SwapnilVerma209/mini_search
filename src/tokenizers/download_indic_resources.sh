#!/bin/sh
#
# Downloads Anoop Kunchukuttan's Indic NLP Resources if it is not already
# present, updates them otherwise.

if [ $# -ne 1 ]; then
    echo "Usage: $0 <tokenizers_path>" >&2;
    exit 1;
fi;

tokenizers_path=$1;
indic_resources_dir="indic_nlp_resources";
indic_resources_url="https://github.com/anoopkunchukuttan/indic_nlp_resources.git";

cd "$tokenizers_path";
if [ -d "$indic_resources_dir" ]; then
    cd "$indic_resources_dir";
    git pull;
else
    git clone "$indic_resources_url";
    cd "$indic_resources_dir";
fi;