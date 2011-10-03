import sublime, sublime_plugin, os

class LudikMoveCommand(sublime_plugin.TextCommand):
	"""seeks and sets cursor to the beggining of standart eludia screen function"""

	def run(self, edit, action): 

		action_folder = {
			'get_item_of'  : 'Content',
			'select'       : 'Content',
			'do_update'    : 'Content',
			'do_create'    : 'Content',
			'do_delete'    : 'Content',
			'draw_item_of' : 'Presentation',
			'draw'         : 'Presentation'
		}

		self.opened_view = self.__switch_to(action_folder[action])
		self.search_for_sub = 'sub ' + action + '_' + self.__currentScreenType()
		sublime.set_timeout(self.__seek_if_view_loaded, 250)

	def __seek_if_view_loaded(self):
		if self.opened_view.is_loading():
			sublime.set_timeout(self.__seek_if_view_loaded, 250)
			return
		
		sublime.status_message(self.search_for_sub)
		self.__goto_sub(self.opened_view, self.search_for_sub)

	def __goto_sub(self, view, subname):
		
		pt = view.find(subname, 0)
		
		if pt:
			view.sel().clear()
			view.sel().add(pt.begin())

			view.show(pt.begin())
	
		
	def __currentScreenType(self):
		file_name = os.path.basename(self.view.file_name())
		return os.path.splitext(file_name)[0]

	def __switch_to(self, target_folder):
		
		current_screen_folder = os.path.dirname(self.view.file_name())
		
		lib_dir = os.path.dirname(current_screen_folder)
		new_file = os.path.join(lib_dir, target_folder, self.__currentScreenType()) + '.pm'

		if not os.path.exists(new_file):
			sublime.status_message('file ' + new_file + ' does not exist')
			return

		return self.view.window().open_file(new_file)

