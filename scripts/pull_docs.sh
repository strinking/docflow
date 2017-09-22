readonly languages=(
    'c'
    'cpp'
    'git'
    'python@3.6'
)

start_dir="$PWD"

cd /tmp
cd devdocs && git pull || git clone https://github.com/Thibaut/devdocs && cd devdocs

command -v bundler >/dev/null 2>&1 || gem install bundler
bundle install || echo "Failed to install dependencies." || exit 1

bundle exec thor docs:download "${languages[@]}"
mv -f public/docs/* "$start_dir/data/"

cd "$start_dir"
echo "Got documentation. Converting to Markdown..."
pipenv run python scripts/convert.py
