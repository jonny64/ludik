import sublime, sublime_plugin, os

class LudikMoveCommand(sublime_plugin.TextCommand):
	"""seeks and sets cursor to the beggining of standart eludia screen function"""

	def run(self, edit, action): 

		self.edit = edit

		if action == 'model':
			self.__goto_model()
			return
		
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
		
		self.action = action
		sublime.set_timeout(self.__seek_if_view_loaded, 250)

	def __seek_if_view_loaded(self):
		if self.opened_view.is_loading():
			sublime.set_timeout(self.__seek_if_view_loaded, 250)
			return
		
		sublime.status_message(self.__subname(self.action))
		self.__goto_sub(self.opened_view, self.action)

	def __goto_sub(self, view, action):
		
		subname = self.__subname(action)
		pt = view.find(subname, 0)
		
		if pt:
			view.sel().clear()
			view.sel().add(pt.begin())

			view.show(pt.begin())
			return

		if sublime.ok_cancel_dialog(subname + ' doesn''t exist. Create it?'):
			sub_header = "\n################################################################################\n\n"
			sub_body = subname + ' { # comments go here\n' + self.__sub_template(action) + "\n}"
			sub_definition = sub_header + sub_body + "\n"

			view.sel().clear()
			view.insert(self.edit, 0, sub_definition)
			view.sel().add(view.text_point(4, 0))
			view.show(0)
			sublime.status_message(subname + ' created.')

	def __sub_template(self, action):

		template_path = os.path.join(
			sublime.packages_path(),
			'ludik',
			'templates',
			'sub_' + action + '.tpl'
		)

		template = open(template_path, 'r').read()

		template = template.decode('cp1251').replace('__TYPE__', self.__currentScreenType())
		return template

	def __subname(self, action):
		return 'sub ' + action + '_' + self.__currentScreenType()

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


	def __goto_model(self): 
		
		sublime.status_message(self.__current_folder())
		
		if self.__current_folder() == 'Model':
			self.__switch_to(self.old_folder)
			return

		self.old_folder = self.__current_folder()
		self.__switch_to('Model')
	
	
	def __current_folder(self):
		
		folder_abspath = os.path.dirname(self.view.file_name())
		
		return os.path.split(folder_abspath)[1]

class LudikSave(sublime_plugin.EventListener):
	"""writes model to database after model file editing"""

	def on_post_save(self, view):

		folder_abspath = os.path.dirname(view.file_name())
		current_folder = os.path.split(folder_abspath)[1]
		if current_folder != 'Model':
			return

		for module_folder in view.window().folders():

			menu_file = os.path.join(module_folder, 'lib', 'Content', 'menu.pm')
			if os.path.exists(menu_file):
				self.touch(menu_file)
				print 'touch ' + menu_file

	def touch(self, fname, times=None):
		with file(fname, 'a'):
			os.utime(fname, times)
