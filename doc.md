# TODO
- [x] launch and rename wows
  - [x] launch
  - [x] sort out the 2 window problem
  - [x] rename
  - [ ] default positions
- [ ] keyboarding listening
- [ ] position + resize on keybind
- [ ] keybind to cycle thru wow windows


# Addon
- Follow and mount command with addon comm


pyinput



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