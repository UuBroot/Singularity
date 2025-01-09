OS=$(uname)
if [ "$OS" = "Darwin" ]; then
    echo "Running on macOS"
    nuitka --follow-imports --standalone --macos-create-app-bundle --output-dir=build --include-plugin-directory=system --plugin-enable=pyside6 --assume-yes-for-downloads singularity-qt.py
elif [ "$OS" = "Linux" ]; then
    echo "Running on Linux"
    nuitka --follow-imports --standalone --onefile --output-dir=build --include-plugin-directory=system --plugin-enable=pyside6 singularity-qt.py
else
    echo "Unsupported OS: $OS"
    exit 1
fi