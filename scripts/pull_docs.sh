readonly languages=(
    'c'
    'cpp'
    'git'
    'python@3.6'
)

start_dir="$PWD"

cd /tmp
git clone https://github.com/Thibaut/devdocs
cd devdocs

command -v bundler >/dev/null 2>&1 || gem install bundler
bundle install || echo "Failed to install dependencies." || exit 1

bundle exec thor docs:download "${languages[@]}"
mv public/docs/* "$start_dir/data/"

cd "$start_dir"
