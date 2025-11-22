#!/usr/bin/env python3
"""
Test script to verify Python environment for VSCode Colab testing.

This script can be run directly from VSCode terminal or as a regular Python script.
"""

import sys
import platform


def test_environment():
    """Test basic Python environment setup."""
    print("=" * 50)
    print("VSCode Colab Test Environment Check")
    print("=" * 50)
    
    # Test 1: Python version
    print(f"\n✓ Python version: {sys.version}")
    print(f"✓ Python executable: {sys.executable}")
    
    # Test 2: Platform info
    print(f"\n✓ Platform: {platform.platform()}")
    print(f"✓ System: {platform.system()}")
    print(f"✓ Machine: {platform.machine()}")
    
    # Test 3: Check for common libraries
    libraries = ['numpy', 'pandas', 'matplotlib']
    print("\nChecking for common data science libraries:")
    
    for lib in libraries:
        try:
            __import__(lib)
            print(f"  ✓ {lib} - installed")
        except ImportError:
            print(f"  ✗ {lib} - not installed (optional)")
    
    print("\n" + "=" * 50)
    print("Environment check complete!")
    print("=" * 50)


if __name__ == "__main__":
    test_environment()
