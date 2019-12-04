import sublime, sublime_plugin, os
from shutil import copyfile

class LudikMoveCommand(sublime_plugin.TextCommand):
	"""seeks and sets cursor to the beggining of standart eludia screen function"""

	def run(self, edit, action):
		self.edit = edit
		self.xtr = False

		action_folder = {
			'get_item_of'     : 'Content',
			'select'          : 'Content',
			'do_update'       : 'Content',
			'validate_update' : 'Content',
			'do_create'       : 'Content',
			'do_delete'       : 'Content',
			'validate_delete' : 'Content',
			'draw_item_of'    : 'Presentation',
			'draw'            : 'Presentation'
		}

		self.xtr = self.view.file_name().endswith('.js') or self.view.file_name().endswith('.html')
		self.xtr = self.xtr or '\\back\\' in self.view.file_name()

		if action == 'model':
			self.__goto_model()
			return

		if action == 'copy':
			self.__copy_type()
			return

		if self.xtr:

			action_folder.update ({
				'html'            : 'html',
				'do_delete'       : 'js\\data',
				'draw'            : 'js\\view'
			})

		self.action = action


		if self.view.file_name() == self.__build_new_file_name (action_folder[action]):

			sublime.status_message(self.__subname(self.action))
			self.__goto_sub(self.view, self.action)

		else:
			self.opened_view = self.__switch_to(action_folder[action])

	def __goto_sub(self, view, action):

		subname = self.__subname(action)
		pt = view.find(subname, 0)

		if pt:
			view.sel().clear()
			view.sel().add(pt.begin())

			view.show(pt.begin())
			return

		if (not self.xtr or 'Content' in self.view.file_name()) and sublime.ok_cancel_dialog(subname + ' doesn''t exist. Create it?'):
			sub_header = "\n################################################################################\n\n"
			sub_body = subname + ' { # comments go here\n\n' + self.__sub_template(action) + "\n}"
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

		template = open(template_path, 'rb').read()

		template = template.decode('cp1251').replace('__TYPE__', self.__currentScreenType())
		return template

	def __subname(self, action):

		if 'Content' in self.view.file_name() and self.view.file_name().endswith('.js'):
			return action + '_' + self.__currentScreenType() + ':'

		return 'sub ' + action + '_' + self.__currentScreenType()

	def __currentScreenType(self):
		file_name = os.path.basename(self.view.file_name())
		return os.path.splitext(file_name)[0]

	def __build_new_file_name(self, target_folder):
		current_screen_folder = os.path.dirname(self.view.file_name())

		lib_dir = os.path.dirname(current_screen_folder)

		ext = '.pm'

		if self.xtr:
			if target_folder == 'html':
				ext = '.html'
			if target_folder.startswith('js'):
				ext = '.js'

			while 'back' in lib_dir or 'front' in lib_dir:
				lib_dir = os.path.dirname(lib_dir)

			sublime.status_message (target_folder)
			if 'Content' in target_folder or 'Model' in target_folder:
				lib_dir = os.path.join(lib_dir, 'back', 'lib')
			else:
				if os.path.exists(os.path.join(lib_dir, 'front', 'root', 'extra')):
					lib_dir = os.path.join(lib_dir, 'front', 'root', 'extra', '_', 'app')
				else:
					lib_dir = os.path.join(lib_dir, 'front', 'root', '_', 'app')

		file = os.path.join(lib_dir, target_folder, self.__currentScreenType())

		if os.path.exists(file + '.js'):
			ext = '.js'

		return file + ext

	def __switch_to(self, target_folder):

		new_file = self.__build_new_file_name (target_folder)

		if not os.path.exists(new_file):
			name, ext = os.path.splitext(new_file)
			if  name.endswith('_list'):
				new_file = name[:-5] + ext
			else:
				new_file = name + '_list' + ext

			if not os.path.exists(new_file):
				new_file = name + 's' + ext

			if not os.path.exists(new_file):
				new_file = name + '.js'

			if not os.path.exists(new_file):
				new_file = name + 's' + '.js'

			if not os.path.exists(new_file) and name.endswith('_roster'):
				new_file = name[:-7] + '.js'

			if not os.path.exists(new_file) and name.endswith('_new'):
				new_file = name[:-4] + 's' + '.js'

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

	def __copy_type(self):

		sublime.status_message("__copy_type")

		def on_done(copy_type_name):
			sublime.status_message("copy starts...")

			copy_files = []

			for action in ['Content', 'js\\data', 'js\\view', 'html', 'Model']:
				src = self.__build_new_file_name (action)
				try:
					dst = os.path.join(os.path.dirname(src), copy_type_name + os.path.splitext(src)[1])
					if not os.path.exists(dst):
						copyfile(src, dst)
					copy_files.append(dst)
				except FileNotFoundError as e:
					pass

			for dst in copy_files:
				self.view.window().open_file(dst)

			sublime.status_message("copy done from " + copy_type_name)

		def on_change(copy_type_name):
			pass

		def on_cancel():
			sublime.status_message("Copy cancelled")

		window = self.view.window()
		window.show_input_panel("Copy current type to:", "", on_done, on_change, on_cancel)

	def __current_folder(self):

		folder_abspath = os.path.dirname(self.view.file_name())

		return os.path.split(folder_abspath)[1]

class LudikSave(sublime_plugin.EventListener):
	"""writes model to database after model file editing"""

	def on_post_save(self, view):

		folder_abspath = os.path.dirname(view.file_name())
		current_folder = os.path.split(folder_abspath)[1]
		library_file = os.path.basename(view.file_name()).startswith('_lib');
		if current_folder != 'Model' and not library_file:
			return
		for module_folder in view.window().folders():

			menu_path = ['lib', 'Config.pm'] if library_file else ['lib', 'Content', 'menu.pm']
			if os.path.split(module_folder)[1] == 'lib':
				menu_path.remove('lib')

			menu_file = os.path.join(module_folder, *menu_path)

			if os.path.exists(menu_file):
				self.touch(menu_file)
				print ('touch ' + menu_file)

	def touch(self, fname, times=None):
		with open(fname, 'a'):
			os.utime(fname, times)
