setlocal
SET tokenizers_path=%1
SET indic_resources_dir="indic_nlp_resources"
SET indic_resources_url="https://github.com/anoopkunchukuttan/indic_nlp_resources.git"

cd %tokenizers_path%
if exists %indic_resources_dir% (
    cd %indic_resources_dir%
    git pull
) else (
    git clone %indic_resources_url%
    cd %indic_resources_dir%
)
endlocal