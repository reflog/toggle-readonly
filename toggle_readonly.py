import sublime, sublime_plugin, os, stat

s = sublime.load_settings('toggle-readonly.sublime-settings') 


def changeReadonly(filename, state):
    if (os.name == 'nt'):
        flag = ~stat.S_IWRITE
        if not state:
            flag = ~flag;
        os.chmod(filename, flag)
    else:  
        flag = ~stat.UF_IMMUTABLE
        if not state:
            flag = flag;
        os.chflags(filename, flag)

def isReadonly(filename):
    if not filename or len(filename) <= 0:
        return False

    fileAtt = os.stat(filename)[0]
 
    if (os.name == 'nt'): 
        return not (fileAtt & stat.S_IWRITE)
    else:
        return not (fileAtt & stat.UF_IMMUTABLE)


class ClearChangesCommand(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if s.get('auto_remove_readonly_on_save'): 
            if isReadonly(view.file_name()):
                changeReadonly(view.file_name(), False)


class SetReadonlyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        changeReadonly(self.view.file_name(), True)

    def is_enabled(self):
        return not isReadonly(self.view.file_name())

    def is_visible(self):
        return self.is_enabled()


class SetWritableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        changeReadonly(self.view.file_name(), False)

    def is_enabled(self):
        return isReadonly(self.view.file_name())

    def is_visible(self):
        return self.is_enabled()
