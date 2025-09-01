#!/usr/bin/env python3
"""Test the LibraryIntegration singleton pattern."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from midi_mcp.genres.library_integration import LibraryIntegration, get_library_integration


def test_singleton():
    """Test that LibraryIntegration is indeed a singleton."""

    print("Testing LibraryIntegration singleton pattern...")

    # Create multiple instances
    lib1 = LibraryIntegration()
    lib2 = LibraryIntegration()
    lib3 = get_library_integration()

    # Check they are the same object
    print(f"lib1 id: {id(lib1)}")
    print(f"lib2 id: {id(lib2)}")
    print(f"lib3 id: {id(lib3)}")

    assert lib1 is lib2, "lib1 and lib2 should be the same object"
    assert lib2 is lib3, "lib2 and lib3 should be the same object"
    assert lib1 is lib3, "lib1 and lib3 should be the same object"

    print("✓ All instances are the same object (singleton working)")

    # Check that libraries are available
    available = lib1.get_available_libraries()
    print(f"Available libraries: {available}")

    print("✓ Singleton pattern test passed!")


if __name__ == "__main__":
    test_singleton()
