from setup import version
import subprocess

branch = subprocess.check_output(['git', 'branch']).decode('utf-8').strip()

if branch.endswith('master'):
    tag_version = 'v{}'.format(version)
    tags = subprocess.check_output(['git', 'tag']).decode('utf-8').split()
    print(tags)
    if tag_version not in tags:
        with open('RELEASE_NOTES.md') as fp:
            notes = fp.read()
        subprocess.check_output(['git', 'tag', '-a', tag_version, '-m', notes])
        subprocess.call(['python', 'setup.py', 'sdist'])
        subprocess.call(['twine', 'check', 'dist/*'])
        subprocess.call(['twine', 'upload', 'dist/*{}.tar.gz'.format(version)])
    else:
        print('version already tagged')
else:
    print('only master branch can be tagged')
