# TODO:
- [x] Add scrollLockOn flag
- [x] add mouse for scrollwheel listening
  - [x] added click (ctrl+click) listener instead
- [ ] add auto window-switcher and try out different switch timers
- [ ] externalise keybinds (possibility to add multiple keybinds per action)
- [ ] set main window
- [x] launch only specific accounts
- [ ] relaunch possibility by getting window handles by their name, don't relaunch windows if present
- [ ] team-select + select-overlay run/close
- [ ] maximize all (keep current win - maximize it last), minimize all (except curent)
- [ ] add hook.py to detect current window

# Bugs:
- closing doesnt release proc ids and handles FIX this!
- closing already closed windows
  - pywintypes.error: (5, 'TerminateProcess', 'Access is denied.')
  - check if proc/window hwnd exists before closing
- handle cycling when window manually closed using try/except block

# Features
- launch any or all wow accounts
- multiple layouts
- adapt position based on order (if we launch 1,3,4 no empty space between 3 and 4)
- close certain windows
- keybind to click/interact with mouseover in game and python script listen and swap to next window with short delay this means 1 button to take action and cycle to next

# TODO
- [x] launch and rename wows
  - [x] launch
  - [x] sort out the 2 window problem
  - [x] rename
  - [ ] default positions
- [x] keyboarding listening
- [ ] position + resize on keybind
- [x] keybind to cycle thru wow windows


# Addon
- Follow and mount command with addon comm


# Launch and Rename hidden window issue
- try to differentiate the windows, this way we can launch all accounts and rename easily after

- [x] launch wows in quick succession
  - [x] store processIds
  - [ ] wait for games to launch
- [x] Get handles for windows named 'World of Warcraft'
  - [x] ignore invisible ones
- [x] win32process.GetWindowThreadProcessId to find it's processId
  - [x] rename to wowX where x is the account# associated with processId

- [x] Keep window handles associated with acc_ids


# Keyboard listening