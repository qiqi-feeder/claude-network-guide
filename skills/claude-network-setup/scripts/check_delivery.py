"""Check local documentation links and obvious secret artifacts, without network calls."""
import argparse
from pathlib import Path
import re
from urllib.parse import unquote

EXCLUDED = {'.git', '.venv', '__pycache__', 'private', 'outputs', 'backups', 'reports'}


def check(root):
    root = Path(root).resolve()
    errors = []
    for file in root.rglob('*'):
        if not file.is_file() or any(part in EXCLUDED for part in file.relative_to(root).parts):
            continue
        if file.suffix in {'.pem', '.key', '.pfx', '.p12'}:
            errors.append(str(file.relative_to(root)) + ': private key artifact')
            continue
        if file.suffix.lower() not in {'.md', '.py', '.json', '.yaml', '.yml', '.ps1', '.txt', '.conf', '.list'}:
            continue
        text = file.read_text(encoding='utf-8-sig')
        if re.search(r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----', text):
            errors.append(str(file.relative_to(root)) + ': private key content')
        if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}', text):
            errors.append(str(file.relative_to(root)) + ': possible GitHub token')
        if file.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                target = target.strip('<>').split('#', 1)[0]
                if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                    continue
                if not (file.parent / unquote(target)).exists():
                    errors.append(str(file.relative_to(root)) + ': missing link ' + target)
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    findings = check(parser.parse_args().root)
    for finding in findings:
        print(finding)
    print('FAILED' if findings else 'Local links and obvious secret-artifact checks passed. Manual review is still required.')
    raise SystemExit(bool(findings))
