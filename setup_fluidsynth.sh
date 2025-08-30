#!/bin/bash

# FluidSynth Setup Script for MIDI MCP Server
# This script sets up FluidSynth with a high-quality SoundFont for multi-channel MIDI playback

echo "🎵 Setting up FluidSynth for MIDI MCP Server..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is required. Install it from https://brew.sh/"
    exit 1
fi

# Install FluidSynth
echo "📦 Installing FluidSynth..."
brew install fluidsynth

# Create soundfonts directory
echo "📁 Creating soundfonts directory..."
mkdir -p ~/soundfonts

# Download GeneralUser GS SoundFont if it doesn't exist
if [ ! -f ~/soundfonts/GeneralUser_GS.sf2 ]; then
    echo "🎼 Downloading GeneralUser GS SoundFont (30MB)..."
    curl -L -o ~/soundfonts/GeneralUser_GS.sf2 \
        "https://musical-artifacts.com/artifacts/1176/GeneralUser_GS_v1.471.sf2"
    echo "✅ SoundFont downloaded successfully!"
else
    echo "✅ SoundFont already exists!"
fi

echo ""
echo "🎉 Setup complete! To start FluidSynth, run:"
echo ""
echo "  fluidsynth -a coreaudio -g 0.5 ~/soundfonts/GeneralUser_GS.sf2"
echo ""
echo "Then test with:"
echo "  python demo_phase_2_mcp.py"
echo ""
echo "🎵 Enjoy high-quality multi-channel MIDI playback!"
