#!/usr/bin/env python3
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))

def find_credential_ids(obj, path=""):
    issues = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'credentials' and isinstance(v, dict) and v:
                issues.append(path + '/credentials')
            else:
                issues.extend(find_credential_ids(v, path + '/' + k))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            issues.extend(find_credential_ids(item, f"{path}[{idx}]"))
    return issues

# Regex patterns for common resource IDs
patterns = {
    'google_sheet': re.compile(r'docs.google.com/spreadsheets/d/([a-zA-Z0-9-_]+)'),
    'drive_folder': re.compile(r'drive.google.com/drive/folders/([a-zA-Z0-9-_]+)'),
    'slack_channel': re.compile(r'"value"\s*:\s*"C[0-9A-Z]{8,}"'),
    'pinecone': re.compile(r'pinecone', re.I),
}


def scan_file(path):
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except Exception:
            return {'error': 'invalid_json'}

    issues = find_credential_ids(data)
    found = []
    text = json.dumps(data)
    for name, pat in patterns.items():
        for m in pat.finditer(text):
            found.append((name, m.group(0)))
    return {'issues': issues, 'found': found}


def main():
    results = {}
    for root, _, files in os.walk(REPO_ROOT):
        for fn in files:
            if fn.endswith('.json'):
                fp = os.path.join(root, fn)
                res = scan_file(fp)
                results[fp] = res

    problems = {k:v for k,v in results.items() if v.get('issues') or v.get('found')}
    if not problems:
        print('No issues found. Workflows appear sanitized.')
        return 0

    print('Potential issues found:')
    for f, r in problems.items():
        print('\nFile:', f)
        if r.get('error'):
            print('  - Could not parse JSON')
            continue
        for p in r.get('issues', []):
            print('  - Credential block found at', p)
        for typ, val in r.get('found', []):
            print('  - Resource match:', typ, '→', val)
    return 1

if __name__ == '__main__':
    exit(main())
