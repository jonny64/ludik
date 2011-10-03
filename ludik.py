import sublime, sublime_plugin  

class LudikMoveCommand(sublime_plugin.TextCommand):
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
		self.__switch_to(action_folder[action])
		self.goto_sub('sub ' + action + '_' + self.__currentScreenType())

	def goto_sub(self, subname):

		pt = self.view.find(subname, 0)

		if pt:
			self.view.sel().clear()
			self.view.sel().add(pt.begin())

			self.view.show(pt.begin())
	
	def __currentScreenType(self):
		pass

	def __switch_to(self, folder):
		pass
