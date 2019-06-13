'''Provides less-like edit functions for invoking the user's editor'''

import os
import subprocess


def edit(filename):
    '''edit(filename) -> return code

    Edit a file. cf. editor in this module
    '''
    cmd = [editor(), filename]
    return subprocess.run(cmd).returncode


def editor():
    '''editor() -> str

    In the same way as ``less`` and many other programs, it tries the
    environment variables VISUAL and EDITOR (in that order) before defaulting
    to vi.
    '''
    defaults = ['vi']
    env_vars = [
            'VISUAL',
            'EDITOR'
            ]
    editors = [
            ed
            for ed in map(
                lambda e: os.environ.get(e),
                env_vars)
            if ed is not None
            ] + defaults
    assert len(editors) > 0, "No editors found"
    return editors[0]
