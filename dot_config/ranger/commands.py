# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)

# You can import any python module as needed.
import os

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import Command

# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!

# {{{ ### --- my_edit (my editor <FILE> --- ###
class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()   
# }}}

# {{{ ### --- fzf_rga_search_documents --- ###
class fzf_rga_documents_search(Command):
    """
    :fzf_rga_search_documents
    Search in PDFs, E-Books and Office documents in current directory.
    Allowed extensions: .epub, .odt, .docx, .fb2, .ipynb, .pdf.

    Usage: fzf_rga_search_documents <search string>
    """
    def execute(self):
        if self.arg(1):
            search_string = self.rest(1)
        else:
            self.fm.notify("Usage: fzf_rga_search_documents <search string>", bad=True)
            return

        import subprocess
        import os.path
        from ranger.container.file import File
        command="rga '%s' . --rga-adapters=pandoc,poppler | fzf +m | awk -F':' '{print $1}'" % search_string
        fzf = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.rstrip('\n'))
            self.fm.execute_file(File(fzf_file)) 
# }}}

# {{{ ### --- Toggle flat --- ###
class toggle_flat(Command):
    """
    :toggle_flat

    Flattens or unflattens the directory view.
    """

    def execute(self):
        if self.fm.thisdir.flat == 0:
            self.fm.thisdir.unload()
            self.fm.thisdir.flat = -1
            self.fm.thisdir.load_content()
        else:
            self.fm.thisdir.unload()
            self.fm.thisdir.flat = 0
            self.fm.thisdir.load_content()
# }}}

# {{{ ### --- Navigate remote hosts via sshfs --- ### (inactive!!! todo: resolve umount function)
# Use sshfs_mount to mount a host filesystem and sshfs_umount to unmount. The design is stolen from nnn file manager.

#import subprocess
#import os

#def show_error_in_console(msg, fm):
#    fm.notify(msg, bad=True)

#def navigate_path(fm, selected):
#    if not selected:
#        return

#    selected = os.path.abspath(selected)
#    if os.path.isdir(selected):
#        fm.cd(selected)
#    elif os.path.isfile(selected):
#        fm.select_file(selected)
#    else:
#        show_error_in_console(f"Neither directory nor file: {selected}", fm)
#        return

#def execute(cmd, input=None):
#    stdin = None
#    if input:
#        stdin = subprocess.PIPE

#    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin, text=True)
#    stdout, stderr = proc.communicate(input=input)

#    if proc.returncode != 0:
#        raise Exception(f"Bad process exit code: {proc.returncode}, stdout={stdout}, stderr={stderr}")

#    return stdout, stderr

#import re
#import curses

#import collections
#URL = collections.namedtuple("URL", ["user", "hostname", "path"])

#def parse_url(url):
#    if len(t := url.split(sep="@", maxsplit=1)) > 1:
#        user = t[0]
#        rest = t[1]
#    else:
#        user = None
#        rest = t[0]
#    if len(t := rest.rsplit(sep=":", maxsplit=1)) > 1:
#        hostname = t[0]
#        path = t[1]
#    else:
#        hostname = t[0]
#        path = None

#    return URL(user=user, hostname=hostname, path=path)

#def url2str(u :URL):
#    res = u.hostname
#    if u.user:
#        res = f"{u.user}@{res}"
#    path = u.path
#    if path is None:
#        path = ""

#    return f"{res}:{path}"

#def search_mount_path(mount_path):
#    stdout, _ = execute(["mount"])
#    return re.search(re.escape(mount_path)+r"\b", stdout)

#def hostname2mount_path(hostname):
#    mount_path = os.path.expanduser(f"~/.config/ranger/mounts/{hostname}")

#    # check whether it is already mounted
#    if search_mount_path(mount_path):
#        raise Exception(f"Already mounted: {mount_path}")

#    os.makedirs(mount_path, exist_ok=True)
#    return mount_path

#class sshfs_mount(Command):
#    def execute(self):
#        url = self.arg(1)
#        u = parse_url(url)

#        mount_path = hostname2mount_path(u.hostname)
#        cmd = ["sshfs", url2str(u), mount_path]

#        execute(cmd)

#        # before navigating we should load it otherwise we see
#        # "not accessible"
#        d = self.fm.get_directory(mount_path)
#        d.load()

#        navigate_path(self.fm, mount_path)

#    # options:
#    # - None
#    # - string: just one complete without iterating
#    # - list, tuple, generator: to iterate options around
#    def tab(self, tabnum):
#        u = parse_url(self.rest(1))

#        def path_options():
#            lst = []
#            for path in ["", "/"]:
#                lst.append(self.start(1) + url2str(u._replace(path=path)))

#            return lst

#        # autocomplete hostname
#        if u.path is None:
#            hostname = select_with_fzf(["fzf", "-q", u.hostname], compose_hostname_list(), self.fm)
#            #hostname = "ilya-thinkpad"

#            # after suspend/init we should manually show the cursor
#            # the same way console.open() does
#            try:
#                curses.curs_set(1)
#            except curses.error:
#                pass

#            if not hostname:
#                return None

#            u = u._replace(hostname=hostname)
#            return path_options()

#        # autocomplete path
#        return path_options()

#def umount(mount_path):
#    prefix = os.path.expanduser(f"~/.config/ranger/mounts/")
#    if not mount_path.startswith(prefix):
#        raise Exception(f"May umount only inside: {prefix}")

#    if not search_mount_path(mount_path):
#        raise Exception(f"Not mounted: {mount_path}")

#    cmd = ["diskutil", "unmount", "force", mount_path]
#    execute(cmd)

#    os.rmdir(mount_path)

#class sshfs_umount(Command):
#    def execute(self):
#        tab = self.fm.tabs[self.fm.current_tab]
#        mount_path = tab.thisfile.path
#        umount(mount_path)

#def compose_hostname_list():
#    # list of possible hostnames
#    # stolen from fzf, https://github.com/junegunn/fzf/blob/master/shell/completion.bash
#    stdout, _ = execute(["bash"], input='''
#command cat <(
#    command tail -n +1 ~/.ssh/config ~/.ssh/config.d/* /etc/ssh/ssh_config 2> /dev/null | command grep -i '^\s*host\(name\)\? ' | awk '{for (i = 2; i <= NF; i++) print $1 " " $i}' | command grep -v '[*?]') \
#        <(command grep -oE '^[[a-z0-9.,:-]+' ~/.ssh/known_hosts | tr ',' '\n' | tr -d '[' | awk '{ print $1 " " $1 }') \
#        <(command grep -v '^\s*\(#\|$\)' /etc/hosts | command grep -Fv '0.0.0.0') |
#        awk '{if (length($2) > 0) {print $2}}' | sort -u
#''')
#    return stdout
# }}}

# {{{ ### --- fzf_select --- ###
class fzf_select(Command):
    """
    :fzf_select
    Find a file using fzf.
    With a prefix argument to select only directories.

    See: https://github.com/junegunn/fzf
    """

    def execute(self):
        import subprocess
        import os
        from ranger.ext.get_executables import get_executables

        if 'fzf' not in get_executables():
            self.fm.notify('Could not find fzf in the PATH.', bad=True)
            return

        fd = None
        if 'fdfind' in get_executables():
            fd = 'fdfind'
        elif 'fd' in get_executables():
            fd = 'fd'

        if fd is not None:
            hidden = ('--hidden' if self.fm.settings.show_hidden else '')
            exclude = "--no-ignore-vcs --exclude '.git' --exclude '*.py[co]' --exclude '__pycache__'"
            only_directories = ('--type directory' if self.quantifier else '')
            fzf_default_command = '{} --follow {} {} {} --color=always'.format(
                fd, hidden, exclude, only_directories
            )
        else:
            hidden = ('-false' if self.fm.settings.show_hidden else r"-path '*/\.*' -prune")
            exclude = r"\( -name '\.git' -o -name '*.py[co]' -o -fstype 'dev' -o -fstype 'proc' \) -prune"
            only_directories = ('-type d' if self.quantifier else '')
            fzf_default_command = 'find -L . -mindepth 1 {} -o {} -o {} -print | cut -b3-'.format(
                hidden, exclude, only_directories
            )

        env = os.environ.copy()
        env['FZF_DEFAULT_COMMAND'] = fzf_default_command
        env['FZF_DEFAULT_OPTS'] = '--height=40% --layout=reverse --ansi --preview="{}"'.format('''
            (
                batcat --color=always {} ||
                bat --color=always {} ||
                cat {} ||
                tree -ahpCL 3 -I '.git' -I '*.py[co]' -I '__pycache__' {}
            ) 2>/dev/null | head -n 100
        ''')

        fzf = self.fm.execute_command('fzf --no-multi', env=env,
                                      universal_newlines=True, stdout=subprocess.PIPE)
        stdout, _ = fzf.communicate()
        if fzf.returncode == 0:
            selected = os.path.abspath(stdout.strip())
            if os.path.isdir(selected):
                self.fm.cd(selected)
            else:
                self.fm.select_file(selected)
# }}}

# {{{ ### --- Search with fd --- ###
from collections import deque

class fd_search(Command):
    """
    :fd_search [-d<depth>] <query>
    Executes "fd -d<depth> <query>" in the current directory and focuses the
    first match. <depth> defaults to 1, i.e. only the contents of the current
    directory.

    See https://github.com/sharkdp/fd
    """

    SEARCH_RESULTS = deque()

    def execute(self):
        import re
        import subprocess
        from ranger.ext.get_executables import get_executables

        self.SEARCH_RESULTS.clear()

        if 'fdfind' in get_executables():
            fd = 'fdfind'
        elif 'fd' in get_executables():
            fd = 'fd'
        else:
            self.fm.notify("Couldn't find fd in the PATH.", bad=True)
            return

        if self.arg(1):
            if self.arg(1)[:2] == '-d':
                depth = self.arg(1)
                target = self.rest(2)
            else:
                depth = '-d1'
                target = self.rest(1)
        else:
            self.fm.notify(":fd_search needs a query.", bad=True)
            return

        hidden = ('--hidden' if self.fm.settings.show_hidden else '')
        exclude = "--no-ignore-vcs --exclude '.git' --exclude '*.py[co]' --exclude '__pycache__'"
        command = '{} --follow {} {} {} --print0 {}'.format(
            fd, depth, hidden, exclude, target
        )
        fd = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)
        stdout, _ = fd.communicate()

        if fd.returncode == 0:
            results = filter(None, stdout.split('\0'))
            if not self.fm.settings.show_hidden and self.fm.settings.hidden_filter:
                hidden_filter = re.compile(self.fm.settings.hidden_filter)
                results = filter(lambda res: not hidden_filter.search(os.path.basename(res)), results)
            results = map(lambda res: os.path.abspath(os.path.join(self.fm.thisdir.path, res)), results)
            self.SEARCH_RESULTS.extend(sorted(results, key=str.lower))
            if len(self.SEARCH_RESULTS) > 0:
                self.fm.notify('Found {} result{}.'.format(len(self.SEARCH_RESULTS),
                                                           ('s' if len(self.SEARCH_RESULTS) > 1 else '')))
                self.fm.select_file(self.SEARCH_RESULTS[0])
            else:
                self.fm.notify('No results found.')

class fd_next(Command):
    """
    :fd_next
    Selects the next match from the last :fd_search.
    """

    def execute(self):
        if len(fd_search.SEARCH_RESULTS) > 1:
            fd_search.SEARCH_RESULTS.rotate(-1)  # rotate left
            self.fm.select_file(fd_search.SEARCH_RESULTS[0])
        elif len(fd_search.SEARCH_RESULTS) == 1:
            self.fm.select_file(fd_search.SEARCH_RESULTS[0])

class fd_prev(Command):
    """
    :fd_prev
    Selects the next match from the last :fd_search.
    """

    def execute(self):
        if len(fd_search.SEARCH_RESULTS) > 1:
            fd_search.SEARCH_RESULTS.rotate(1)  # rotate right
            self.fm.select_file(fd_search.SEARCH_RESULTS[0])
        elif len(fd_search.SEARCH_RESULTS) == 1:
            self.fm.select_file(fd_search.SEARCH_RESULTS[0])
# }}}

# {{{ ### --- fzf_locate --- ###
class fzf_locate(Command):
    """
    :fzf_locate
    Find a file using fzf.
    With a prefix argument select only directories.
    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        if self.quantifier:
            command="locate home | fzf -e -i"
        else:
            command="locate home | fzf -e -i"
        fzf = self.fm.execute_command(command, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.decode('utf-8').rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)
# }}}

# {{{ ### --- fzf_content_open --- ###
# Search file content in current directory recursively with fzf and open target with (neo)vim
class fzf_content_open(Command):
    """
    :fzf_content_open
    Pre-requisites: fzf, rg, bat, awk, vim or neovim
    Using `rg` to search file content recursively in current directory.
    Filtering with `fzf` and preview with `bat`.
    Pressing `Enter` on target will open at line in (neo)vim.
    """

    def execute(self):
        import subprocess
        import os
        from ranger.ext.get_executables import get_executables

        if 'rg' in get_executables():
            rg = 'rg'
        else:
            self.fm.notify("Couldn't find rg in the PATH.", bad=True)
            return

        if 'fzf' in get_executables():
            fzf = 'fzf'
        else:
            self.fm.notify("Couldn't find fzf in the PATH.", bad=True)
            return

        if 'bat' in get_executables():
            bat = 'bat'
        else:
            self.fm.notify("Couldn't find bat in the PATH.", bad=True)
            return

        editor = None
        if 'nvim' in get_executables():
            editor = 'nvim'
        elif 'vim' in get_executables():
            editor = 'vim'

        if rg is not None and fzf is not None and bat is not None and editor is not None:
            # we should not recursively search through all file content from home directory
            if (self.fm.thisdir.path == self.fm.home_path):
                self.fm.notify("Searching from home directory is not allowed", bad=True)
                return
            fzf = self.fm.execute_command(
                'rg --line-number "${1:-.}" | fzf --delimiter \':\' \
                    --preview \'bat --color=always --highlight-line {2} {1}\' \
                    | awk -F \':\' \'{print "+"$2" "$1}\'',
                universal_newlines=True,stdout=subprocess.PIPE)

            stdout, _ = fzf.communicate()
            if fzf.returncode == 0:
                if len(stdout) < 2:
                    return

                selected_line = stdout.split()[0]
                full_path = stdout.split()[1].strip()

                file_fullpath = os.path.abspath(full_path)
                file_basename = os.path.basename(full_path)

                if os.path.isdir(file_fullpath):
                    self.fm.cd(file_fullpath)
                else:
                    self.fm.select_file(file_fullpath)

                self.fm.execute_command(editor + " " + selected_line + " " + file_basename)
# }}}
