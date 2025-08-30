#!/usr/bin/env python3
"""
Test script for MIDI device enumeration across platforms.

This script tests the new cross-platform MIDI device discovery implementation
to ensure it works on the current system.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from midi_mcp.config.settings import MidiConfig
from midi_mcp.midi.manager import MidiManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_device_discovery():
    """Test MIDI device discovery and basic operations."""
    print("🎵 Testing MIDI Device Discovery")
    print("=" * 50)
    
    # Create MIDI manager
    config = MidiConfig()
    midi_manager = MidiManager(config)
    
    try:
        # Test backend status
        print("\n📋 Backend Status:")
        backend_status = midi_manager.get_backend_status()
        for key, value in backend_status.items():
            print(f"  {key}: {value}")
        
        # Test device discovery
        print("\n🔍 Discovering MIDI devices...")
        devices = await midi_manager.discover_devices()
        
        if not devices:
            print("❌ No devices found")
            return
        
        print(f"\n✅ Found {len(devices)} MIDI devices:")
        for i, device in enumerate(devices, 1):
            print(f"  {i}. {device}")
        
        # Test connecting to first output device
        output_devices = [d for d in devices if d.is_output]
        if output_devices:
            print(f"\n🔌 Testing connection to: {output_devices[0].name}")
            try:
                device = await midi_manager.connect_device(output_devices[0].device_id)
                print("✅ Connection successful!")
                
                # Test sending a note
                print("🎹 Testing note playback...")
                await device.send_note_on(60, 100, 0)  # Middle C
                await asyncio.sleep(0.5)
                await device.send_note_off(60, 64, 0)
                print("✅ Note sent successfully!")
                
                # Disconnect
                await midi_manager.disconnect_device(output_devices[0].device_id)
                print("🔌 Disconnected successfully!")
                
            except Exception as e:
                print(f"❌ Connection/playback error: {e}")
        else:
            print("⚠️  No output devices available for testing")
        
        # Test latency stats
        print("\n📊 Latency Statistics:")
        stats = midi_manager.get_latency_stats()
        for operation, latency in stats.items():
            print(f"  {operation}: {latency:.4f}s")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        await midi_manager.cleanup()
        print("\n🧹 Cleanup completed")

def main():
    """Main test function."""
    print("🚀 Starting MIDI Device Discovery Test")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        sys.exit(1)
    
    # Run the test
    try:
        asyncio.run(test_device_discovery())
        print("\n✅ Test completed successfully!")
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
