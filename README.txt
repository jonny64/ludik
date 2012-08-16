1. DESCRIPTION

	This Sublime 2 plugin adds navigation hotkeys and templates for Eludia.pm framework (http://github.com/do-/eludia)

2. INSTALLATION

	There are two options:

	- installation via Sublime Package Control

	http://wbond.net/sublime_packages/package_control

	- Manual, via Sublime Text 2 console.

	This is accessed via the ctrl+` shortcut. Once open, paste the following command into the console:

	import urllib2,os; pf='ludik.sublime-package'; ipp=sublime.installed_packages_path(); os.makedirs(ipp) if not os.path.exists(ipp) else None; urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler())); open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://github.com/downloads/jonny64/ludik/ludik.sublime-package').read()); print 'Please restart Sublime Text to finish installation'

3. USAGE

	use following hotkeys to quickly switch/create functions in Content/Presentation:

	alt + g = get_item
	alt + s = select
	alt + g = draw_item
	alt + w = draw
	alt + u = do_update
	alt + c = do_create
	alt + d = do_delete

	F5      = goto model and back to screen where we started
