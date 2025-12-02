#!/usr/bin/env python3
"""
Script to fix Python 3.13 dataclass compatibility issues in fairseq.
Converts mutable default values to use default_factory.
"""

import re
import os
import sys

def fix_file(filepath):
    """Fix dataclass mutable defaults in a single file."""
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    changes = []

    # Pattern 1: field_name: ConfigType = ConfigType()
    # Should become: field_name: ConfigType = field(default_factory=ConfigType)
    pattern1 = re.compile(
        r'^(\s+)(\w+):\s+(\w+Config)\s*=\s*\3\(\)$',
        re.MULTILINE
    )

    def replace1(match):
        indent, field_name, config_type = match.groups()
        changes.append(f"  {field_name}: {config_type} = {config_type}() -> field(default_factory={config_type})")
        return f'{indent}{field_name}: {config_type} = field(default_factory={config_type})'

    content = pattern1.sub(replace1, content)

    # Pattern 2: field_name: ConfigType = field(default=ConfigType())
    # Should become: field_name: ConfigType = field(default_factory=ConfigType)
    pattern2 = re.compile(
        r'field\(default=(\w+Config)\(\)\)',
        re.MULTILINE
    )

    def replace2(match):
        config_type = match.group(1)
        changes.append(f"  field(default={config_type}()) -> field(default_factory={config_type})")
        return f'field(default_factory={config_type})'

    content = pattern2.sub(replace2, content)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return changes

    return []

def main():
    fairseq_root = "/mnt/ExtraStorage/source/repos/ai_tools/dependencies/fairseq"

    # Files to fix based on our search
    files_to_fix = [
        "fairseq/models/transformer/transformer_config.py",
        "examples/data2vec/models/data2vec_text.py",
        "examples/wav2vec/unsupervised/w2vu_generate.py",
        "examples/wav2vec/unsupervised/tasks/unpaired_audio_text.py",
        "examples/data2vec/models/data2vec2.py",
        "examples/wav2vec/unsupervised/models/wav2vec_u.py",
        "examples/speech_recognition/new/infer.py",
    ]

    total_changes = 0
    for rel_path in files_to_fix:
        filepath = os.path.join(fairseq_root, rel_path)
        if os.path.exists(filepath):
            print(f"\nProcessing: {rel_path}")
            changes = fix_file(filepath)
            if changes:
                print(f"  Fixed {len(changes)} issue(s):")
                for change in changes:
                    print(change)
                total_changes += len(changes)
            else:
                print("  No changes needed")
        else:
            print(f"\nSkipping (not found): {rel_path}")

    print(f"\n{'='*60}")
    print(f"Total fixes applied: {total_changes}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
