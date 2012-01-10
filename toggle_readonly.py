import sublime, sublime_plugin, os, stat

class ToggleReadonlyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
      myFile = self.view.file_name()
      fileAtt = os.stat(myFile)[0]
      myPlatform = os.name

      if (myPlatform == 'nt'):
        if (not fileAtt & stat.S_IWRITE):
          sublime.status_message("Making "+myFile+" writable")
          os.chmod(myFile, stat.S_IWRITE)
      else:
        if (fileAtt & stat.UF_IMMUTABLE):
          sublime.status_message("Making "+myFile+" mutable")
          os.chflags(myFile, not stat.UF_IMMUTABLE)

    def is_enabled(self):
        return self.view.file_name() and len(self.view.file_name()) > 0
